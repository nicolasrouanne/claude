# Qraft — Non-dev workspace

This is the workspace for qraft non-dev tasks:
- Time tracking (toggl)
- Content editing (notion)
- File management (gogcli / Google Drive)
- Client communications

## Notion

Always use the local Notion MCP server (`mcp__notion__API-*` tools) for all Notion operations. Never use the claude.ai Notion connector (`mcp__claude_ai_Notion__*`) — it connects to a different workspace and won't have access to Qraft pages.

## Billi — Plateforme SaaS de gestion d'agences de freelances

### Accès

- **App** : https://app.billi.so | **API** : https://api.billi.so
- **Credentials** : 1Password, item "Billi Qraft - Agency User" dans vault Qraft
- **Auth API** : Bearer token via cookie `access_token` après login sur l'app
- **Repo** : https://github.com/billiapp/billi | Local : `~/dev/billi/billi`
- **Stack** : Rails 8.1 (API, `api/`) + Next.js 15 (frontend, `web/`)

### Récupérer les CRA via l'API

Après connexion dans Chrome, exécuter dans la console :
```javascript
const token = document.cookie.match(/access_token=([^;]+)/)[1];
const res = await fetch('https://api.billi.so/activity_reports', {
  headers: { 'Authorization': `Bearer ${token}`, 'Accept': 'application/json' }
});
const data = await res.json();
// data.data contient les activity_reports avec: id, month, state, duration, mission, company, freelancer, activities
```

### Récupérer les jours de commits par auteur

```bash
git -C ~/dev/billi/billi log --after="YYYY-01-01" --before="YYYY+1-01-01" --format='%aN' | sort | uniq -c | sort -rn
# Jours uniques par auteur :
git -C ~/dev/billi/billi log --after="YYYY-01-01" --before="YYYY+1-01-01" --author="Nom" --format="%ad" --date=format:"%Y-%m-%d" | sort -u | wc -l
```

### Missions Billi dans Billi (dogfooding)

- Mission "CTO" (Nicolas Rouanne) — depuis sept. 2025
- Mission "Direction technique" (Alexis Nugon) — en cours
- Note : les CRA dans Billi sont peu remplis, les commits git sont une meilleure source pour le temps passé

### Contributeurs principaux (2025)

| Auteur | Commits | Jours uniques |
|--------|---------|---------------|
| Adrien Lupo | 178 | 34 (jan-mars) |
| Thomas Demoncy (+Thomas) | 138 | N/A (non déclaré CII) |
| Thibaud | 120 | N/A (non déclaré CII) |
| Nicolas Rouanne | 96 | 29 |
| Alexis Nugon (+Alexis) | 38 | 20 |

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

### Déclaration 2024 Qraft (référence)

- **Projet** : P1 Billi, type Innovation (CII)
- **Personnel** : Lili LIARDET (junior, CDI, sortie 29/03/2024), Adrien Lupo (CDI, entré 01/07/2024)
- **Temps** : Lili 61j, Adrien 123j, total 184j (0.5j/mois enlevé pour admin)
- **Dépenses** : Personnel 37 867€ + Amortissements 601€ = 38 468€
- **CII** : 11 540€ (taux 30%)
- **Méthodologie temps** : CRA dans Billi (dogfooding)
- **Description Qraft** : "agence tech experte en développement d'applications web et mobile sur mesure"
- **Équipe R&D** : "4 développeurs, dont deux fondateurs expérimentés (10 et 15 ans) et deux profils plus juniors"
