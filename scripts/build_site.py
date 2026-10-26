#!/usr/bin/env python3
"""Build the browsable HTML reader and PDFs for the offline study library.

Reads ``study/_meta/lessons.json`` and the Markdown files produced by
``scripts/extract_articles.py``, then writes:

    study/html/index.html              course home
    study/html/modules/mNN.html        module overview
    study/html/lessons/...html         one page per lesson
    study/html/print/mNN.html          print layout for module PDFs
    study/html/print/full.html         print layout for the full book
    study/html/assets/...              CSS, JS, search index, images
    study/pdf/*.pdf                    module PDFs + full-course PDF

Usage
-----
    python3 scripts/build_site.py
    python3 scripts/build_site.py --no-pdf
    python3 scripts/build_site.py --pdf-only
    python3 scripts/build_site.py --study /path/to/study

Requirements: markdown-it-py, Pygments, beautifulsoup4, PyYAML
    python3 -m pip install -r scripts/requirements.txt
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from html import escape
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from markdown_it import MarkdownIt
from pygments import highlight as pygments_highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import TextLexer, get_lexer_by_name
from pygments.util import ClassNotFound

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_STUDY = ROOT / "study"


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------


def strip_front_matter(text: str) -> str:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[end + 5 :].lstrip("\n")
    return text


def strip_lesson_header(markdown_text: str) -> str:
    """Remove the generated H1 + metadata block from a lesson body.

    The Markdown files keep that header so they read well on their own; the
    HTML and print layouts have their own title/meta header.
    """
    text = strip_front_matter(markdown_text)
    text = re.sub(r"\A# .+\n+", "", text, count=1).lstrip("\n")
    text = re.sub(r"\A(?:>.*\n)+(?:\n)*---\n+", "", text, count=1)
    return text


def slugify_heading(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:80]


def highlight_code(code: str, language: str, attrs: str) -> str:
    if not language:
        return escape(code)
    try:
        lexer = get_lexer_by_name(language, stripall=False)
    except ClassNotFound:
        return escape(code)
    return pygments_highlight(code, lexer, HtmlFormatter(nowrap=True))


def make_markdown(*, highlight: bool = True) -> MarkdownIt:
    md = MarkdownIt(
        "commonmark",
        {
            "html": True,
            "highlight": highlight_code if highlight else None,
            "typographer": False,
        },
    )
    md.enable("table")
    return md


def build_toc(headings: list[tuple[int, str, str]]) -> str:
    """Build a compact table of contents from h2/h3 headings.

    Some articles use only h3 section headings, so h3s that appear before the
    first h2 become top-level entries instead of being dropped.
    """
    usable: list[tuple[int, str, str]] = []
    for level, text, ident in headings:
        if level not in (2, 3):
            continue
        label = text.strip()
        if level == 3 and (
            label in {"...", "…", "•", "-"}
            or re.match(r"^(step|phase)\s+\d+$", label, re.I)
        ):
            continue
        usable.append((level, text, ident))

    if len(usable) < 3:
        return ""

    open_attr = " open" if len(usable) <= 12 else ""
    lines = [
        f'<details class="toc"{open_attr}>',
        "<summary>On this page</summary>",
        "<ul>",
    ]
    open_top = False
    open_sub = False

    def close_sub() -> None:
        nonlocal open_sub
        if open_sub:
            lines.append("</ul>")
            open_sub = False

    def close_top() -> None:
        nonlocal open_top
        close_sub()
        if open_top:
            lines.append("</li>")
            open_top = False

    for level, text, ident in usable:
        if level == 2:
            close_top()
            lines.append(f'<li><a href="#{ident}">{escape(text)}</a>')
            open_top = True
        elif open_top:
            if not open_sub:
                lines.append("<ul>")
                open_sub = True
            lines.append(f'<li><a href="#{ident}">{escape(text)}</a></li>')
        else:
            # h3 section before the first h2: show it at the top level.
            lines.append(f'<li><a href="#{ident}">{escape(text)}</a></li>')

    close_top()
    lines.extend(["</ul>", "</details>"])
    return "\n".join(lines)


def render_markdown(
    markdown_text: str,
    *,
    print_mode: bool = False,
    add_toc: bool = True,
) -> tuple[str, str]:
    """Render Markdown to HTML and return (html, toc_html)."""
    body = strip_front_matter(markdown_text)
    # Markdown images live at ../../assets/images from study/modules/...
    # HTML pages live one directory below study/html/, so the path is ../assets.
    body = body.replace("](../../assets/images/", "](../assets/images/")

    md = make_markdown(highlight=not print_mode)
    html = md.render(body)
    soup = BeautifulSoup(html, "html.parser")

    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.startswith(("http://", "https://")):
            link["target"] = "_blank"
            link["rel"] = "noopener noreferrer"

    for table in soup.find_all("table"):
        wrapper = soup.new_tag("div")
        wrapper["class"] = "table-wrap"
        table.wrap(wrapper)

    headings: list[tuple[int, str, str]] = []
    seen_ids: dict[str, int] = {}
    for tag in soup.find_all(["h2", "h3", "h4"]):
        text = tag.get_text(" ", strip=True)
        base = slugify_heading(text) or f"section-{len(headings) + 1}"
        count = seen_ids.get(base, 0) + 1
        seen_ids[base] = count
        ident = base if count == 1 else f"{base}-{count}"
        tag["id"] = ident
        if not print_mode:
            anchor = soup.new_tag("a", href=f"#{ident}")
            anchor["class"] = "anchor"
            anchor["aria-hidden"] = "true"
            anchor.string = "#"
            tag.append(soup.new_string(" "))
            tag.append(anchor)
        headings.append((int(tag.name[1]), text, ident))

    for image in soup.find_all("img"):
        if not print_mode:
            image["loading"] = "lazy"
            image["decoding"] = "async"
        if not image.get("alt"):
            image["alt"] = ""

    toc_html = build_toc(headings) if (add_toc and not print_mode) else ""
    return str(soup), toc_html


def plain_text(markdown_text: str, limit: int = 12000) -> str:
    text = strip_front_matter(markdown_text)
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[#>*_`|~-]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()[:limit]


# ---------------------------------------------------------------------------
# Static CSS and JS
# ---------------------------------------------------------------------------

CSS = r"""
:root {
  --bg: #fbfbfd;
  --bg-elev: #ffffff;
  --bg-soft: #f3f4f8;
  --text: #1b1f2a;
  --muted: #5f6b7a;
  --border: #e2e5ec;
  --accent: #4f46e5;
  --accent-strong: #3730a3;
  --accent-soft: #eef2ff;
  --code-bg: #1e1e2e;
  --code-text: #cdd6f4;
  --success: #16a34a;
  --warning: #b45309;
  --shadow: 0 1px 2px rgba(16,24,40,.06), 0 8px 24px rgba(16,24,40,.06);
  --sidebar-width: 312px;
  --content-width: 78ch;
  --radius: 12px;
}
[data-theme="dark"] {
  --bg: #0f1117;
  --bg-elev: #161a22;
  --bg-soft: #1d2330;
  --text: #e6e9f0;
  --muted: #9aa5b5;
  --border: #2a3140;
  --accent: #8b9cff;
  --accent-strong: #b4c0ff;
  --accent-soft: #1e2540;
  --code-bg: #111318;
  --code-text: #d8dee9;
  --success: #4ade80;
  --warning: #fbbf24;
  --shadow: 0 1px 2px rgba(0,0,0,.4), 0 8px 24px rgba(0,0,0,.3);
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto,
    "Helvetica Neue", Arial, sans-serif;
  font-size: 16px;
  line-height: 1.7;
  -webkit-font-smoothing: antialiased;
}
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
:target { scroll-margin-top: 84px; }
.skip-link {
  position: absolute; left: -9999px; top: 8px; z-index: 999;
  background: var(--bg-elev); color: var(--text); padding: 8px 12px;
  border: 1px solid var(--border); border-radius: 8px;
}
.skip-link:focus { left: 8px; }

/* Top bar */
.topbar {
  position: sticky; top: 0; z-index: 50;
  display: flex; align-items: center; gap: 12px;
  height: 60px; padding: 0 16px;
  background: var(--bg-elev);
  border-bottom: 1px solid var(--border);
}
.icon-btn {
  display: inline-flex; align-items: center; justify-content: center;
  width: 36px; height: 36px; flex: 0 0 36px;
  border: 1px solid var(--border); border-radius: 9px;
  background: var(--bg); color: var(--text);
  font-size: 16px; cursor: pointer;
}
.icon-btn:hover { background: var(--bg-soft); }
#menu-toggle { display: none; }
.brand {
  color: var(--text); font-weight: 750; letter-spacing: -.02em;
  white-space: nowrap; font-size: 15px;
}
.brand:hover { text-decoration: none; color: var(--accent); }
.search-wrap { position: relative; flex: 1 1 auto; max-width: 620px; margin: 0 auto; }
.search-wrap input {
  width: 100%; height: 38px; padding: 0 14px;
  border: 1px solid var(--border); border-radius: 9px;
  background: var(--bg); color: var(--text); font-size: 14px;
  outline: none;
}
.search-wrap input:focus { border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-soft); }
.search-results {
  position: absolute; left: 0; right: 0; top: 44px;
  max-height: min(70vh, 620px); overflow-y: auto;
  background: var(--bg-elev); border: 1px solid var(--border);
  border-radius: 12px; box-shadow: var(--shadow); padding: 6px;
}
.search-result {
  display: block; padding: 10px 12px; border-radius: 8px;
  color: var(--text); cursor: pointer;
}
.search-result:hover, .search-result.active { background: var(--accent-soft); text-decoration: none; }
.search-result-title { font-weight: 650; font-size: 14px; }
.search-result-meta { font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: .04em; margin-top: 2px; }
.search-result-snippet { font-size: 12.5px; color: var(--muted); margin-top: 4px; line-height: 1.45; }
.search-result mark { background: var(--accent-soft); color: var(--accent-strong); padding: 0 2px; border-radius: 3px; }
.search-empty { padding: 14px; color: var(--muted); font-size: 14px; }
.progress-mini {
  flex: 0 0 auto; min-width: 46px; text-align: center;
  font-size: 12px; font-weight: 650; color: var(--muted);
  border: 1px solid var(--border); border-radius: 999px; padding: 5px 9px;
}

/* Layout */
.layout { display: flex; align-items: flex-start; }
.sidebar {
  position: fixed; left: 0; top: 60px; bottom: 0; z-index: 40;
  width: var(--sidebar-width); overflow-y: auto;
  padding: 16px 12px 42px;
  background: var(--bg-elev); border-right: 1px solid var(--border);
}
.content-wrap { margin-left: var(--sidebar-width); width: calc(100% - var(--sidebar-width)); min-width: 0; }
.content { max-width: var(--content-width); margin: 0 auto; padding: 38px 28px 80px; }

/* Sidebar */
.progress-box {
  border: 1px solid var(--border); border-radius: 10px;
  background: var(--bg); padding: 12px; margin-bottom: 14px;
}
.progress-bar, .card-progress, .module-progress-bar {
  height: 7px; border-radius: 999px; background: var(--bg-soft);
  overflow: hidden;
}
.progress-bar > span, .card-progress > span, .module-progress-bar > span {
  display: block; height: 100%; width: 0; border-radius: inherit;
  background: linear-gradient(90deg, var(--accent), var(--success));
  transition: width .25s ease;
}
.progress-label { margin-top: 7px; font-size: 11.5px; color: var(--muted); }
.course-nav { font-size: 13.5px; }
.nav-home {
  display: block; padding: 8px 10px; border-radius: 7px;
  color: var(--text); font-weight: 650;
}
.nav-home:hover { background: var(--bg-soft); text-decoration: none; }
.nav-home.active { color: var(--accent-strong); background: var(--accent-soft); }
.nav-module { margin-top: 4px; border-radius: 8px; }
.nav-module > summary {
  display: flex; align-items: center; justify-content: space-between; gap: 8px;
  padding: 8px 10px; cursor: pointer; border-radius: 7px;
  color: var(--text); font-weight: 600; list-style: none;
}
.nav-module > summary::-webkit-details-marker { display: none; }
.nav-module > summary:hover { background: var(--bg-soft); }
.nav-module[open] > summary { color: var(--accent-strong); }
.nav-module-title { min-width: 0; }
.nav-count {
  flex: 0 0 auto; font-size: 10.5px; font-weight: 650; color: var(--muted);
  background: var(--bg-soft); border-radius: 999px; padding: 2px 7px;
}
.nav-module ul { list-style: none; margin: 2px 0 8px; padding: 0 0 0 7px; }
.nav-lesson {
  display: flex; align-items: flex-start; gap: 7px;
  padding: 5px 8px; border-radius: 6px; line-height: 1.4;
}
.nav-lesson:hover { background: var(--bg-soft); }
.nav-lesson.active { background: var(--accent-soft); }
.nav-lesson.active > a { color: var(--accent-strong); font-weight: 650; }
.nav-lesson > a { color: var(--text); min-width: 0; }
.nav-lesson > a:hover { text-decoration: none; }
.nav-check { flex: 0 0 auto; padding-top: 2px; }
.nav-check input { width: 14px; height: 14px; accent-color: var(--success); cursor: pointer; }
.nav-module-single { display: block; padding: 8px 10px; border-radius: 7px; color: var(--text); font-weight: 600; }
.nav-module-single:hover { background: var(--bg-soft); text-decoration: none; }

/* Headings and body copy */
h1, h2, h3, h4 { line-height: 1.25; letter-spacing: -.015em; scroll-margin-top: 84px; }
h1 { font-size: clamp(1.8rem, 3.2vw, 2.45rem); margin: 0 0 .5em; }
h2 { font-size: clamp(1.3rem, 2.2vw, 1.58rem); margin: 2.2em 0 .65em; padding-top: .55em; border-top: 1px solid var(--border); }
h3 { font-size: 1.16rem; margin: 1.8em 0 .55em; }
h4 { font-size: 1.03rem; margin: 1.5em 0 .45em; }
p { margin: .85em 0; }
ul, ol { padding-left: 1.45em; margin: .8em 0; }
li { margin: .32em 0; }
li > p { margin: .35em 0; }
strong { font-weight: 700; }
hr { border: 0; border-top: 1px solid var(--border); margin: 2.4em 0; }
blockquote {
  margin: 1.2em 0; padding: .75em 1.1em;
  border-left: 4px solid var(--accent); border-radius: 0 9px 9px 0;
  background: var(--accent-soft); color: var(--text);
}
blockquote > :first-child { margin-top: 0; }
blockquote > :last-child { margin-bottom: 0; }
.anchor { opacity: 0; margin-left: .3em; color: var(--muted); font-weight: 400; }
h2:hover .anchor, h3:hover .anchor, h4:hover .anchor { opacity: 1; }

/* Code and tables */
code, kbd, pre {
  font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas,
    "Liberation Mono", monospace;
}
code { font-size: .88em; }
:not(pre) > code {
  background: var(--bg-soft); padding: .15em .36em;
  border: 1px solid var(--border); border-radius: 5px;
  overflow-wrap: anywhere;
}
pre {
  background: var(--code-bg); color: var(--code-text);
  padding: 14px 16px; border-radius: 10px; overflow-x: auto;
  font-size: .84rem; line-height: 1.55; tab-size: 2;
}
pre code { background: none; border: 0; padding: 0; font-size: inherit; color: inherit; }
.table-wrap { overflow-x: auto; margin: 1.15em 0; border-radius: 9px; border: 1px solid var(--border); }
table { width: 100%; border-collapse: collapse; margin: 0; font-size: .92rem; }
th, td { border-bottom: 1px solid var(--border); padding: 8px 10px; text-align: left; vertical-align: top; }
th { background: var(--bg-soft); font-weight: 650; }
tr:last-child td { border-bottom: 0; }
tbody tr:nth-child(even) td { background: color-mix(in srgb, var(--bg-soft) 45%, transparent); }
img {
  max-width: 100%; height: auto; display: block;
  margin: 1.2em auto; border-radius: 10px;
  border: 1px solid var(--border); background: var(--bg-elev);
}

/* Lesson and module chrome */
.breadcrumb { font-size: 12.5px; color: var(--muted); margin: 0 0 10px; }
.breadcrumb a { color: var(--muted); }
.breadcrumb a:hover { color: var(--accent); }
.lesson-header { margin-bottom: 20px; }
.lesson-meta { display: flex; flex-wrap: wrap; gap: 8px 16px; align-items: center; color: var(--muted); font-size: 13px; }
.lesson-meta a { color: var(--accent); }
.lesson-tags { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 10px; }
.tag {
  display: inline-block; font-size: 11px; line-height: 1.4;
  color: var(--muted); background: var(--bg-soft);
  border: 1px solid var(--border); border-radius: 999px; padding: 2px 8px;
}
.read-toggle {
  display: inline-flex; align-items: center; gap: 7px;
  margin-top: 14px; padding: 7px 11px;
  border: 1px solid var(--border); border-radius: 9px;
  background: var(--bg-elev); font-size: 13px; cursor: pointer;
}
.read-toggle input { width: 15px; height: 15px; accent-color: var(--success); }
.video-links { margin: 12px 0 0; padding: 10px 12px; background: var(--bg-soft); border: 1px solid var(--border); border-radius: 9px; font-size: 13.5px; }
.video-links strong { margin-right: 4px; }
.toc {
  margin: 20px 0 24px; padding: 12px 14px;
  border: 1px solid var(--border); border-radius: 10px; background: var(--bg-elev);
}
.toc > summary { cursor: pointer; font-weight: 650; color: var(--text); }
.toc ul { margin: 8px 0 0; padding-left: 1.2em; }
.toc li { margin: .22em 0; }
.toc a { color: var(--muted); font-size: 13.5px; }
.toc a:hover, .toc a.active { color: var(--accent); }
.prev-next {
  display: grid; grid-template-columns: 1fr 1fr; gap: 12px;
  margin-top: 46px; padding-top: 20px; border-top: 1px solid var(--border);
}
.prev-next a {
  display: block; padding: 12px 14px; border: 1px solid var(--border);
  border-radius: 10px; background: var(--bg-elev); color: var(--text);
}
.prev-next a:hover { border-color: var(--accent); text-decoration: none; }
.prev-next .label { display: block; font-size: 10.5px; color: var(--muted); text-transform: uppercase; letter-spacing: .06em; margin-bottom: 3px; }
.prev-next .next { text-align: right; }
.footer { margin-top: 40px; padding-top: 18px; border-top: 1px solid var(--border); color: var(--muted); font-size: 12px; }
.footer p { margin: .3em 0; }

/* Course home */
.hero {
  padding: 34px 30px; border: 1px solid var(--border); border-radius: 16px;
  background:
    radial-gradient(1100px 260px at 12% -20%, var(--accent-soft), transparent 70%),
    var(--bg-elev);
  box-shadow: var(--shadow); margin-bottom: 26px;
}
.hero .kicker { margin: 0 0 8px; color: var(--accent); font-weight: 700; font-size: 12px; letter-spacing: .1em; text-transform: uppercase; }
.hero h1 { margin: 0 0 10px; max-width: 20ch; }
.hero p { color: var(--muted); max-width: 70ch; }
.hero-actions { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 18px; }
.btn {
  display: inline-flex; align-items: center; gap: 7px;
  padding: 9px 14px; border-radius: 9px; font-size: 13.5px; font-weight: 650;
  border: 1px solid var(--border); background: var(--bg-elev); color: var(--text);
}
.btn:hover { border-color: var(--accent); text-decoration: none; }
.btn-primary { background: var(--accent); border-color: var(--accent); color: #fff; }
.btn-primary:hover { background: var(--accent-strong); color: #fff; }
.stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 10px; margin-top: 22px; }
.stat { padding: 12px; border: 1px solid var(--border); border-radius: 10px; background: var(--bg-elev); }
.stat .value { font-size: 20px; font-weight: 750; letter-spacing: -.03em; }
.stat .label { font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: .05em; }
.home-progress { margin-top: 18px; }
.home-progress .progress-bar { height: 9px; }
.module-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(270px, 1fr)); gap: 14px; margin: 16px 0 30px; }
.module-card {
  display: flex; flex-direction: column; gap: 8px;
  padding: 16px; border: 1px solid var(--border); border-radius: 12px;
  background: var(--bg-elev); color: var(--text); box-shadow: 0 1px 2px rgba(16,24,40,.03);
  transition: border-color .15s ease, transform .15s ease, box-shadow .15s ease;
}
.module-card:hover { border-color: var(--accent); transform: translateY(-1px); box-shadow: var(--shadow); text-decoration: none; }
.module-card-head { display: flex; justify-content: space-between; gap: 10px; font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: .05em; }
.module-card h2 { font-size: 1.02rem; margin: 0; padding: 0; border: 0; line-height: 1.35; }
.module-card p { margin: 0; color: var(--muted); font-size: 13px; line-height: 1.5; }
.card-progress { margin-top: auto; }
.card-progress-text { font-size: 11px; color: var(--muted); }
.module-header {
  padding: 24px 24px 20px; border: 1px solid var(--border); border-radius: 14px;
  background: var(--bg-elev); box-shadow: var(--shadow); margin-bottom: 24px;
}
.module-header .kicker { margin: 0 0 6px; color: var(--accent); font-weight: 700; font-size: 11px; letter-spacing: .09em; text-transform: uppercase; }
.module-header h1 { margin: 0 0 8px; }
.module-header .lede { color: var(--muted); margin: 0; }
.module-header .module-progress { margin-top: 16px; }
.module-header .module-progress-meta { display: flex; justify-content: space-between; gap: 10px; font-size: 12px; color: var(--muted); margin-bottom: 6px; }
.lesson-table { width: 100%; border-collapse: collapse; margin-top: 16px; }
.lesson-table th, .lesson-table td { padding: 9px 8px; border-bottom: 1px solid var(--border); vertical-align: middle; }
.lesson-table th { font-size: 11px; text-transform: uppercase; letter-spacing: .05em; color: var(--muted); background: transparent; }
.lesson-table td { font-size: 14px; }
.lesson-table tr:last-child td { border-bottom: 0; }
.lesson-table input { width: 15px; height: 15px; accent-color: var(--success); }
.lesson-table .time { white-space: nowrap; color: var(--muted); font-size: 12px; }
.lesson-table .source { white-space: nowrap; font-size: 12px; }
.mark-module {
  display: inline-flex; align-items: center; gap: 6px; margin-top: 14px;
  padding: 8px 12px; border: 1px solid var(--border); border-radius: 8px;
  background: var(--bg); color: var(--text); font-size: 12.5px; cursor: pointer;
}
.mark-module:hover { border-color: var(--accent); }
.section-title { display: flex; align-items: baseline; justify-content: space-between; gap: 12px; }
.section-title h2 { border: 0; padding: 0; margin: 0 0 10px; }
.section-title .hint { color: var(--muted); font-size: 12px; }
.module-nav { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 30px; }
.module-nav a { display: block; padding: 12px 14px; border: 1px solid var(--border); border-radius: 10px; color: var(--text); background: var(--bg-elev); }
.module-nav a:hover { border-color: var(--accent); text-decoration: none; }
.module-nav .label { display: block; font-size: 10.5px; color: var(--muted); text-transform: uppercase; letter-spacing: .06em; margin-bottom: 3px; }
.module-nav .next { text-align: right; }

/* Mobile */
.sidebar-overlay { display: none; }
@media (max-width: 1000px) {
  #menu-toggle { display: inline-flex; }
  .sidebar {
    transform: translateX(-100%); transition: transform .2s ease;
    z-index: 60; box-shadow: var(--shadow);
  }
  body.sidebar-open .sidebar { transform: translateX(0); }
  body.sidebar-open .sidebar-overlay {
    display: block; position: fixed; inset: 60px 0 0; z-index: 55;
    background: rgba(0,0,0,.35);
  }
  .content-wrap { margin-left: 0; width: 100%; }
  .content { padding: 26px 18px 60px; }
  .brand { font-size: 14px; }
  .progress-mini { display: none; }
  .prev-next, .module-nav { grid-template-columns: 1fr; }
  .prev-next .next, .module-nav .next { text-align: left; }
}
@media (max-width: 620px) {
  .topbar { gap: 8px; padding: 0 10px; }
  .search-wrap { margin: 0; }
  .brand { display: none; }
  .hero { padding: 24px 20px; }
  .module-header { padding: 18px; }
  .lesson-table .source { display: none; }
}

/* Print */
@media print {
  .topbar, .sidebar, .footer, .search-wrap, .progress-mini, .read-toggle,
  .prev-next, .module-nav, .mark-module, .toc, .anchor, .sidebar-overlay,
  .skip-link { display: none !important; }
  .content-wrap { margin-left: 0 !important; width: 100% !important; }
  .content { max-width: none; padding: 0; }
  body { background: #fff; color: #111; font-size: 10.5pt; }
  a { color: #1a4fd6; text-decoration: none; }
  pre, blockquote, table, img, .table-wrap { break-inside: avoid; }
  h1, h2, h3, h4 { break-after: avoid; }
  pre { background: #f6f8fa; color: #111; border: 1px solid #ddd; }
  img { border: 1px solid #ddd; }
  .module-header { box-shadow: none; }
}

/* Print document (used by study/html/print/*.html) */
.print-body { background: #fff; color: #111; font-size: 10.5pt; line-height: 1.6; }
.print-body a { color: #1a4fd6; text-decoration: none; }
.print-document { max-width: 190mm; margin: 0 auto; }
.print-cover {
  min-height: 245mm; display: flex; flex-direction: column; justify-content: center;
  page-break-after: always; border-bottom: 2px solid #111; padding-bottom: 20mm;
}
.print-cover .kicker { font-size: 11pt; letter-spacing: .16em; text-transform: uppercase; color: #555; margin: 0 0 10mm; }
.print-cover h1 { font-size: 32pt; line-height: 1.1; margin: 0 0 6mm; letter-spacing: -.03em; }
.print-cover h2 { font-size: 18pt; line-height: 1.25; margin: 0 0 8mm; color: #333; border: 0; padding: 0; }
.print-cover .meta { color: #555; font-size: 10pt; }
.print-cover .notice { margin-top: 16mm; color: #666; font-size: 9pt; max-width: 120mm; }
.print-toc { page-break-after: always; }
.print-toc h1 { font-size: 24pt; margin: 0 0 8mm; }
.print-toc ul { list-style: none; padding-left: 0; margin: 0; }
.print-toc ul.toc-lessons { padding-left: 1.5em; }
.print-toc li { margin: .25em 0; }
.print-toc .module-entry { margin-top: .8em; font-weight: 650; }
.print-toc .lesson-entry { font-weight: 400; font-size: 9.5pt; color: #333; }
.print-module-title { page-break-before: always; padding-top: 10mm; }
.print-module-title .kicker { font-size: 10pt; letter-spacing: .14em; text-transform: uppercase; color: #666; margin: 0 0 4mm; }
.print-module-title h1 { font-size: 28pt; line-height: 1.15; margin: 0 0 6mm; }
.print-module-title .meta { color: #555; font-size: 9.5pt; }
.print-module-intro { margin: 0 0 8mm; }
.print-lesson { page-break-before: always; }
.print-lesson-kicker { font-size: 9pt; letter-spacing: .12em; text-transform: uppercase; color: #666; margin: 0 0 2mm; }
.print-lesson h1 { font-size: 22pt; line-height: 1.2; margin: 0 0 3mm; }
.print-lesson-meta { color: #555; font-size: 8.5pt; margin: 0 0 7mm; }
.print-lesson img { max-width: 100%; }
.print-lesson pre { font-size: 8pt; line-height: 1.45; }
.print-lesson table { font-size: 8.5pt; }
.print-lesson h2 { border-top: 1px solid #ddd; padding-top: 3mm; }
.print-lesson .toc { display: none; }
.print-footer { margin-top: 10mm; padding-top: 3mm; border-top: 1px solid #ddd; color: #666; font-size: 8pt; text-align: center; }

@page { size: A4; margin: 18mm 16mm 20mm; }
"""


JS = r"""
(function () {
  "use strict";

  var root = document.documentElement.dataset.root || "";
  var READ_KEY = "aec-read-v1";
  var THEME_KEY = "aec-theme-v1";

  function loadRead() {
    try { return new Set(JSON.parse(localStorage.getItem(READ_KEY) || "[]")); }
    catch (_) { return new Set(); }
  }
  function saveRead(set) {
    try { localStorage.setItem(READ_KEY, JSON.stringify(Array.from(set))); } catch (_) {}
  }

  var read = loadRead();

  function lessonInputs() {
    return Array.prototype.slice.call(
      document.querySelectorAll('input[type="checkbox"][data-lesson]')
    );
  }

  function uniqueIds(inputs) {
    var ids = new Set();
    inputs.forEach(function (input) { ids.add(input.dataset.lesson); });
    return ids;
  }

  function updateProgress() {
    var inputs = lessonInputs();
    var ids = uniqueIds(inputs);
    var total = ids.size;
    var done = 0;
    ids.forEach(function (id) { if (read.has(id)) done++; });
    var pct = total ? Math.round((done / total) * 100) : 0;

    var fill = document.getElementById("progress-fill");
    if (fill) fill.style.width = pct + "%";
    var label = document.getElementById("progress-label");
    if (label) label.textContent = done + " of " + total + " lessons read";
    var top = document.getElementById("progress-text");
    if (top) top.textContent = pct + "%";

    var homeFill = document.getElementById("home-progress-fill");
    if (homeFill) homeFill.style.width = pct + "%";
    var homeText = document.getElementById("home-progress-text");
    if (homeText) homeText.textContent = done + " of " + total + " lessons read";

    document.querySelectorAll("[data-nav-count]").forEach(function (el) {
      var moduleNum = el.dataset.navCount;
      var moduleInputs = inputs.filter(function (input) {
        return input.dataset.module === moduleNum;
      });
      var moduleIds = uniqueIds(moduleInputs);
      var moduleDone = 0;
      moduleIds.forEach(function (id) { if (read.has(id)) moduleDone++; });
      el.textContent = moduleDone + "/" + moduleIds.size;
    });

    document.querySelectorAll("[data-card-module]").forEach(function (card) {
      var moduleNum = card.dataset.cardModule;
      var moduleInputs = inputs.filter(function (input) {
        return input.dataset.module === moduleNum;
      });
      var moduleIds = uniqueIds(moduleInputs);
      var moduleDone = 0;
      moduleIds.forEach(function (id) { if (read.has(id)) moduleDone++; });
      var cardFill = card.querySelector(".card-progress-fill, .module-progress-fill");
      if (cardFill) {
        cardFill.style.width = (moduleIds.size ? Math.round((moduleDone / moduleIds.size) * 100) : 0) + "%";
      }
      var cardText = card.querySelector(".card-progress-text, .module-progress-text");
      if (cardText) cardText.textContent = moduleDone + "/" + moduleIds.size + " read";
    });
  }

  var inputs = lessonInputs();
  inputs.forEach(function (input) {
    input.checked = read.has(input.dataset.lesson);
    input.addEventListener("change", function () {
      if (input.checked) read.add(input.dataset.lesson);
      else read.delete(input.dataset.lesson);
      saveRead(read);
      inputs.forEach(function (other) {
        if (other.dataset.lesson === input.dataset.lesson) other.checked = input.checked;
      });
      updateProgress();
    });
  });
  updateProgress();

  // Theme
  var themeToggle = document.getElementById("theme-toggle");
  function applyTheme(theme) {
    document.documentElement.dataset.theme = theme;
    if (themeToggle) themeToggle.textContent = theme === "dark" ? "☀️" : "🌙";
    try { localStorage.setItem(THEME_KEY, theme); } catch (_) {}
  }
  var savedTheme = null;
  try { savedTheme = localStorage.getItem(THEME_KEY); } catch (_) {}
  if (!savedTheme) {
    savedTheme = (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) ? "dark" : "light";
  }
  applyTheme(savedTheme);
  if (themeToggle) {
    themeToggle.addEventListener("click", function () {
      applyTheme(document.documentElement.dataset.theme === "dark" ? "light" : "dark");
    });
  }

  // Mobile sidebar
  var menuToggle = document.getElementById("menu-toggle");
  var overlay = document.getElementById("sidebar-overlay");
  if (menuToggle) {
    menuToggle.addEventListener("click", function () {
      document.body.classList.toggle("sidebar-open");
    });
  }
  if (overlay) overlay.addEventListener("click", function () {
    document.body.classList.remove("sidebar-open");
  });
  document.querySelectorAll(".sidebar a").forEach(function (link) {
    link.addEventListener("click", function () {
      document.body.classList.remove("sidebar-open");
    });
  });

  // Mark a module as read / unread
  document.querySelectorAll("[data-mark-module]").forEach(function (button) {
    button.addEventListener("click", function () {
      var moduleNum = button.dataset.markModule;
      var moduleInputs = lessonInputs().filter(function (input) {
        return input.dataset.module === moduleNum;
      });
      var ids = uniqueIds(moduleInputs);
      var allDone = true;
      ids.forEach(function (id) { if (!read.has(id)) allDone = false; });
      ids.forEach(function (id) {
        if (allDone) read.delete(id); else read.add(id);
      });
      saveRead(read);
      lessonInputs().forEach(function (input) {
        input.checked = read.has(input.dataset.lesson);
      });
      updateProgress();
      button.textContent = allDone ? "Mark module as read" : "Mark module as unread";
    });
  });

  // Search
  var search = document.getElementById("search");
  var results = document.getElementById("search-results");
  var searchIndex = null;
  var loadingIndex = false;
  var selected = -1;
  var currentResults = [];

  function loadSearchIndex() {
    if (searchIndex) return Promise.resolve(searchIndex);
    if (loadingIndex) {
      return new Promise(function (resolve) {
        var timer = setInterval(function () {
          if (searchIndex) { clearInterval(timer); resolve(searchIndex); }
        }, 60);
      });
    }
    loadingIndex = true;
    return new Promise(function (resolve, reject) {
      var script = document.createElement("script");
      script.src = root + "assets/search-index.js";
      script.onload = function () {
        searchIndex = window.SEARCH_INDEX || [];
        loadingIndex = false;
        resolve(searchIndex);
      };
      script.onerror = function () {
        loadingIndex = false;
        reject(new Error("search index failed to load"));
      };
      document.head.appendChild(script);
    });
  }

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }
  function escapeRegExp(value) {
    return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }
  function highlight(text, terms) {
    var safe = escapeHtml(text);
    terms.forEach(function (term) {
      if (!term) return;
      safe = safe.replace(new RegExp("(" + escapeRegExp(escapeHtml(term)) + ")", "gi"), "<mark>$1</mark>");
    });
    return safe;
  }
  function snippet(text, terms) {
    var lower = text.toLowerCase();
    var positions = terms.map(function (term) { return lower.indexOf(term); })
      .filter(function (pos) { return pos >= 0; });
    var start = positions.length ? Math.max(0, Math.min.apply(null, positions) - 70) : 0;
    var slice = text.slice(start, start + 230);
    if (start > 0) slice = "…" + slice;
    if (start + 230 < text.length) slice += "…";
    return highlight(slice, terms);
  }
  function hideResults() {
    if (results) results.hidden = true;
    selected = -1;
    currentResults = [];
  }
  function renderResults(items, terms) {
    if (!results) return;
    if (!items.length) {
      results.innerHTML = '<div class="search-empty">No lessons found.</div>';
      results.hidden = false;
      return;
    }
    results.innerHTML = items.map(function (item, index) {
      return '<a class="search-result" data-index="' + index + '" href="' + root + item.url + '">' +
        '<div class="search-result-title">' + highlight(item.title, terms) + '</div>' +
        '<div class="search-result-meta">Module ' + item.module + ' · ' + escapeHtml(item.module_title) + '</div>' +
        '<div class="search-result-snippet">' + snippet(item.text, terms) + '</div>' +
        '</a>';
    }).join("");
    results.hidden = false;
    selected = -1;
    currentResults = items;
    results.querySelectorAll(".search-result").forEach(function (link) {
      link.addEventListener("mouseenter", function () {
        selected = Number(link.dataset.index);
        updateSelected();
      });
    });
  }
  function updateSelected() {
    if (!results) return;
    results.querySelectorAll(".search-result").forEach(function (link, index) {
      link.classList.toggle("active", index === selected);
    });
  }
  function runSearch(query) {
    var terms = query.toLowerCase().split(/\s+/).filter(Boolean);
    if (!terms.length) { hideResults(); return; }
    loadSearchIndex().then(function (index) {
      var scored = [];
      index.forEach(function (item) {
        var title = item.title.toLowerCase();
        var tags = (item.tags || []).join(" ").toLowerCase();
        var text = item.text.toLowerCase();
        var all = true;
        var score = 0;
        terms.forEach(function (term) {
          var inTitle = title.indexOf(term) !== -1;
          var inTags = tags.indexOf(term) !== -1;
          var inText = text.indexOf(term) !== -1;
          if (!inTitle && !inTags && !inText) { all = false; return; }
          if (inTitle) score += 100;
          if (inTags) score += 20;
          if (inText) score += 5;
          if (title.indexOf(term) === 0) score += 50;
        });
        if (!all) return;
        if (title.indexOf(query.toLowerCase()) !== -1) score += 200;
        scored.push({ item: item, score: score });
      });
      scored.sort(function (a, b) { return b.score - a.score; });
      renderResults(scored.slice(0, 12).map(function (entry) { return entry.item; }), terms);
    }).catch(function () {
      if (results) {
        results.innerHTML = '<div class="search-empty">Search index could not be loaded.</div>';
        results.hidden = false;
      }
    });
  }

  if (search) {
    var timer = null;
    search.addEventListener("input", function () {
      clearTimeout(timer);
      var value = search.value.trim();
      if (value.length < 2) { hideResults(); return; }
      timer = setTimeout(function () { runSearch(value); }, 130);
    });
    search.addEventListener("focus", function () {
      if (search.value.trim().length >= 2) runSearch(search.value.trim());
    });
    search.addEventListener("keydown", function (event) {
      if (event.key === "Escape") { hideResults(); search.blur(); return; }
      if (!currentResults.length) return;
      if (event.key === "ArrowDown") {
        event.preventDefault();
        selected = Math.min(currentResults.length - 1, selected + 1);
        updateSelected();
      } else if (event.key === "ArrowUp") {
        event.preventDefault();
        selected = Math.max(0, selected - 1);
        updateSelected();
      } else if (event.key === "Enter") {
        event.preventDefault();
        var target = selected >= 0 ? currentResults[selected] : currentResults[0];
        if (target) window.location.href = root + target.url;
      }
    });
    document.addEventListener("click", function (event) {
      if (results && !results.hidden && !results.contains(event.target) && event.target !== search) {
        hideResults();
      }
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "/" && document.activeElement !== search &&
          !/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName)) {
        event.preventDefault();
        search.focus();
      }
    });
  }

  // Active TOC entry
  var tocLinks = Array.prototype.slice.call(
    document.querySelectorAll(".toc a[href^='#']")
  );
  if (tocLinks.length && "IntersectionObserver" in window) {
    var headingMap = {};
    tocLinks.forEach(function (link) {
      var id = link.getAttribute("href").slice(1);
      var heading = document.getElementById(id);
      if (heading) headingMap[id] = link;
    });
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        tocLinks.forEach(function (link) { link.classList.remove("active"); });
        var active = headingMap[entry.target.id];
        if (active) active.classList.add("active");
      });
    }, { rootMargin: "-80px 0px -70% 0px" });
    Object.keys(headingMap).forEach(function (id) {
      var heading = document.getElementById(id);
      if (heading) observer.observe(heading);
    });
  }
})();
"""


# ---------------------------------------------------------------------------
# HTML page rendering
# ---------------------------------------------------------------------------


def load_metadata(study: Path) -> dict[str, Any]:
    path = study / "_meta" / "lessons.json"
    if not path.exists():
        sys.exit(
            f"Metadata not found: {path}\n"
            "Run scripts/extract_articles.py first."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def all_lessons(metadata: dict[str, Any]) -> list[dict[str, Any]]:
    return [lesson for module in metadata["modules"] for lesson in module["lessons"]]


def lesson_href(lesson: dict[str, Any]) -> str:
    return f"lessons/{lesson['id']}-{lesson['slug']}.html"


def sibling_lesson_href(lesson: dict[str, Any]) -> str:
    """Link to a lesson from another page inside the lessons/ directory."""
    return f"{lesson['id']}-{lesson['slug']}.html"


def module_href(module: dict[str, Any]) -> str:
    return f"modules/m{module['num']:02d}.html"


def render_sidebar(
    metadata: dict[str, Any],
    root: str,
    active_lesson: str | None = None,
    active_module: int | None = None,
) -> str:
    modules = metadata["modules"]
    first_with_lessons = next((m["num"] for m in modules if m["lessons"]), None)
    parts = ['<nav class="course-nav" aria-label="Course modules">']
    home_active = " active" if not active_lesson and active_module is None else ""
    parts.append(
        f'<a class="nav-home{home_active}" href="{root}index.html">Course home</a>'
    )
    for module in modules:
        if not module["lessons"]:
            active = " active" if active_module == module["num"] else ""
            parts.append(
                f'<a class="nav-module-single{active}" href="{root}{module_href(module)}">'
                f"{module['num']}. {escape(module['title'])}</a>"
            )
            continue
        open_attr = ""
        if active_module == module["num"]:
            open_attr = " open"
        elif active_module is None and module["num"] == first_with_lessons:
            open_attr = " open"
        parts.append(
            f'<details class="nav-module" data-module="{module["num"]}"{open_attr}>'
        )
        parts.append(
            "<summary>"
            f'<span class="nav-module-title">{module["num"]}. {escape(module["title"])}</span>'
            f'<span class="nav-count" data-nav-count="{module["num"]}">0/{len(module["lessons"])}</span>'
            "</summary>"
        )
        parts.append("<ul>")
        for lesson in module["lessons"]:
            active = " active" if lesson["id"] == active_lesson else ""
            parts.append(
                f'<li class="nav-lesson{active}">'
                f'<label class="nav-check"><input type="checkbox" '
                f'data-lesson="{lesson["id"]}" data-module="{module["num"]}" '
                f'aria-label="Mark {escape(lesson["title"])} as read"></label>'
                f'<a href="{root}{lesson_href(lesson)}">{lesson["num"]} {escape(lesson["title"])}</a>'
                "</li>"
            )
        parts.append("</ul>")
        parts.append("</details>")
    parts.append("</nav>")
    return "\n".join(parts)


def page_shell(
    *,
    title: str,
    content: str,
    metadata: dict[str, Any],
    root: str,
    active_lesson: str | None = None,
    active_module: int | None = None,
    description: str = "",
    body_class: str = "",
) -> str:
    sidebar = render_sidebar(metadata, root, active_lesson, active_module)
    safe_title = escape(title)
    document_title = safe_title if "AI Engineering Course" in title else f"{safe_title} · AI Engineering Course"
    safe_description = escape(description or "")
    return f"""<!DOCTYPE html>
<html lang="en" data-root="{root}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{safe_description}">
<title>{document_title}</title>
<link rel="stylesheet" href="{root}assets/style.css">
<link rel="stylesheet" href="{root}assets/pygments.css">
</head>
<body class="{body_class}">
<a class="skip-link" href="#content">Skip to content</a>
<header class="topbar">
  <button id="menu-toggle" class="icon-btn" type="button" aria-label="Toggle navigation">☰</button>
  <a class="brand" href="{root}index.html">AI Engineering Course</a>
  <div class="search-wrap">
    <input id="search" type="search" placeholder="Search lessons…" autocomplete="off" aria-label="Search lessons">
    <div id="search-results" class="search-results" hidden></div>
  </div>
  <div class="progress-mini" title="Course progress"><span id="progress-text">0%</span></div>
  <button id="theme-toggle" class="icon-btn" type="button" aria-label="Toggle light/dark theme">🌙</button>
</header>
<div class="layout">
  <aside class="sidebar" id="sidebar">
    <div class="progress-box">
      <div class="progress-bar"><span id="progress-fill"></span></div>
      <div class="progress-label" id="progress-label">0 of 0 lessons read</div>
    </div>
    {sidebar}
  </aside>
  <div class="sidebar-overlay" id="sidebar-overlay"></div>
  <div class="content-wrap">
    <main class="content" id="content">
      {content}
    </main>
  </div>
</div>
<script src="{root}assets/app.js"></script>
</body>
</html>
"""


def module_plain_intro(module: dict[str, Any], limit: int = 190) -> str:
    text = plain_text(module.get("intro", ""), limit=4000)
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0] + "…"


def render_home(metadata: dict[str, Any]) -> str:
    modules = metadata["modules"]
    lessons = all_lessons(metadata)
    stats = metadata["stats"]
    total_minutes = stats.get("reading_minutes", 0)
    first_lesson = lessons[0] if lessons else None
    first_href = lesson_href(first_lesson) if first_lesson else "modules/m00.html"
    full_pdf = "../pdf/ai-engineering-course-full.pdf"

    cards = []
    for module in modules:
        lesson_count = len(module["lessons"])
        count_label = f"{lesson_count} lessons" if lesson_count else "Reference"
        intro = module_plain_intro(module)
        progress = ""
        if lesson_count:
            progress = (
                '<div class="card-progress"><span class="card-progress-fill"></span></div>'
                f'<div class="card-progress-text">0/{lesson_count} read</div>'
            )
        cards.append(
            f'<a class="module-card" data-card-module="{module["num"]}" '
            f'href="{module_href(module)}">'
            '<div class="module-card-head">'
            f'<span>Module {module["num"]}</span><span>{count_label}</span>'
            "</div>"
            f'<h2>{escape(module["title"])}</h2>'
            f"<p>{escape(intro)}</p>"
            f"{progress}"
            "</a>"
        )

    return f"""
<section class="hero">
  <p class="kicker">Offline study library</p>
  <h1>AI Engineering Course</h1>
  <p>The full articles behind every lesson, organized by module and ready to read
  offline. Search across the whole course, track what you have finished, and keep
  the Markdown or PDFs for later.</p>
  <div class="hero-actions">
    <a class="btn btn-primary" href="{first_href}">Start learning →</a>
    <a class="btn" href="../pdf/ai-engineering-course-full.pdf">Full-course PDF</a>
    <a class="btn" href="modules/m00.html">Module 0: Must Know</a>
  </div>
  <div class="stats">
    <div class="stat"><div class="value">{len(modules)}</div><div class="label">Modules</div></div>
    <div class="stat"><div class="value">{len(lessons)}</div><div class="label">Lessons</div></div>
    <div class="stat"><div class="value">{total_minutes/60:.1f}h</div><div class="label">Reading time</div></div>
    <div class="stat"><div class="value">{stats.get("images", 0)}</div><div class="label">Diagrams</div></div>
  </div>
  <div class="home-progress">
    <div class="progress-bar"><span id="home-progress-fill"></span></div>
    <div class="progress-label" id="home-progress-text">0 of {len(lessons)} lessons read</div>
  </div>
</section>

<div class="section-title">
  <h2>Modules</h2>
  <span class="hint">Read in order, or jump to a topic</span>
</div>
<section class="module-grid">
  {"".join(cards)}
</section>

<section class="hero" style="margin-top: 8px;">
  <p class="kicker">How to use this library</p>
  <h2 style="margin-top:0; border:0; padding:0;">Three ways to study</h2>
  <p><strong>HTML reader:</strong> full-text search, a table of contents on every
  lesson, and checkboxes that remember your progress in this browser.</p>
  <p><strong>Markdown:</strong> every lesson is a self-contained file under
  <code>study/modules/</code>. Add your own notes directly below the article.</p>
  <p><strong>PDF:</strong> one PDF per module plus a complete book, for printing
  or reading without a browser.</p>
  <p class="progress-label">Content © Outcome School / Amit Shekhar.
  Personal offline study only — <a href="notice.html">usage notice</a>.</p>
</section>
"""


def render_module_page(metadata: dict[str, Any], module: dict[str, Any]) -> str:
    intro_html, toc_html = render_markdown(module.get("intro", ""), add_toc=True)
    lesson_rows = []
    for lesson in module["lessons"]:
        tags = " ".join(
            f'<span class="tag">{escape(tag)}</span>' for tag in lesson.get("tags", [])
        )
        lesson_rows.append(
            "<tr>"
            f'<td><input type="checkbox" data-lesson="{lesson["id"]}" '
            f'data-module="{module["num"]}" aria-label="Mark {escape(lesson["title"])} as read"></td>'
            f'<td><a href="../{lesson_href(lesson)}">{escape(lesson["title"])}</a></td>'
            f'<td class="time">~{lesson["reading_time"]} min</td>'
            f"<td>{tags}</td>"
            f'<td class="source"><a href="{lesson["source"]}" target="_blank" rel="noopener noreferrer">Source</a></td>'
            "</tr>"
        )

    videos = ""
    if module.get("videos"):
        links = " · ".join(
            f'<a href="{video["url"]}" target="_blank" rel="noopener noreferrer">{escape(video["title"])}</a>'
            for video in module["videos"]
        )
        videos = f'<div class="video-links"><strong>Module videos:</strong> {links}</div>'

    lesson_count = len(module["lessons"])
    if lesson_count:
        progress_block = f"""
    <div class="module-progress">
      <div class="module-progress-meta">
        <span>Module progress</span>
        <span class="module-progress-text">0/{lesson_count} read</span>
      </div>
      <div class="module-progress-bar"><span class="module-progress-fill"></span></div>
      <button class="mark-module" type="button" data-mark-module="{module["num"]}">Mark module as read</button>
    </div>"""
        header_attrs = f' data-card-module="{module["num"]}"'
    else:
        progress_block = '<p class="progress-label">Reference module — no numbered lessons.</p>'
        header_attrs = ""

    lessons_section = ""
    if module["lessons"]:
        lessons_section = f"""
<div class="section-title">
  <h2>Lessons</h2>
  <span class="hint">{lesson_count} lessons</span>
</div>
<table class="lesson-table">
  <thead><tr><th></th><th>Lesson</th><th>Time</th><th>Tags</th><th>Source</th></tr></thead>
  <tbody>{"".join(lesson_rows)}</tbody>
</table>"""

    return f"""
<header class="module-header"{header_attrs}>
  <p class="kicker">Module {module["num"]}</p>
  <h1>{escape(module["title"])}</h1>
  {progress_block}
  {videos}
</header>
{toc_html}
{intro_html}
{lessons_section}
"""


def render_lesson_page(
    metadata: dict[str, Any],
    module: dict[str, Any],
    lesson: dict[str, Any],
    markdown_text: str,
    prev_lesson: dict[str, Any] | None,
    next_lesson: dict[str, Any] | None,
) -> str:
    content_html, toc_html = render_markdown(
        strip_lesson_header(markdown_text), add_toc=True
    )
    tags = " ".join(
        f'<span class="tag">{escape(tag)}</span>' for tag in lesson.get("tags", [])
    )
    published = lesson.get("published", "")
    meta_bits = [f"Lesson {lesson['num']}", f"~{lesson['reading_time']} min"]
    if published:
        meta_bits.append(f"Published {published}")
    meta_html = " · ".join(escape(bit) for bit in meta_bits)
    source = lesson.get("source", "")

    videos = ""
    if lesson.get("videos"):
        links = " · ".join(
            f'<a href="{video["url"]}" target="_blank" rel="noopener noreferrer">{escape(video["title"])}</a>'
            for video in lesson["videos"]
        )
        videos = f'<div class="video-links"><strong>Videos:</strong> {links}</div>'

    prev_html = ""
    next_html = ""
    if prev_lesson:
        prev_html = (
            f'<a href="{sibling_lesson_href(prev_lesson)}">'
            '<span class="label">← Previous lesson</span>'
            f'{escape(prev_lesson["num"])} {escape(prev_lesson["title"])}</a>'
        )
    if next_lesson:
        next_html = (
            f'<a class="next" href="{sibling_lesson_href(next_lesson)}">'
            '<span class="label">Next lesson →</span>'
            f'{escape(next_lesson["num"])} {escape(next_lesson["title"])}</a>'
        )
    prev_next = ""
    if prev_html or next_html:
        prev_next = f'<nav class="prev-next" aria-label="Lesson navigation">{prev_html}{next_html}</nav>'

    source_link = (
        f'<a href="{source}" target="_blank" rel="noopener noreferrer">Original article</a>'
        if source
        else ""
    )

    return f"""
<article>
  <header class="lesson-header">
    <p class="breadcrumb">
      <a href="../index.html">Course</a> /
      <a href="../{module_href(module)}">Module {module["num"]}</a> /
      Lesson {lesson["num"]}
    </p>
    <h1>{escape(lesson["title"])}</h1>
    <div class="lesson-meta">
      <span>{meta_html}</span>
      {source_link}
    </div>
    <div class="lesson-tags">{tags}</div>
    <label class="read-toggle">
      <input type="checkbox" data-lesson="{lesson["id"]}" data-module="{module["num"]}">
      Mark as read
    </label>
    {videos}
  </header>
  {toc_html}
  {content_html}
  {prev_next}
  <footer class="footer">
    <p>Personal offline study copy · Content © Outcome School / Amit Shekhar ·
    <a href="../notice.html">usage notice</a>.</p>
    <p>Source: <a href="{source}" target="_blank" rel="noopener noreferrer">{escape(source)}</a></p>
  </footer>
</article>
"""


def render_notice_page(notice_markdown: str) -> str:
    content, _ = render_markdown(notice_markdown, add_toc=False)
    return f"""
<article>
  <p class="breadcrumb"><a href="index.html">Course</a> / Usage notice</p>
  {content}
  <footer class="footer">
    <p><a href="index.html">← Back to the course</a></p>
  </footer>
</article>
"""


# ---------------------------------------------------------------------------
# Print pages and PDFs
# ---------------------------------------------------------------------------


def print_cover(kicker: str, title: str, subtitle: str, meta: str) -> str:
    return f"""
<section class="print-cover">
  <p class="kicker">{escape(kicker)}</p>
  <h1>{escape(title)}</h1>
  <h2>{escape(subtitle)}</h2>
  <p class="meta">{escape(meta)}</p>
  <p class="notice">Personal offline study copy. Content © Outcome School /
  Amit Shekhar. Not for redistribution. See study/NOTICE.md.</p>
</section>
"""


def print_toc(metadata: dict[str, Any], modules: list[dict[str, Any]]) -> str:
    items = ['<section class="print-toc">', "<h1>Contents</h1>", "<ul>"]
    for module in modules:
        items.append(
            f'<li class="module-entry"><a href="#module-{module["num"]}">'
            f'Module {module["num"]}: {escape(module["title"])}</a>'
        )
        if module["lessons"]:
            items.append('<ul class="toc-lessons">')
            for lesson in module["lessons"]:
                items.append(
                    f'<li class="lesson-entry"><a href="#lesson-{lesson["id"]}">'
                    f'{lesson["num"]} {escape(lesson["title"])}</a></li>'
                )
            items.append("</ul>")
        items.append("</li>")
    items.extend(["</ul>", "</section>"])
    return "\n".join(items)


def print_lesson_section(module: dict[str, Any], lesson: dict[str, Any], study: Path) -> str:
    path = study / lesson["file"]
    markdown_text = path.read_text(encoding="utf-8") if path.exists() else ""
    content_html, _ = render_markdown(
        strip_lesson_header(markdown_text), print_mode=True, add_toc=False
    )
    meta = f"Lesson {lesson['num']} · ~{lesson['reading_time']} min"
    if lesson.get("published"):
        meta += f" · Published {lesson['published']}"
    if lesson.get("source"):
        meta += f' · <a href="{lesson["source"]}">{escape(lesson["source"])}</a>'
    return f"""
<section class="print-lesson" id="lesson-{lesson["id"]}">
  <p class="print-lesson-kicker">Lesson {lesson["num"]}</p>
  <h1>{escape(lesson["title"])}</h1>
  <p class="print-lesson-meta">{meta}</p>
  {content_html}
</section>
"""


def print_module_section(module: dict[str, Any], study: Path) -> str:
    intro_html, _ = render_markdown(module.get("intro", ""), print_mode=True, add_toc=False)
    lessons_html = "".join(
        print_lesson_section(module, lesson, study) for lesson in module["lessons"]
    )
    return f"""
<section class="print-module" id="module-{module["num"]}">
  <section class="print-module-title">
    <p class="kicker">Module {module["num"]}</p>
    <h1>{escape(module["title"])}</h1>
    <p class="meta">{len(module["lessons"])} lessons · ~{module.get("intro_reading_time", 0)} min overview</p>
  </section>
  <div class="print-module-intro">{intro_html}</div>
  {lessons_html}
</section>
"""


def print_document(*, title: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<link rel="stylesheet" href="../assets/style.css">
<link rel="stylesheet" href="../assets/print.css">
</head>
<body class="print-body">
<main class="print-document">
{body}
</main>
</body>
</html>
"""


def find_chrome() -> str | None:
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        path = shutil.which(name)
        if path:
            return path
    return None


def html_to_pdf(chrome: str, html_path: Path, pdf_path: Path) -> tuple[bool, str]:
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    commands = [
        [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--no-pdf-header-footer",
            "--virtual-time-budget=10000",
            f"--print-to-pdf={pdf_path}",
            html_path.as_uri(),
        ],
        [
            chrome,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--no-pdf-header-footer",
            "--virtual-time-budget=10000",
            f"--print-to-pdf={pdf_path}",
            html_path.as_uri(),
        ],
    ]
    last_error = ""
    for command in commands:
        try:
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=240,
                text=True,
            )
            if pdf_path.exists() and pdf_path.stat().st_size > 1000:
                return True, ""
            last_error = (result.stderr or result.stdout or "no PDF produced")[-800:]
        except Exception as exc:  # noqa: BLE001 - report and try the next command form
            last_error = repr(exc)
    return False, last_error


# ---------------------------------------------------------------------------
# Main build
# ---------------------------------------------------------------------------


def build(study: Path, *, do_html: bool, do_pdf: bool, chrome: str | None) -> None:
    metadata = load_metadata(study)
    modules = metadata["modules"]
    lessons = all_lessons(metadata)
    html_dir = study / "html"
    assets_dir = html_dir / "assets"
    lessons_dir = html_dir / "lessons"
    modules_dir = html_dir / "modules"
    print_dir = html_dir / "print"
    pdf_dir = study / "pdf"

    build_report = [
        "# Build Report",
        "",
        f"- **Study library:** `{study}`",
        f"- **Modules:** {len(modules)}",
        f"- **Lessons:** {len(lessons)}",
        f"- **HTML built:** {'yes' if do_html else 'no'}",
        f"- **PDF built:** {'yes' if do_pdf else 'no'}",
        "",
    ]

    if do_html:
        for directory in (html_dir, assets_dir, lessons_dir, modules_dir, print_dir):
            directory.mkdir(parents=True, exist_ok=True)

        # Static assets.
        (assets_dir / "style.css").write_text(CSS, encoding="utf-8")
        (assets_dir / "app.js").write_text(JS, encoding="utf-8")
        pygments_css = HtmlFormatter(style="monokai").get_style_defs()
        (assets_dir / "pygments.css").write_text(pygments_css, encoding="utf-8")
        print_css = """
/* Print-only overrides. The main print rules live in style.css. */
.print-body .anchor { display: none; }
.print-body .toc { display: none; }
"""
        (assets_dir / "print.css").write_text(print_css, encoding="utf-8")

        images_src = study / "assets" / "images"
        if images_src.exists():
            shutil.copytree(images_src, assets_dir / "images", dirs_exist_ok=True)

        # Search index as JS so it works when opened directly from file://.
        search_items = []
        for module in modules:
            for lesson in module["lessons"]:
                path = study / lesson["file"]
                text = path.read_text(encoding="utf-8") if path.exists() else ""
                search_items.append(
                    {
                        "id": lesson["id"],
                        "title": lesson["title"],
                        "module": module["num"],
                        "module_title": module["title"],
                        "tags": lesson.get("tags", []),
                        "url": lesson_href(lesson),
                        "text": plain_text(text, limit=12000),
                    }
                )
        search_js = "window.SEARCH_INDEX = " + json.dumps(
            search_items, ensure_ascii=False, separators=(",", ":")
        ) + ";\n"
        (assets_dir / "search-index.js").write_text(search_js, encoding="utf-8")

        # Course home.
        (html_dir / "index.html").write_text(
            page_shell(
                title="AI Engineering Course — Offline Study Library",
                content=render_home(metadata),
                metadata=metadata,
                root="",
                description="Full articles from the AI Engineering Course, organized by module for offline study.",
            ),
            encoding="utf-8",
        )

        # Module pages.
        for module in modules:
            (modules_dir / f"m{module['num']:02d}.html").write_text(
                page_shell(
                    title=f"Module {module['num']}: {module['title']}",
                    content=render_module_page(metadata, module),
                    metadata=metadata,
                    root="../",
                    active_module=module["num"],
                    description=module_plain_intro(module),
                ),
                encoding="utf-8",
            )

        # Lesson pages.
        for index, lesson in enumerate(lessons):
            module_num = lesson.get("module")
            if module_num is None:
                module_num = int(lesson["id"][1:3])
            module = next(m for m in modules if m["num"] == module_num)
            path = study / lesson["file"]
            markdown_text = path.read_text(encoding="utf-8") if path.exists() else ""
            prev_lesson = lessons[index - 1] if index > 0 else None
            next_lesson = lessons[index + 1] if index + 1 < len(lessons) else None
            (lessons_dir / f"{lesson['id']}-{lesson['slug']}.html").write_text(
                page_shell(
                    title=lesson["title"],
                    content=render_lesson_page(
                        metadata, module, lesson, markdown_text, prev_lesson, next_lesson
                    ),
                    metadata=metadata,
                    root="../",
                    active_lesson=lesson["id"],
                    active_module=module["num"],
                    description=plain_text(markdown_text, limit=180),
                ),
                encoding="utf-8",
            )

        # Notice page.
        notice_path = study / "NOTICE.md"
        notice_markdown = notice_path.read_text(encoding="utf-8") if notice_path.exists() else ""
        (html_dir / "notice.html").write_text(
            page_shell(
                title="Copyright and Usage Notice",
                content=render_notice_page(notice_markdown),
                metadata=metadata,
                root="",
                description="Copyright and usage notice for the offline study library.",
            ),
            encoding="utf-8",
        )

        # Print pages.
        for module in modules:
            body = print_cover(
                "AI Engineering Course",
                f"Module {module['num']}",
                module["title"],
                f"{len(module['lessons'])} lessons · Personal offline study copy",
            )
            body += print_toc(metadata, [module])
            body += print_module_section(module, study)
            body += '<p class="print-footer">Personal offline study copy · Content © Outcome School / Amit Shekhar</p>'
            (print_dir / f"m{module['num']:02d}.html").write_text(
                print_document(title=f"Module {module['num']}: {module['title']}", body=body),
                encoding="utf-8",
            )

        full_body = print_cover(
            "AI Engineering Course",
            "The Complete Course",
            "Machine Learning, LLMs, RAG, Agents, Inference, and AI Systems",
            f"{len(modules)} modules · {len(lessons)} lessons · Personal offline study copy",
        )
        full_body += print_toc(metadata, modules)
        full_body += "".join(print_module_section(module, study) for module in modules)
        full_body += '<p class="print-footer">Personal offline study copy · Content © Outcome School / Amit Shekhar</p>'
        (print_dir / "full.html").write_text(
            print_document(title="AI Engineering Course — Complete Book", body=full_body),
            encoding="utf-8",
        )

        build_report.extend(
            [
                "## HTML",
                "",
                f"- Course home: `{html_dir / 'index.html'}`",
                f"- Lesson pages: {len(lessons)}",
                f"- Module pages: {len(modules)}",
                f"- Search index: `{assets_dir / 'search-index.js'}` ({len(search_items)} entries)",
                f"- Images: `{assets_dir / 'images'}`",
                "",
            ]
        )

    if do_pdf:
        pdf_dir.mkdir(parents=True, exist_ok=True)
        if not chrome:
            build_report.extend(
                [
                    "## PDF",
                    "",
                    "No Chromium/Chrome executable found; PDF generation was skipped.",
                    "",
                ]
            )
            print("PDF skipped: no Chromium/Chrome executable found.")
        else:
            build_report.extend(["## PDF", ""])
            jobs = [(print_dir / f"m{module['num']:02d}.html", pdf_dir / f"{module['slug']}.pdf") for module in modules]
            jobs.append((print_dir / "full.html", pdf_dir / "ai-engineering-course-full.pdf"))
            for html_path, pdf_path in jobs:
                print(f"PDF  {pdf_path.name} ...", end=" ", flush=True)
                ok, error = html_to_pdf(chrome, html_path, pdf_path)
                if ok:
                    size = pdf_path.stat().st_size
                    print(f"ok ({size/1_000_000:.1f} MB)")
                    build_report.append(f"- `{pdf_path.name}` — {size/1_000_000:.1f} MB")
                else:
                    print("failed")
                    build_report.append(f"- `{pdf_path.name}` — **failed**: {error}")
            build_report.append("")

    build_report.extend(
        [
            "## Open the reader",
            "",
            f"Open `{html_dir / 'index.html'}` in a browser.",
            "",
            "The HTML reader uses relative links and a JavaScript search index, so it",
            "works directly from the filesystem (`file://`) without a web server.",
            "",
        ]
    )
    (study / "_meta").mkdir(parents=True, exist_ok=True)
    (study / "_meta" / "build-report.md").write_text(
        "\n".join(build_report), encoding="utf-8"
    )

    print("\nBuild complete.")
    print(f"  HTML: {html_dir / 'index.html'}")
    if do_pdf:
        print(f"  PDF:  {pdf_dir}")
    print(f"  Report: {study / '_meta' / 'build-report.md'}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--study",
        type=Path,
        default=DEFAULT_STUDY,
        help="Study library directory (default: <repo>/study).",
    )
    parser.add_argument("--no-html", action="store_true", help="Skip the HTML build.")
    parser.add_argument("--no-pdf", action="store_true", help="Skip PDF generation.")
    parser.add_argument("--pdf-only", action="store_true", help="Only generate PDFs.")
    parser.add_argument(
        "--chrome",
        default=None,
        help="Path to Chrome/Chromium (default: auto-detect).",
    )
    args = parser.parse_args()

    study = args.study.resolve()
    if not study.exists():
        sys.exit(f"Study directory not found: {study}")
    do_html = not args.no_html and not args.pdf_only
    do_pdf = not args.no_pdf
    chrome = args.chrome or find_chrome()
    if do_pdf and not chrome:
        print("Warning: no Chrome/Chromium found; HTML will be built without PDFs.")
        do_pdf = False
    build(study, do_html=do_html, do_pdf=do_pdf, chrome=chrome)


if __name__ == "__main__":
    main()
