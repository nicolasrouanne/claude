---
name: cra
description: "Suivi du temps : réconciliation Toggl, Billi CRA et git commits. Vue d'ensemble et détection d'écarts entre les sources."
title: /cra
parent: Skills
permalink: /skills/cra/
nav_order: 14
---

# CRA — Suivi du temps

Skill chapeau pour le suivi du temps de travail. Orchestre les 3 sources de données sans dupliquer leur logique.

## Sources de temps

| Source | Rôle | Skill dédié | Pour qui |
|--------|------|-------------|----------|
| **Toggl** | Source de vérité (temps réel) | `/toggl-calendar` | Nicolas (accès Toggl personnel) |
| **Billi CRA** | Déclaratif client | `/billi-cra` | Tous les freelances/salariés |
| **Git commits** | Proxy jours travaillés | — (commandes git) | Collaborateurs sans Toggl |

## Billi — Accès API

- **App** : https://app.billi.so | **API** : https://api.billi.so
- **Credentials** : 1Password, item "Billi Qraft - Agency User" dans vault Qraft
- **Auth** : OAuth password grant (voir `/billi-cra` pour le détail auth)

### Récupérer les CRA via l'API

```bash
# 1. Get token
curl -s -X POST https://api.billi.so/oauth/token \
  -H "Content-Type: application/json" \
  -d '{"grant_type":"password","email":"<email>","password":"<password>"}'

# 2. Fetch CRAs
curl -s https://api.billi.so/activity_reports \
  -H "Authorization: Bearer <token>" \
  -H "Accept: application/json"
# Returns activity_reports with: id, month, state, duration, mission, company, freelancer, activities
```

## Git commits — Extraction jours travaillés

Pour les collaborateurs qui n'ont pas Toggl, les commits git servent de proxy :

```bash
# Tous les auteurs sur une année
git -C <repo> log --after="YYYY-01-01" --before="YYYY+1-01-01" --format='%aN' | sort | uniq -c | sort -rn

# Jours uniques par auteur
git -C <repo> log --after="YYYY-01-01" --before="YYYY+1-01-01" --author="Nom" --format="%ad" --date=format:"%Y-%m-%d" | sort -u | wc -l

# Détail jour par jour (pour vérification)
git -C <repo> log --after="YYYY-01-01" --before="YYYY+1-01-01" --author="Nom" --format="%ad" --date=format:"%Y-%m-%d" | sort -u
```

## Your Task

Quand l'utilisateur invoque `/cra` :

### Sans argument — Vue d'ensemble

Demander la période (mois ou plage) et afficher un résumé par source :
1. Toggl : `python3 ~/dev/qraft/toggl/main.py <mois>` (ou pointer vers `/toggl-calendar`)
2. Billi : nombre de CRA remplis/en attente pour la période
3. Git : jours de commits par auteur sur les repos pertinents

### Avec un sujet

- `/cra toggl <mois>` → déléguer à `/toggl-calendar`
- `/cra billi import/export` → déléguer à `/billi-cra`
- `/cra git <repo> <année>` → extraire les jours de commits
- `/cra compare <mois> <personne>` → réconcilier les sources :
  1. Récupérer le temps Toggl (si disponible pour cette personne)
  2. Récupérer les CRA Billi pour cette personne/mois
  3. Récupérer les jours de commits git
  4. Afficher un tableau comparatif et signaler les écarts

### Réconciliation

Quand on compare les sources, les règles sont :
- **Toggl vs Billi** : Toggl est la référence. Si Billi a moins → CRA à compléter
- **Git vs Billi** : Git est indicatif (un jour sans commit ≠ un jour sans travail). Mais un jour avec commit ET sans CRA → probable oubli
- **Seuil d'alerte** : écart > 2 jours sur un mois → signaler
