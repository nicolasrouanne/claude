#!/usr/bin/env python3
"""Render a Notion page (exported as Markdown) into a Qraft-branded PDF.

Pipeline: Notion-flavored Markdown -> semantic HTML (Qraft house style) -> PDF
via headless Chrome. Content is rendered faithfully; only the letterhead and
visual styling are added. No text is rewritten, condensed, or dropped.

Usage:
    python3 notion_md_to_pdf.py INPUT.md OUTPUT.pdf \
        --title "Proposition refonte ARRC / EduFormUp" \
        --header-right "Proposition commerciale - Juin 2026"

The script is pure standard library. Supply the Markdown with
`API-retrieve-page-markdown`, and resolve any `<mention-page url=.../>` to a
plain `[Title](url)` link beforehand for exact link text.
"""

import argparse
import html as html_lib
import os
import re
import subprocess
import sys
import tempfile

# Candidate headless-browser binaries, first match wins.
CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    "google-chrome",
    "chromium",
]

# Notion callout background -> CSS class in style.css.
COLOR_MAP = {
    "blue_bg": "blue",
    "yellow_bg": "yellow",
    "gray_bg": "gray",
    "grey_bg": "gray",
    "orange_bg": "orange",
}

# Sentinels used to protect fragments from HTML escaping.
_BR = "\x00BR\x00"
_STAR = "\x00STAR\x00"


def inline(text):
    """Convert inline Markdown (bold, italic, code, links, <br>) to HTML."""
    text = re.sub(r"<br\s*/?>", _BR, text)
    # Unescape Notion's backslash escapes before HTML-escaping.
    for esc, raw in (("\\|", "|"), ("\\~", "~"), ("\\>", ">"),
                     ("\\<", "<"), ("\\*", _STAR), ("\\-", "-")):
        text = text.replace(esc, raw)
    text = html_lib.escape(text, quote=False)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return text.replace(_STAR, "*").replace(_BR, "<br>")


def collect_until(lines, start, end_tag):
    """Return (joined block, next index) spanning `lines[start]`..end_tag line."""
    buf = [lines[start]]
    if end_tag in lines[start]:
        return "\n".join(buf), start + 1
    i = start + 1
    while i < len(lines):
        buf.append(lines[i])
        if end_tag in lines[i]:
            return "\n".join(buf), i + 1
        i += 1
    return "\n".join(buf), i


def _keep_icon(icon):
    """Keep emoji icons; drop single-letter/digit Notion placeholders."""
    return bool(icon) and any(ord(ch) > 127 for ch in icon)


def render_callout(block):
    open_tag = re.search(r"<callout([^>]*)>", block).group(1)
    icon_m = re.search(r'icon="([^"]*)"', open_tag)
    color_m = re.search(r'color="([^"]*)"', open_tag)
    icon = icon_m.group(1) if icon_m else ""
    color = COLOR_MAP.get(color_m.group(1) if color_m else "", "gray")

    inner = re.sub(r"^.*?<callout[^>]*>", "", block, count=1, flags=re.S)
    inner = re.sub(r"</callout>\s*$", "", inner, flags=re.S)
    lines = [l.strip() for l in inner.split("\n") if l.strip()]

    parts, paras, bullets = [], [], []

    def flush():
        if paras:
            parts.append("<br>".join(inline(p) for p in paras))
            paras.clear()
        if bullets:
            parts.append("<ul>" + "".join(f"<li>{inline(b)}</li>"
                                          for b in bullets) + "</ul>")
            bullets.clear()

    for line in lines:
        if re.match(r"^[-*]\s+", line):
            if paras:
                parts.append("<br>".join(inline(p) for p in paras))
                paras.clear()
            bullets.append(re.sub(r"^[-*]\s+", "", line))
        else:
            if bullets:
                parts.append("<ul>" + "".join(f"<li>{inline(b)}</li>"
                                              for b in bullets) + "</ul>")
                bullets.clear()
            paras.append(line)
    flush()

    prefix = f"{icon} " if _keep_icon(icon) else ""
    return f'<div class="callout {color}">{prefix}{"".join(parts)}</div>'


def render_columns(block):
    cols = re.findall(r"<column>(.*?)</column>", block, flags=re.S)
    out = []
    for col in cols:
        callout = re.search(r"<callout.*?</callout>", col, flags=re.S)
        out.append(render_callout(callout.group(0)) if callout
                   else f"<div>{parse_blocks(col)}</div>")
    return f'<div class="cols">{"".join(out)}</div>'


def render_table(block):
    colgroup = ""
    cg = re.search(r"<colgroup>(.*?)</colgroup>", block, flags=re.S)
    if cg:
        tags = []
        for attrs in re.findall(r"<col([^>]*)>", cg.group(1)):
            wm = re.search(r'width="([\d.]+)"', attrs)
            tags.append(f'<col style="width:{round(float(wm.group(1)))}px">'
                        if wm else "<col>")
        colgroup = "<colgroup>" + "".join(tags) + "</colgroup>"

    rows_out = []
    for idx, (attrs, body) in enumerate(
            re.findall(r"<tr([^>]*)>(.*?)</tr>", block, flags=re.S)):
        cells = re.findall(r"<td>(.*?)</td>", body, flags=re.S)
        if idx == 0:  # header row
            rows_out.append("<tr>" + "".join(f"<th>{inline(c)}</th>"
                                             for c in cells) + "</tr>")
            continue
        color_m = re.search(r'color="([^"]*)"', attrs)
        color = color_m.group(1) if color_m else ""
        cls = " class=\"total\"" if color == "yellow_bg" else \
              " class=\"subtotal\"" if color in ("blue_bg", "grey_bg", "gray_bg") else ""
        rows_out.append(f"<tr{cls}>" + "".join(f"<td>{inline(c)}</td>"
                                               for c in cells) + "</tr>")
    return f"<table>{colgroup}{''.join(rows_out)}</table>"


def parse_blocks(md):
    """Convert block-level Notion Markdown to HTML. `#` maps to <h2> because the
    page title already occupies <h1>."""
    md = re.sub(r'<mention-page url="([^"]+)"\s*/>', r"[page liée](\1)", md)
    lines = md.split("\n")
    out, i, n = [], 0, len(md.split("\n"))
    while i < n:
        stripped = lines[i].strip()
        if stripped == "" or stripped == "---":
            i += 1
            continue
        if stripped.startswith("<callout"):
            block, i = collect_until(lines, i, "</callout>")
            out.append(render_callout(block))
            continue
        if stripped.startswith("<columns"):
            block, i = collect_until(lines, i, "</columns>")
            out.append(render_columns(block))
            continue
        if stripped.startswith("<table"):
            block, i = collect_until(lines, i, "</table>")
            out.append(render_table(block))
            continue
        heading = re.match(r"^(#{1,4})\s+(.*)$", stripped)
        if heading:
            level = min(len(heading.group(1)) + 1, 6)
            out.append(f"<h{level}>{inline(heading.group(2))}</h{level}>")
            i += 1
            continue
        if re.match(r"^\d+\.\s+", stripped):
            items = []
            while i < n and re.match(r"^\d+\.\s+", lines[i].strip()):
                items.append(inline(re.sub(r"^\d+\.\s+", "", lines[i].strip())))
                i += 1
            out.append("<ol>" + "".join(f"<li>{it}</li>" for it in items) + "</ol>")
            continue
        if re.match(r"^[-*]\s+", stripped):
            items = []
            while i < n and re.match(r"^[-*]\s+", lines[i].strip()):
                items.append(inline(re.sub(r"^[-*]\s+", "", lines[i].strip())))
                i += 1
            out.append("<ul>" + "".join(f"<li>{it}</li>" for it in items) + "</ul>")
            continue
        out.append(f"<p>{inline(stripped)}</p>")
        i += 1
    return "\n".join(out)


def build_html(markdown, title, header_right, css):
    body = parse_blocks(markdown)
    header = ""
    if header_right:
        header = (f'<div class="doc-header"><span class="brand">QRAFT</span>'
                  f'<span class="muted">{html_lib.escape(header_right)}</span></div>')
    title_html = f"<h1>{html_lib.escape(title)}</h1>" if title else ""
    return (f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8">'
            f"<style>{css}</style></head><body>{header}{title_html}{body}"
            f"</body></html>")


def find_chrome():
    for path in CHROME_CANDIDATES:
        if os.path.sep in path:
            if os.path.exists(path):
                return path
        elif subprocess.run(["which", path], capture_output=True).returncode == 0:
            return path
    return None


def html_to_pdf(html, out_pdf):
    chrome = find_chrome()
    if not chrome:
        sys.exit("No Chrome/Chromium binary found; edit CHROME_CANDIDATES.")
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False,
                                     encoding="utf-8") as tmp:
        tmp.write(html)
        html_path = tmp.name
    try:
        subprocess.run([
            chrome, "--headless", "--disable-gpu", "--no-pdf-header-footer",
            f"--print-to-pdf={out_pdf}", f"file://{html_path}",
        ], check=True, capture_output=True)
    finally:
        os.unlink(html_path)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", help="Notion Markdown file")
    ap.add_argument("output", help="Output PDF path")
    ap.add_argument("--title", default="", help="Document title (<h1>)")
    ap.add_argument("--header-right", default="",
                    help="Right-hand letterhead text, e.g. 'Proposition commerciale - Juin 2026'")
    ap.add_argument("--html-only", action="store_true",
                    help="Write HTML next to the output instead of a PDF")
    args = ap.parse_args()

    with open(args.input, encoding="utf-8") as f:
        markdown = f.read()
    css_path = os.path.join(os.path.dirname(__file__), "..", "assets", "style.css")
    with open(css_path, encoding="utf-8") as f:
        css = f.read()

    html = build_html(markdown, args.title, args.header_right, css)
    if args.html_only:
        out_html = os.path.splitext(args.output)[0] + ".html"
        with open(out_html, "w", encoding="utf-8") as f:
            f.write(html)
        print(out_html)
    else:
        html_to_pdf(html, args.output)
        print(args.output)


if __name__ == "__main__":
    main()
