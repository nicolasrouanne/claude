---
name: notion-pdf
description: "Render a Notion page (commercial proposal, client doc) as a Qraft-branded PDF, faithful to the Notion content. Notion markdown -> styled HTML -> PDF via headless Chrome."
title: /notion-pdf
parent: Skills
permalink: /skills/notion-pdf/
nav_order: 33
---

# notion-pdf — Notion page → Qraft-branded PDF

Renders a Notion page as a PDF with the Qraft letterhead and house style,
**faithful to the content**: nothing is rewritten, condensed, or dropped. Only
the letterhead and visual styling are added.

Use it to produce clean attachments (commercial proposals, client docs) when the
email also links the Notion page: the PDF and the link must show the **exact
same content**.

## Files

| File | Role |
|---|---|
| `assets/style.css` | The Qraft house style (typography, letterhead, callouts, tables, columns). **Source of truth for the formatting.** |
| `scripts/notion_md_to_pdf.py` | Converter: Notion markdown → styled HTML → PDF. Pure stdlib Python. |

## Workflow

1. **Fetch the page markdown**: `mcp__notion__API-retrieve-page-markdown` with
   the `page_id`.
2. **Fetch the exact title** (`API-retrieve-a-page`, `filter_properties=title`)
   → it becomes the `<h1>`.
3. **Resolve mentions**: replace each `<mention-page url="..."/>` with a markdown
   link `[Page title](url)` (fetch the linked page's title). Otherwise the
   script emits a generic link.
4. **Save the markdown** to a `.md` file (scratchpad).
5. **Render**:
   ```bash
   uv run python scripts/notion_md_to_pdf.py INPUT.md OUTPUT.pdf \
     --title "Exact Notion page title" \
     --header-right "Proposition commerciale - Juin 2026"
   ```
   Add `--html-only` to inspect the HTML without producing a PDF.

## Fidelity rules (important)

- **No content changes.** Render the markdown as-is: same bullets, same figures,
  same order, same wording. No invented subtitle, no condensing, no
  adding/removing participants.
- The `QRAFT · <header-right>` letterhead and the `<h1>` (page title) are the
  **only** added elements — that is the letterhead, not content.
- Notion dividers (`---`) are skipped (headings already carry a border). No text
  is lost.
- After rendering, check that amounts/efforts in the PDF match Notion exactly.

## Formatting mapping

- Notion headings: `#` → `<h2>`, `##` → `<h3>`, `###` → `<h4>` (the `<h1>` is the
  page title).
- Callouts: `blue_bg`/`yellow_bg`/`gray_bg`/`orange_bg` → `.callout.blue` etc.
  Emoji icons are kept; single letter/digit Notion placeholders (`r`, `t`, `1`…)
  are dropped.
- Tables: first row → header (`<th>`, blue background); `yellow_bg` row →
  `tr.total` (yellow); `blue_bg` row → `tr.subtotal` (blue). Column widths
  (`<colgroup>`) are preserved.
- Notion columns (`<columns>`) → `.cols` (flex).

## Requirements

- **Chrome/Chromium** installed (macOS: Google Chrome by default). The script
  auto-detects the binary; edit `CHROME_CANDIDATES` otherwise.
- No Python dependencies (stdlib only).
