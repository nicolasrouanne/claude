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
- **Credentials** : 1Password, item `chezmoi_billi` dans le vault `AI Agents` (email via `op item get chezmoi_billi --vault "AI Agents" --fields username --reveal`, password via `op read "op://AI Agents/chezmoi_billi/password"`)
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

## Billi — Missions internes « Qraft — Interne » (non facturable)

Le temps sans client facturable (interne Qraft) est tracké dans un client Billi dédié **`Qraft — Interne`** (company id `605`, agency `1`, tarif **0 €**, freelancer Nicolas = `166`). 4 missions stables, reproductibles chaque mois :

| Mission | mission_id | rate_id | Contenu |
|---|---|---|---|
| Prospection | 304 | 297 | commercial, business dev, propositions |
| Opérations | 301 | 294 | RH, compta, admin, direction, veille |
| R&D / Innovation | 302 | 295 | recherche, POCs, tooling agentic (assiette CII) |
| Contentieux | 303 | 296 | litiges / contentieux |

### Mapping projet Toggl → mission interne (reproductible chaque mois)

| Projet Toggl (id) | → Mission |
|---|---|
| Prospection (159925478), Qraft › Prospection (217285296) | **Prospection** |
| Qraft (164497337), Administratif (190333392), Recrutement (195772172), Qraft › RH (217285294), Facturation (217285293), Veille & Research (217285295), Site coworking (212320887) | **Opérations** |
| Startup Studio › Car TCO (216891628), Qraft › Agentic Engineering (216891883) | **R&D / Innovation** |
| Projets « Contentieux » / « Organisation » du client en litige (IDs en config privée) | **Contentieux** |

**Exclure** (jamais dans un CRA interne) : projets clients facturables et le perso (Perso 149821005, Immobilier, Bruno, Administratif Gybe).

### Remplir un CRA interne (mensuel)
1. Agréger le temps brut Toggl par mission via le mapping ci-dessus.
2. Appliquer l'arrondi carry-forward (voir `/toggl-calendar`) **avec plafond 1,0 j/jour** — Billi refuse toute durée hors `{0, 0.5, 1.0}`.
3. `POST /activity_reports {"format":"billi","month":"YYYY-MM-01T00:00:00.000Z","mission_id":<id>}` puis `PUT /activity_reports/<cra_id> {"activities_attributes":[{date,duration,mission_rate_id}]}`.

## Règles de classement (facturable vs interne)

- **CRA client = uniquement le facturable.** Ne jamais facturer à un client du temps qui ne lui revient pas.
- **Contentieux** : jamais facturé au client adverse → `Qraft — Interne › Contentieux`.
- **R&D / agentic engineering** : → `R&D / Innovation`, assiette **CII** (voir `/cii`), pas un CRA client.
- **Un jour déjà déclaré dans un CRA Billi = vérité** (tu as travaillé, même si Toggl l'a raté) : garder les jours déclarés, compléter les jours non déclarés au prorata Toggl — **ne jamais supprimer un jour déclaré**.
- **Nettoyer Toggl avant de figer** : timers oubliés (>10h), pauses déj, entrées « Sans client » à réattribuer au bon projet (voir `/toggl-calendar`).

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
