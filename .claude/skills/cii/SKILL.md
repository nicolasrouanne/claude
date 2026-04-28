---
name: cii
description: "Dossier CII/CIR : accès Finalli, données de référence, extraction temps personnel pour les déclarations de crédit d'impôt innovation."
---

# CII / CIR — Dossier Crédit d'Impôt Innovation

Skill pour travailler sur les déclarations CII/CIR sur la plateforme Finalli.

## Finalli — Plateforme dossier CII/CIR

- **URL** : https://app.finalli.com
- **Credentials** : 1Password, item "Finalli (Self & Innov)" dans vault Qraft
- **Cabinet** : Finalli (anciennement Self & Innov)

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

## Déclaration 2024 Qraft (référence)

Utiliser la déclaration CII 2024 Qraft comme baseline pour les déclarations suivantes :
- **Projet** : P1 Billi, type Innovation (CII)
- **Taux CII** : 30%
- **Méthodologie temps** : CRA dans Billi (dogfooding)
- **Postes de dépenses** : Personnel, Amortissements (matériel)
- **Convention** : 0.5j/mois enlevé pour admin par personne
- Pour les données exactes (personnel, montants), consulter la déclaration sur Finalli directement

## Source de temps pour le personnel CII

Le temps déclaré pour le CII est basé sur les **CRA Billi** (`/billi-cra`, `/cra`).

Les commits git peuvent servir de lecture complémentaire pour vérifier la cohérence, mais ne sont pas la source officielle. Utiliser `/cra git` pour cette analyse.

## Your Task

Quand l'utilisateur invoque `/cii` :

1. Demander quelle déclaration (année, entreprise) si pas précisé
2. Pour le temps du personnel, toujours utiliser Billi CRA (`/billi-cra`). Les autres sources (git, toggl) sont secondaires
3. Se référer à la déclaration de l'année fiscale passée comme baseline pour le format et les conventions
