---
name: cii
description: "Dossier CII/CIR : accès Finalli, données de référence, extraction temps personnel pour les déclarations de crédit d'impôt innovation."
---

# CII / CIR — Dossier Crédit d'Impôt Innovation

Skill pour travailler sur les déclarations CII/CIR sur la plateforme Finalli.

## Finalli — Plateforme dossier CII/CIR

- **URL** : https://app.finalli.com
- **Credentials** : 1Password, item "Finalli (Self & Innov)" dans vault Qraft (nicolas@qraft.tech)
- **Cabinet** : Self & Innov (anciennement selforiel)

### Déclarations existantes

| Déclaration | URL |
|---|---|
| CII 2025 — Qraft | https://app.finalli.com/selforiel/page/1385be93-ef44-4348-844f-dbf16ce0397d/1 |
| CII 2024 — Qraft (validé) | https://app.finalli.com/selforiel/page/e6bf3102-f265-453c-81b6-6ac70ca9b1cf/1 |
| CII 2024 — Gybe | https://app.finalli.com/selforiel/page/a941f448-1299-4c7e-87ee-5feb3cd7d77c/1 |
| CII 2021 — Qraft | https://app.finalli.com/selforiel/page/JN6-061-GWN-WBB-YFC/1 |

### Structure des pages (URL = base + /N)

| Page | Section | Contenu |
|------|---------|---------|
| /1 | Synthèse | Vue d'ensemble financière |
| /2 | 1. Identification | Infos entreprise, SIREN, comptable, CA, salariés |
| /3 | 2. Description entreprise | Présentation, activité R&D, équipe |
| /4 | 3. Projets | Liste des projets (P1 Billi = Innovation CII) |
| /5 | 4. Personnel | Personnes déclarées (nom, poste, contrat, diplôme, dates) |
| /6 | 5. Temps passés | Jours travaillés, absences, temps par projet |
| /7 | 6. Rémunérations | Salaires bruts, charges patronales |
| /8 | 7. Sous-traitance | Sous-traitance R&D |
| /9 | 8. Dotations aux amortissements | Matériel (PC, etc.) |
| /10 | 9. Propriété intellectuelle | Brevets, licences |
| /19 | Documents | Pièces justificatives (CV, bulletins, CRA) |

## Description Qraft (pour le dossier)

- **Activité** : "agence tech experte en développement d'applications web et mobile sur mesure"
- **Équipe R&D** : "4 développeurs, dont deux fondateurs expérimentés (10 et 15 ans) et deux profils plus juniors"

## Déclaration 2024 Qraft (référence)

Utiliser comme baseline pour les déclarations suivantes :

- **Projet** : P1 Billi, type Innovation (CII)
- **Personnel** : Lili LIARDET (junior, CDI, sortie 29/03/2024), Adrien Lupo (CDI, entré 01/07/2024)
- **Temps** : Lili 61j, Adrien 123j, total 184j (0.5j/mois enlevé pour admin)
- **Dépenses** : Personnel 37 867€ + Amortissements 601€ = 38 468€
- **CII** : 11 540€ (taux 30%)
- **Méthodologie temps** : CRA dans Billi (dogfooding)

## Sources de temps pour le personnel CII

Le temps déclaré vient de sources différentes selon la personne :

| Source | Pour qui | Commande/Skill |
|--------|----------|----------------|
| **Toggl** | Nicolas (CEO) | `/toggl-calendar` — source de vérité |
| **Git commits** | Collaborateurs sans Toggl (Adrien, Alexis, etc.) | Voir commandes ci-dessous |
| **Billi CRA** | Tous (déclaratif final) | `/billi-cra` |

### Extraction jours de commits par auteur

```bash
# Nombre de commits par auteur sur l'année
git -C ~/dev/billi/billi log --after="YYYY-01-01" --before="YYYY+1-01-01" --format='%aN' | sort | uniq -c | sort -rn

# Jours uniques de travail par auteur
git -C ~/dev/billi/billi log --after="YYYY-01-01" --before="YYYY+1-01-01" --author="Nom" --format="%ad" --date=format:"%Y-%m-%d" | sort -u | wc -l
```

### Contributeurs Billi 2025 (référence)

| Auteur | Commits | Jours uniques |
|--------|---------|---------------|
| Adrien Lupo | 178 | 34 (jan-mars) |
| Thomas Demoncy (+Thomas) | 138 | N/A (non déclaré CII) |
| Thibaud | 120 | N/A (non déclaré CII) |
| Nicolas Rouanne | 96 | 29 |
| Alexis Nugon (+Alexis) | 38 | 20 |

## Your Task

Quand l'utilisateur invoque `/cii` :

1. **Sans argument** : demander sur quelle déclaration travailler (année, entreprise)
2. **Avec un sujet** (ex: `/cii temps 2025`, `/cii personnel`) : aller directement à la section concernée
3. Pour le temps du personnel, utiliser la bonne source selon la personne (Toggl pour Nicolas, git commits pour les autres)
4. Toujours se référer à la déclaration 2024 comme baseline pour le format et les conventions
