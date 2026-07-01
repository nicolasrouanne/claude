---
name: notion-pdf
description: "Rendre une page Notion (proposition commerciale, doc client) en PDF à l'en-tête Qraft, fidèle au contenu Notion. Conversion markdown Notion → HTML charté → PDF via Chrome headless."
title: /notion-pdf
parent: Skills
permalink: /skills/notion-pdf/
nav_order: 33
---

# notion-pdf — Page Notion → PDF charté Qraft

Rend une page Notion en PDF avec l'en-tête et la charte Qraft, **fidèle au
contenu** : rien n'est réécrit, condensé ni supprimé. Seuls l'en-tête (papier à
en-tête) et la mise en forme visuelle sont ajoutés.

Sert à produire des pièces jointes propres (propositions commerciales, docs
client) quand le mail lie aussi la page Notion : le PDF et le lien doivent
montrer **exactement le même contenu**.

## Fichiers

| Fichier | Rôle |
|---|---|
| `assets/style.css` | La charte Qraft (typo, en-tête, callouts, tableaux, colonnes). **Source de vérité de la mise en forme.** |
| `scripts/notion_md_to_pdf.py` | Convertisseur : markdown Notion → HTML charté → PDF. Pure stdlib Python. |

## Workflow

1. **Récupérer le markdown** de la page Notion :
   `mcp__notion__API-retrieve-page-markdown` avec le `page_id`.
2. **Récupérer le titre exact** de la page (`API-retrieve-a-page`,
   `filter_properties=title`) → il devient le `<h1>`.
3. **Résoudre les mentions** : remplacer chaque
   `<mention-page url="..."/>` par un lien markdown `[Titre de la page](url)`
   (récupérer le titre de la page liée). Sinon le script met un lien générique.
4. **Sauver le markdown** dans un fichier `.md` (scratchpad).
5. **Générer** :
   ```bash
   uv run python scripts/notion_md_to_pdf.py INPUT.md OUTPUT.pdf \
     --title "Titre exact de la page Notion" \
     --header-right "Proposition commerciale - Juin 2026"
   ```
   Ajouter `--html-only` pour inspecter le HTML sans produire de PDF.

## Règles de fidélité (important)

- **Aucune modification de contenu.** On rend le markdown tel quel : mêmes
  puces, mêmes chiffres, même ordre, mêmes libellés. Pas de sous-titre inventé,
  pas de condensation, pas d'ajout/retrait de participants.
- L'en-tête `QRAFT · <header-right>` et le `<h1>` (titre de page) sont les
  **seuls** éléments ajoutés — c'est le papier à en-tête, pas du contenu.
- Les séparateurs Notion (`---`) sont ignorés (les titres portent déjà une
  bordure). Aucun texte n'est perdu.
- Vérifier après coup que les montants/efforts du PDF sont identiques à Notion.

## Mapping de mise en forme

- Titres Notion : `#` → `<h2>`, `##` → `<h3>`, `###` → `<h4>` (le `<h1>` est le
  titre de page).
- Callouts : `blue_bg`/`yellow_bg`/`gray_bg`/`orange_bg` → `.callout.blue` etc.
  Les icônes emoji sont gardées ; les placeholders Notion à une lettre/chiffre
  (`r`, `t`, `1`…) sont ignorés.
- Tableaux : 1ʳᵉ ligne → en-tête (`<th>`, fond bleu) ; ligne `yellow_bg` →
  `tr.total` (jaune) ; ligne `blue_bg` → `tr.subtotal` (bleu). Largeurs de
  colonnes (`<colgroup>`) préservées.
- Colonnes Notion (`<columns>`) → `.cols` (flex).

## Prérequis

- **Chrome/Chromium** installé (macOS : Google Chrome par défaut). Le script
  détecte le binaire ; adapter `CHROME_CANDIDATES` sinon.
- Aucune dépendance Python (stdlib uniquement).
