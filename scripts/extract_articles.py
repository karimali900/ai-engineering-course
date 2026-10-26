#!/usr/bin/env python3
"""Build an offline study library from the AI Engineering Course README.

The README is a curriculum index: every lesson links to a full article on
Outcome School.  This script parses the README, downloads each article,
removes the repeated author/promo blocks, downloads the article images, and
writes a structured Markdown library under ``study/``.

The downloaded articles remain the copyright of Outcome School / Amit
Shekhar.  They are stored locally for personal study only; see study/NOTICE.md.

Usage
-----
    python3 scripts/extract_articles.py
    python3 scripts/extract_articles.py --limit 5          # small test run
    python3 scripts/extract_articles.py --module 1         # one module
    python3 scripts/extract_articles.py --no-images        # keep remote images
    python3 scripts/extract_articles.py --raw-dir /path    # reuse saved HTML

Requirements: requests, beautifulsoup4, markdownify, PyYAML
    python3 -m pip install -r scripts/requirements.txt
"""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import random
import re
import shutil
import sys
import threading
import time
import traceback
import unicodedata
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Iterable
from urllib.parse import parse_qs, unquote, urljoin, urlparse

import requests
import yaml
from bs4 import BeautifulSoup

try:
    from markdownify import markdownify as html_to_markdown
except ImportError:  # pragma: no cover - friendly message for a common setup issue
    sys.exit(
        "markdownify is required.\n"
        "Install the extraction dependencies with:\n"
        "    python3 -m pip install -r scripts/requirements.txt"
    )


ROOT = Path(__file__).resolve().parent.parent
README_PATH = ROOT / "README.md"
STUDY_DIR = ROOT / "study"
MODULES_DIR = STUDY_DIR / "modules"
ASSETS_DIR = STUDY_DIR / "assets" / "images"
META_DIR = STUDY_DIR / "_meta"
BASE_URL = "https://outcomeschool.com"
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)

MODULE_RE = re.compile(r"^## Module (\d+): (.+)$", re.M)
LESSON_RE = re.compile(r"^### (\d+)\.(\d+) (.+)$", re.M)
BLOG_LINK_RE = re.compile(
    r"\[([^\]]+)\]\((https://outcomeschool\.com/blog/[^)]+)\)"
)
VIDEO_LINK_RE = re.compile(
    r"\[([^\]]+)\]\((https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[^)]+)\)"
)
GET_STARTED_RE = re.compile(
    r"Let['’]s get started[:\s]*\[([^\]]+)\]"
    r"\((https://outcomeschool\.com/blog/[^)]+)\)",
    re.I,
)
MODULE_RESOURCES_RE = re.compile(
    r"\*\*Videos and more resources for Module \d+:\*\*"
    r"(.*?)(?=\n---|\n## |\Z)",
    re.S | re.I,
)
MODULE_LESSONS_RE = re.compile(
    r"\*\*Lessons in this module:\*\*.*?(?=\n---|\n## |\Z)",
    re.S | re.I,
)

# Repeated site-wide promotional text.  Matching is case-insensitive and
# substring-based; a matching paragraph/list item is removed as a whole.
PROMO_PATTERNS = (
    "I am Amit Shekhar",
    "I teach AI and Machine Learning at Outcome School",
    "Planning your move into AI?",
    "A quick note for you",
    "Stay updated: Subscribe to our newsletter",
    "You can connect with me on",
    "Follow Outcome School on",
    "Read all of our high-quality blogs here",
    "Amit Shekhar Founder @ Outcome School",
    "check out our AI and Machine Learning Program at Outcome School",
    "we have it all covered in our AI and Machine Learning Program",
    "we have a complete program on it",
    "This AI Engineering Course is completely free to read",
    "AI and Machine Learning Program",
    "Outcome School",
    "paid live program",
    "live classes",
    "This course is free",
    "Do share this blog",
    "spread the knowledge",
)

PROMO_LINE_PATTERNS = (
    r"paid live program",
    r"This course is free\. If you want",
    r"If you want more practical",
    r"If this AI Engineering Course helped you",
    r"Copyright \(C\) \d{4} Outcome School",
)

IMAGE_URL_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
FENCE_RE = re.compile(r"^```", re.M)


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------


def slugify(value: str, max_length: int = 80) -> str:
    """Return a filesystem- and URL-friendly slug."""
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = value.lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    if len(value) > max_length:
        value = value[:max_length].rstrip("-")
    return value or "untitled"


def normalise_space(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def dedupe_videos(videos: Iterable[dict]) -> list[dict]:
    seen: set[str] = set()
    result: list[dict] = []
    for video in videos:
        url = video.get("url", "").strip()
        if not url or url in seen:
            continue
        seen.add(url)
        result.append({"title": normalise_space(video.get("title", "")), "url": url})
    return result


def strip_promo_lines(text: str) -> str:
    """Remove promotional one-liners from module intros."""
    kept = []
    for line in text.splitlines():
        if any(re.search(pattern, line, re.I) for pattern in PROMO_LINE_PATTERNS):
            continue
        kept.append(line)
    text = "\n".join(kept)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def strip_front_matter(text: str) -> str:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[end + 5 :].lstrip("\n")
    return text


def count_words(markdown: str) -> int:
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'’_-]*", markdown))


def reading_minutes(words: int) -> int:
    return max(1, round(words / 200))


# ---------------------------------------------------------------------------
# README parsing
# ---------------------------------------------------------------------------


def parse_readme(readme_path: Path = README_PATH) -> list[dict]:
    text = readme_path.read_text(encoding="utf-8")
    module_matches = list(MODULE_RE.finditer(text))
    if not module_matches:
        raise ValueError(f"No '## Module N:' headings found in {readme_path}")

    modules: list[dict] = []
    for index, match in enumerate(module_matches):
        module_num = int(match.group(1))
        module_title = match.group(2).strip()
        module_start = match.end()
        module_end = (
            module_matches[index + 1].start()
            if index + 1 < len(module_matches)
            else len(text)
        )
        block = text[module_start:module_end]
        lesson_matches = list(LESSON_RE.finditer(block))

        if lesson_matches:
            intro = block[: lesson_matches[0].start()]
        else:
            intro = block

        # Module-level "Videos and more resources" block (kept out of the
        # last lesson's body).
        module_videos: list[dict] = []
        resources_match = MODULE_RESOURCES_RE.search(block)
        if resources_match:
            module_videos.extend(
                {"title": title, "url": url}
                for title, url in VIDEO_LINK_RE.findall(resources_match.group(1))
            )

        intro = MODULE_LESSONS_RE.sub("", intro)
        intro = MODULE_RESOURCES_RE.sub("", intro)
        intro = strip_promo_lines(intro)
        intro = re.split(r"\n## License\s*\n", intro, maxsplit=1)[0].rstrip()
        intro = re.sub(r"^\s*---\s*$", "", intro, flags=re.M).strip()

        # Module 0 has a video embedded directly in its intro.
        for title, url in VIDEO_LINK_RE.findall(intro):
            module_videos.append({"title": title, "url": url})
        module_videos = dedupe_videos(module_videos)

        lessons: list[dict] = []
        for lesson_index, lesson_match in enumerate(lesson_matches):
            major = int(lesson_match.group(1))
            minor = int(lesson_match.group(2))
            lesson_title = lesson_match.group(3).strip()
            lesson_start = lesson_match.end()
            lesson_end = (
                lesson_matches[lesson_index + 1].start()
                if lesson_index + 1 < len(lesson_matches)
                else len(block)
            )
            body = block[lesson_start:lesson_end]
            body = MODULE_RESOURCES_RE.sub("", body)
            body = re.sub(r"^\s*---\s*$", "", body, flags=re.M).strip()
            body = re.sub(r"\n{3,}", "\n\n", body)

            source_match = GET_STARTED_RE.search(body)
            if source_match:
                source = source_match.group(2)
                source_title = source_match.group(1)
            else:
                blog_links = BLOG_LINK_RE.findall(body)
                normalised_title = slugify(lesson_title)
                exact = [
                    (title, url)
                    for title, url in blog_links
                    if slugify(title) == normalised_title
                ]
                if exact:
                    source_title, source = exact[0]
                elif blog_links:
                    source_title, source = blog_links[-1]
                else:
                    source_title, source = "", None

            videos: list[dict] = []
            for line in body.splitlines():
                if "watch the video" in line.lower():
                    videos.extend(
                        {"title": title, "url": url}
                        for title, url in VIDEO_LINK_RE.findall(line)
                    )
            videos = dedupe_videos(videos)

            summary = GET_STARTED_RE.sub("", body)
            summary = re.sub(r"Watch the video:.*", "", summary, flags=re.I)
            summary = re.sub(r"\n{3,}", "\n\n", summary).strip()

            lesson_slug = slugify(lesson_title)
            stem = f"{module_num:02d}-{major:02d}-{minor:02d}-{lesson_slug}"
            lessons.append(
                {
                    "id": f"m{module_num:02d}-l{major:02d}{minor:02d}",
                    "num": f"{major}.{minor}",
                    "major": major,
                    "minor": minor,
                    "title": lesson_title,
                    "slug": lesson_slug,
                    "stem": stem,
                    "source": source,
                    "source_title": source_title,
                    "videos": videos,
                    "summary": summary,
                }
            )

        intro_words = count_words(intro)
        modules.append(
            {
                "num": module_num,
                "title": module_title,
                "slug": f"{module_num:02d}-{slugify(module_title)}",
                "intro": intro,
                "intro_words": intro_words,
                "intro_reading_time": reading_minutes(intro_words),
                "videos": module_videos,
                "lessons": lessons,
            }
        )

    # Make sure file stems are unique within a module.
    for module in modules:
        used: set[str] = set()
        for lesson in module["lessons"]:
            stem = lesson["stem"]
            suffix = 2
            while stem in used:
                stem = f"{lesson['stem']}-{suffix}"
                suffix += 1
            used.add(stem)
            lesson["stem"] = stem
            lesson["file"] = f"modules/{module['slug']}/{stem}.md"
            lesson["html"] = f"html/lessons/{lesson['id']}-{lesson['slug']}.html"

    return modules


# ---------------------------------------------------------------------------
# Article fetching and cleaning
# ---------------------------------------------------------------------------

_thread_local = threading.local()


def get_session() -> requests.Session:
    if not hasattr(_thread_local, "session"):
        session = requests.Session()
        session.headers.update(
            {
                "User-Agent": USER_AGENT,
                "Accept": "text/html,application/xhtml+xml",
                "Accept-Language": "en-US,en;q=0.9",
            }
        )
        _thread_local.session = session
    return _thread_local.session


def fetch_html(url: str, timeout: int = 40, retries: int = 4) -> str:
    last_error: str | None = None
    for attempt in range(retries):
        try:
            response = get_session().get(url, timeout=timeout, allow_redirects=True)
            if response.status_code == 200:
                return response.text
            if response.status_code in (429, 500, 502, 503, 504):
                last_error = f"HTTP {response.status_code}"
                time.sleep((2**attempt) + random.random())
                continue
            raise RuntimeError(f"HTTP {response.status_code}")
        except Exception as exc:  # noqa: BLE001 - retry network errors
            last_error = repr(exc)
            time.sleep((2**attempt) + random.random())
    raise RuntimeError(last_error or "unknown fetch error")


def absolute_image_url(src: str) -> str | None:
    if not src or src.startswith("data:"):
        return None
    if src.startswith("/_next/image"):
        query = parse_qs(urlparse(src).query)
        real = query.get("url", [None])[0]
        if not real:
            return None
        return urljoin(BASE_URL, unquote(real))
    return urljoin(BASE_URL, src)


def code_language(element) -> str:
    code = element.find("code")
    if code:
        for class_name in code.get("class", []):
            if class_name.startswith("language-"):
                return class_name[len("language-") :]
    return ""


def is_promo_text(text: str) -> bool:
    lowered = normalise_space(text).lower()
    if not lowered:
        return False
    if lowered in {"happy learning :)", "happy learning"}:
        return True
    return any(pattern.lower() in lowered for pattern in PROMO_PATTERNS)


def remove_element_and_following(element, stop_markers: tuple[str, ...]) -> None:
    """Remove *element* and its following siblings up to a stop marker."""
    node = element
    while node is not None:
        next_node = node.find_next_sibling()
        text = node.get_text(" ", strip=True)
        node.decompose()
        if any(marker.lower() in text.lower() for marker in stop_markers):
            break
        node = next_node


def clean_article(html: str) -> tuple[str, dict]:
    """Convert an Outcome School article page to clean Markdown."""
    soup = BeautifulSoup(html, "html.parser")
    article = soup.find("article")
    if not article:
        raise ValueError("article element not found")
    prose = article.find("div", class_="prose")
    if not prose:
        raise ValueError("div.prose not found")

    # Metadata from the page header (outside the prose body).
    article_text = article.get_text(" ", strip=True)
    published_match = re.search(
        r"Published on\s+([A-Z][a-z]+ \d{1,2}, \d{4})", article_text
    )
    published = published_match.group(1) if published_match else ""

    tags: list[str] = []
    for heading in article.find_all(["h2", "h3"]):
        if heading.get_text(strip=True).lower() == "tags":
            sibling = heading.find_next_sibling()
            if sibling:
                tags = [
                    link.get_text(strip=True)
                    for link in sibling.find_all("a")
                    if link.get_text(strip=True)
                ]
            break

    article_title_tag = article.find("h1")
    article_title = (
        normalise_space(article_title_tag.get_text(" ", strip=True))
        if article_title_tag
        else ""
    )

    # Real images are often inside <noscript>; keep them, drop the wrapper.
    for noscript in prose.find_all("noscript"):
        noscript.unwrap()
    for tag in prose.find_all(["script", "style", "svg"]):
        tag.decompose()

    # Markdown cannot represent nested emphasis cleanly.
    for tag_name in ("strong", "b", "em", "i"):
        for tag in list(prose.find_all(tag_name)):
            if tag.find(tag_name):
                for inner in tag.find_all(tag_name):
                    inner.unwrap()

    # Remove tags/share sections that occasionally live inside the prose.
    for heading in list(prose.find_all(["h2", "h3"])):
        if heading.get_text(strip=True).lower() == "tags":
            sibling = heading.find_next_sibling()
            heading.decompose()
            if sibling:
                sibling.decompose()

    # Remove the repeated author intro, program promos, newsletter block, and
    # final author bio.  The site uses the same blocks on every article.
    for element in list(prose.find_all(["p", "h2", "h3", "h4", "ul", "li"])):
        if not element.parent:
            continue
        text = normalise_space(element.get_text(" ", strip=True))
        if not text:
            continue

        if text.lower().startswith(("thanks", "that's it for now")):
            node = element
            while node is not None:
                next_node = node.find_next_sibling()
                node.decompose()
                node = next_node
            break

        if not is_promo_text(text):
            continue

        if "planning your move into ai?" in text.lower():
            remove_element_and_following(
                element, ("takes you there", "program at outcome school")
            )
            continue

        if "a quick note for you" in text.lower():
            remove_element_and_following(element, ("get back to the topic",))
            continue

        element.decompose()

    # A second pass catches promos whose wording varies slightly.
    for element in list(prose.find_all(["p", "li"])):
        if not element.parent:
            continue
        text = normalise_space(element.get_text(" ", strip=True))
        if text and is_promo_text(text):
            element.decompose()

    # Absolute links and clean, de-duplicated images.
    for link in prose.find_all("a", href=True):
        link["href"] = urljoin(BASE_URL, link["href"])

    image_urls: list[str] = []
    seen_images: set[str] = set()
    for img in list(prose.find_all("img")):
        src = absolute_image_url(img.get("src", ""))
        if not src or src in seen_images:
            img.decompose()
            continue
        seen_images.add(src)
        image_urls.append(src)
        img["src"] = src
        if not img.get("alt"):
            img["alt"] = "Figure"

    # Drop empty spans/paragraphs left behind by the site's layout wrapper.
    for element in list(prose.find_all(["span", "p"])):
        if not element.get_text(strip=True) and not element.find(["img", "br"]):
            element.decompose()

    markdown = html_to_markdown(
        str(prose),
        heading_style="ATX",
        bullets="-",
        code_language_callback=code_language,
    )

    # Remove any remaining lazy-load placeholders and duplicate images.
    lines: list[str] = []
    seen_image_lines: set[str] = set()
    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("!["):
            match = IMAGE_URL_RE.search(stripped)
            if match:
                url = match.group(1)
                if url.startswith("data:") or url in seen_image_lines:
                    continue
                seen_image_lines.add(url)
        lines.append(line.rstrip())
    markdown = "\n".join(lines)

    markdown = markdown.replace("\xa0", " ")
    markdown = re.sub(r"[ \t]+\n", "\n", markdown)
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)
    markdown = markdown.strip() + "\n"

    metadata = {
        "article_title": article_title,
        "published": published,
        "tags": tags,
        "image_urls": image_urls,
    }
    return markdown, metadata


# ---------------------------------------------------------------------------
# Image downloading
# ---------------------------------------------------------------------------


def safe_image_name(url: str) -> str:
    name = unquote(urlparse(url).path.rsplit("/", 1)[-1]) or "image.png"
    name = re.sub(r"[^A-Za-z0-9._-]+", "-", name).strip("-.")
    if not Path(name).suffix:
        name += ".png"
    return name[:120] or "image.png"


def download_image(url: str, destination_dir: Path) -> tuple[str, int, str | None]:
    """Download one image. Returns (local filename, bytes, error)."""
    destination_dir.mkdir(parents=True, exist_ok=True)
    filename = safe_image_name(url)
    destination = destination_dir / filename
    if destination.exists() and destination.stat().st_size > 0:
        return filename, destination.stat().st_size, None

    suffix = 2
    while destination.exists() and destination.stat().st_size == 0:
        destination.unlink()
        destination = destination_dir / f"{Path(filename).stem}-{suffix}{Path(filename).suffix}"
        suffix += 1

    try:
        response = get_session().get(url, stream=True, timeout=40)
        if response.status_code != 200:
            return filename, 0, f"HTTP {response.status_code}"
        content_type = response.headers.get("Content-Type", "").split(";")[0].strip()
        if content_type and not content_type.startswith("image/"):
            return filename, 0, f"unexpected content type: {content_type}"
        content = response.content
        if not content:
            return filename, 0, "empty response"
        if len(content) > 15 * 1024 * 1024:
            return filename, 0, "image larger than 15 MB"
        if content_type and not Path(filename).suffix:
            extension = mimetypes.guess_extension(content_type) or ".png"
            filename += extension
            destination = destination_dir / filename
        destination.write_bytes(content)
        return filename, len(content), None
    except Exception as exc:  # noqa: BLE001 - report the failure and keep remote URL
        return filename, 0, repr(exc)


# ---------------------------------------------------------------------------
# Writing the library
# ---------------------------------------------------------------------------


def yaml_front_matter(data: dict) -> str:
    dumped = yaml.safe_dump(
        data,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
        width=1000,
    )
    return f"---\n{dumped}---\n"


def render_toc(markdown: str, max_items: int = 40) -> str:
    """Build a small Markdown table of contents from ##/### headings."""
    entries: list[tuple[int, str, str]] = []
    in_code = False
    for line in markdown.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        match = re.match(r"^(##|###)\s+(.+?)\s*$", line)
        if not match:
            continue
        level = len(match.group(1))
        title = re.sub(r"[`*_]", "", match.group(2)).strip()
        anchor = slugify(title)
        entries.append((level, title, anchor))
        if len(entries) >= max_items:
            break
    if len(entries) < 3:
        return ""
    lines = ["## Contents", ""]
    for level, title, anchor in entries:
        indent = "  " * max(0, level - 2)
        lines.append(f"{indent}- [{title}](#{anchor})")
    return "\n".join(lines) + "\n"


@dataclass
class LessonResult:
    module_num: int
    lesson: dict
    markdown: str = ""
    metadata: dict = field(default_factory=dict)
    status: str = "pending"
    error: str | None = None
    chars: int = 0
    words: int = 0
    reading_time: int = 0
    images: int = 0
    downloaded_image_bytes: int = 0
    failed_images: list[str] = field(default_factory=list)

    @property
    def key(self) -> str:
        return f"{self.module_num:02d}.{self.lesson['num']}"


def write_lesson_file(result: LessonResult, module: dict, fetch_date: str) -> str:
    lesson = result.lesson
    content = result.markdown.strip() + "\n"
    words = count_words(content)
    reading_time = reading_minutes(words)

    front = {
        "title": lesson["title"],
        "module": module["num"],
        "module_title": module["title"],
        "lesson": lesson["num"],
        "source": lesson["source"],
        "published": result.metadata.get("published", ""),
        "tags": result.metadata.get("tags", []),
        "videos": lesson["videos"],
        "fetched": fetch_date,
        "words": words,
        "reading_time": reading_time,
        "status": result.status,
    }

    source_line = (
        f"> Source: [Outcome School]({lesson['source']})"
        if lesson["source"]
        else "> Source: Outcome School"
    )
    if front["published"]:
        source_line += f" · Published: {front['published']}"
    source_line += f" · Reading time: ~{reading_time} min"
    if front["tags"]:
        source_line += " · Tags: " + ", ".join(f"`{tag}`" for tag in front["tags"])

    video_lines = "\n".join(
        f"> Video: [{video['title']}]({video['url']})" for video in lesson["videos"]
    )

    body_parts = [
        f"# {lesson['title']}",
        "",
        f"> **Module {module['num']} · Lesson {lesson['num']}**  ",
        source_line,
    ]
    if video_lines:
        body_parts.append(video_lines)
    body_parts.append("")
    if result.status != "full":
        error = result.error or "unknown error"
        body_parts.extend(
            [
                f"> **Note:** The full article could not be fetched ({error}). "
                "The summary below is from the course README.  ",
                f"> [Read the original article]({lesson['source']})",
                "",
                "## Summary from the course README",
                "",
                lesson["summary"],
                "",
                "---",
                "",
            ]
        )
    else:
        body_parts.extend(["---", "", content])

    markdown = yaml_front_matter(front) + "\n".join(body_parts).rstrip() + "\n"
    destination = STUDY_DIR / lesson["file"]
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(markdown, encoding="utf-8")

    result.words = words
    result.reading_time = reading_time
    result.chars = len(markdown)
    result.metadata["reading_time"] = reading_time
    result.metadata["words"] = words
    return content


def write_module_readme(module: dict, results: dict[str, LessonResult], fetch_date: str) -> None:
    module_dir = MODULES_DIR / module["slug"]
    module_dir.mkdir(parents=True, exist_ok=True)
    readme_path = module_dir / "README.md"

    toc = render_toc(module["intro"]) if len(module["intro"]) > 5000 else ""
    lines = [
        f"# Module {module['num']}: {module['title']}",
        "",
        "[← Course index](../../README.md) · "
        f"[HTML module page](../../html/modules/m{module['num']:02d}.html)",
        "",
    ]
    if toc:
        lines.extend([toc, ""])
    lines.extend([module["intro"].strip(), ""])

    if module["videos"] and any(
        video["url"] not in module["intro"] for video in module["videos"]
    ):
        lines.extend(["## Module videos", ""])
        lines.extend(
            f"- [{video['title']}]({video['url']})" for video in module["videos"]
        )
        lines.append("")

    if module["lessons"]:
        lines.extend(
            [
                "## Lessons",
                "",
                "| # | Lesson | Reading time | Source |",
                "|---:|---|---:|---|",
            ]
        )
        for lesson in module["lessons"]:
            result = results.get(lesson["id"])
            reading = f"~{result.reading_time} min" if result else "—"
            status = ""
            if result and result.status != "full":
                status = " *(summary)*"
            lines.append(
                f"| {lesson['num']} | "
                f"[{lesson['title']}]({lesson['stem']}.md){status} | "
                f"{reading} | [Outcome School]({lesson['source']}) |"
            )
        lines.append("")
        lines.extend(
            [
                "---",
                "",
                f"*{len(module['lessons'])} lessons · Fetched {fetch_date}. "
                "For personal offline study only; see [NOTICE.md](../../NOTICE.md).*",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "---",
                "",
                f"*Fetched {fetch_date}. For personal offline study only; "
                "see [NOTICE.md](../../NOTICE.md).*",
                "",
            ]
        )

    readme_path.write_text("\n".join(lines), encoding="utf-8")


def module_stats(module: dict, results: dict[str, LessonResult]) -> tuple[int, int, int, int]:
    lesson_results = [results[l["id"]] for l in module["lessons"] if l["id"] in results]
    words = sum(r.words for r in lesson_results) + module.get("intro_words", 0)
    minutes = sum(r.reading_time for r in lesson_results) + module.get(
        "intro_reading_time", 0
    )
    full = sum(1 for r in lesson_results if r.status == "full")
    summary = len(lesson_results) - full
    return words, minutes, full, summary


def write_master_readme(modules: list[dict], results: dict[str, LessonResult], fetch_date: str) -> None:
    total_lessons = sum(len(m["lessons"]) for m in modules)
    total_words = sum(r.words for r in results.values()) + sum(
        m.get("intro_words", 0) for m in modules
    )
    total_minutes = sum(r.reading_time for r in results.values()) + sum(
        m.get("intro_reading_time", 0) for m in modules
    )
    full = sum(1 for r in results.values() if r.status == "full")
    summary = len(results) - full
    hours = total_minutes / 60

    lines = [
        "# AI Engineering Course — Offline Study Library",
        "",
        "> **The full articles behind every lesson**, organized by the 19 modules of the "
        "AI Engineering Course.  ",
        "> For personal offline study. The articles remain the copyright of "
        "Outcome School / Amit Shekhar — see [NOTICE.md](NOTICE.md).",
        "",
        f"**Fetched:** {fetch_date} · **Modules:** {len(modules)} · "
        f"**Lessons:** {total_lessons} · **Reading time:** ~{hours:.1f} hours",
        "",
        "## Start here",
        "",
        "- **[Open the HTML reader](html/index.html)** — search, reading progress, "
        "dark mode, per-lesson table of contents",
        "- **[Full-course PDF](pdf/ai-engineering-course-full.pdf)** — print-ready book",
        "- **[Module 0: Must Know](modules/00-must-know/README.md)** — the six terms "
        "that come up everywhere",
        "",
        "## Modules",
        "",
        "| # | Module | Lessons | Reading time | Markdown | HTML | PDF |",
        "|---:|---|---:|---:|---|---|---|",
    ]
    for module in modules:
        words, minutes, module_full, module_summary = module_stats(module, results)
        lesson_count = len(module["lessons"])
        count_text = f"{lesson_count}"
        if module_summary:
            count_text += f" ({module_summary} summary)"
        lines.append(
            f"| {module['num']} | {module['title']} | {count_text} | "
            f"~{minutes / 60:.1f} h | "
            f"[Read](modules/{module['slug']}/README.md) | "
            f"[HTML](html/modules/m{module['num']:02d}.html) | "
            f"[PDF](pdf/{module['slug']}.pdf) |"
        )

    lines.extend(
        [
            "",
            "## How to use this library",
            "",
            "1. **Read in order.** The modules build on each other; Module 0 is a short "
            "orientation, then Modules 1–17 go from ML foundations to frontier ideas.",
            "2. **Use the HTML reader for study.** It has a full-text search, a "
            "per-lesson table of contents, and checkboxes that remember what you have "
            "read in your browser.",
            "3. **Annotate the Markdown.** Each lesson is a self-contained `.md` file. "
            "Add your own notes below the article, or keep a separate notes file.",
            "4. **Use the PDFs for offline reading.** Each module has a PDF, and there "
            "is one full-course PDF.",
            "",
            "## Folder map",
            "",
            "```text",
            "study/",
            "├── README.md              # this index",
            "├── NOTICE.md              # copyright and usage notice",
            "├── modules/               # Markdown lessons, grouped by module",
            "├── assets/images/         # downloaded article images",
            "├── html/                  # browsable HTML reader",
            "├── pdf/                   # module PDFs + full book",
            "└── _meta/                 # metadata, scrape report, build report",
            "```",
            "",
            "## Scrape summary",
            "",
            f"- **Full articles:** {full}",
            f"- **README fallbacks:** {summary}",
            f"- **Words:** {total_words:,}",
            f"- **Images:** {sum(r.images for r in results.values())}",
            "",
            "See [_meta/scrape-report.md](_meta/scrape-report.md) for the per-lesson "
            "status.",
            "",
        ]
    )
    (STUDY_DIR / "README.md").write_text("\n".join(lines), encoding="utf-8")


def write_notice(fetch_date: str) -> None:
    notice = f"""# Copyright and Usage Notice

The lesson content in this folder was downloaded from
[Outcome School](https://outcomeschool.com) on {fetch_date} for **personal,
offline study**.

- The articles, diagrams, and images are copyright © Outcome School /
  Amit Shekhar, unless stated otherwise.
- The Apache 2.0 license of the `ai-engineering-course` repository applies to
  that repository's own code and text. It **does not** cover the downloaded
  articles in this folder.
- Do **not** redistribute this folder or its article content. Keep it for your
  own study.
- Every lesson keeps its original source URL for attribution and further
  reading.
- If you want to share an article, share the original link instead of the local
  copy.

The Markdown, HTML, and PDF files here are convenience copies generated from
the public articles. If anything is inaccurate or out of date, the original
article on Outcome School is the source of truth.
"""
    (STUDY_DIR / "NOTICE.md").write_text(notice, encoding="utf-8")


def write_reports(
    modules: list[dict],
    results: dict[str, LessonResult],
    fetch_date: str,
    images_downloaded: int,
    image_bytes: int,
    failed_images: list[tuple[str, str, str]],
    usage_errors: list[str],
) -> None:
    total = len(results)
    full = sum(1 for r in results.values() if r.status == "full")
    summary = total - full
    total_words = sum(r.words for r in results.values())

    lines = [
        "# Scrape Report",
        "",
        f"- **Generated:** {fetch_date}",
        "- **Source:** https://outcomeschool.com/blog/",
        f"- **Modules:** {len(modules)}",
        f"- **Lessons:** {total}",
        f"- **Full articles:** {full}",
        f"- **README fallbacks:** {summary}",
        f"- **Words:** {total_words:,}",
        f"- **Images downloaded:** {images_downloaded} ({image_bytes / 1_000_000:.1f} MB)",
        f"- **Failed images:** {len(failed_images)}",
        "",
        "## Status by lesson",
        "",
        "| Module | Lesson | Title | Status | Words | Images |",
        "|---:|---|---|---|---:|---:|",
    ]
    for module in modules:
        for lesson in module["lessons"]:
            result = results.get(lesson["id"])
            if not result:
                continue
            lines.append(
                f"| {module['num']} | {lesson['num']} | {lesson['title']} | "
                f"{result.status} | {result.words} | {result.images} |"
            )

    if usage_errors:
        lines.extend(["", "## Fetch errors", ""])
        lines.extend(f"- {error}" for error in usage_errors)

    if failed_images:
        lines.extend(["", "## Failed images", ""])
        for lesson_key, url, error in failed_images:
            lines.append(f"- `{lesson_key}` — {url} — {error}")

    lines.extend(
        [
            "",
            "## Cleaning notes",
            "",
            "- Removed the repeated author intro, program promotions, newsletter "
            "callout, final author bio, and social links.",
            "- Preserved headings, body text, lists, tables, code blocks, blockquotes, "
            "FAQ sections, and the article's own diagrams.",
            "- Downloaded article images into `assets/images/<lesson>/`.",
            "- Kept the original source URL in every lesson's front matter and header.",
            "",
        ]
    )
    (META_DIR / "scrape-report.md").write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--limit", type=int, default=0, help="Only process the first N lessons (for testing)."
    )
    parser.add_argument(
        "--module", type=int, default=None, help="Only process one module number."
    )
    parser.add_argument(
        "--workers", type=int, default=6, help="Concurrent article fetches (default: 6)."
    )
    parser.add_argument(
        "--timeout", type=int, default=40, help="HTTP timeout in seconds (default: 40)."
    )
    parser.add_argument(
        "--no-images",
        action="store_true",
        help="Keep remote image URLs instead of downloading images.",
    )
    parser.add_argument(
        "--raw-dir",
        type=Path,
        default=None,
        help="Directory of previously saved raw HTML files (optional).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output directory (default: <repo>/study).",
    )
    args = parser.parse_args()

    global STUDY_DIR, MODULES_DIR, ASSETS_DIR, META_DIR
    if args.output:
        STUDY_DIR = args.output.resolve()
        MODULES_DIR = STUDY_DIR / "modules"
        ASSETS_DIR = STUDY_DIR / "assets" / "images"
        META_DIR = STUDY_DIR / "_meta"

    fetch_date = date.today().isoformat()
    modules = parse_readme()
    if args.module is not None:
        modules = [m for m in modules if m["num"] == args.module]
        if not modules:
            sys.exit(f"No module {args.module} found in README.md")

    all_lessons = [(m, l) for m in modules for l in m["lessons"]]
    if args.limit:
        all_lessons = all_lessons[: args.limit]
        allowed_ids = {l["id"] for _, l in all_lessons}
        for module in modules:
            module["lessons"] = [l for l in module["lessons"] if l["id"] in allowed_ids]
        modules = [m for m in modules if m["lessons"] or m["num"] in (0, 18)]

    print(f"Preparing {len(all_lessons)} lessons from {len(modules)} modules...")
    MODULES_DIR.mkdir(parents=True, exist_ok=True)
    META_DIR.mkdir(parents=True, exist_ok=True)

    def process(item: tuple[dict, dict]) -> LessonResult:
        module, lesson = item
        result = LessonResult(module_num=module["num"], lesson=lesson)
        source = lesson.get("source")
        if not source:
            result.status = "summary"
            result.error = "no source URL in README"
            result.markdown = lesson["summary"]
            return result

        raw_html: str | None = None
        if args.raw_dir:
            prefix = f"{module['num']:02d}-{lesson['major']}-{lesson['minor']}-"
            matches = sorted(args.raw_dir.glob(prefix + "*.html"))
            if matches:
                raw_html = matches[0].read_text(encoding="utf-8")

        try:
            if raw_html is None:
                raw_html = fetch_html(source, timeout=args.timeout)
            markdown, metadata = clean_article(raw_html)
            if len(markdown) < 800:
                raise ValueError(f"cleaned article too short ({len(markdown)} chars)")
            result.markdown = markdown
            result.metadata = metadata
            result.status = "full"
        except Exception as exc:  # noqa: BLE001 - fall back to the README summary
            result.status = "summary"
            result.error = str(exc)
            result.markdown = lesson["summary"]
            result.metadata = {"tags": [], "published": "", "image_urls": []}
            traceback.print_exc(limit=1)
        return result

    results: dict[str, LessonResult] = {}
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
        futures = {executor.submit(process, item): item for item in all_lessons}
        for index, future in enumerate(as_completed(futures), 1):
            result = future.result()
            results[result.lesson["id"]] = result
            print(
                f"[{index:3d}/{len(all_lessons)}] {result.key:<8} "
                f"{result.status:<7} {len(result.markdown):>7,} chars  "
                f"{result.lesson['title'][:64]}",
                flush=True,
            )

    # Download images after the text has been cleaned.  A failed download keeps
    # the original remote URL in the Markdown, so the lesson still works online.
    image_tasks: list[tuple[LessonResult, str, str]] = []
    for result in results.values():
        if result.status != "full" or args.no_images:
            continue
        for url in result.metadata.get("image_urls", []):
            image_tasks.append((result, result.lesson["stem"], url))

    image_map: dict[tuple[str, str], str] = {}
    failed_images: list[tuple[str, str, str]] = []
    image_bytes = 0
    if image_tasks:
        print(f"\nDownloading {len(image_tasks)} images...")
        with ThreadPoolExecutor(max_workers=8) as executor:
            future_map = {
                executor.submit(
                    download_image, url, ASSETS_DIR / stem
                ): (result, stem, url)
                for result, stem, url in image_tasks
            }
            for index, future in enumerate(as_completed(future_map), 1):
                result, stem, url = future_map[future]
                filename, size, error = future.result()
                if error:
                    failed_images.append((result.key, url, error))
                    print(f"  [{index:3d}/{len(image_tasks)}] FAIL {stem}/{filename}: {error}")
                    continue
                image_bytes += size
                image_map[(stem, url)] = f"../../assets/images/{stem}/{filename}"
                print(
                    f"  [{index:3d}/{len(image_tasks)}] ok   {stem}/{filename} "
                    f"({size / 1024:.0f} KB)"
                )

    # Apply local image paths and write the Markdown files.
    for result in results.values():
        if result.status == "full":
            for url in result.metadata.get("image_urls", []):
                local = image_map.get((result.lesson["stem"], url))
                if local:
                    result.markdown = result.markdown.replace(url, local)
            result.images = len(result.metadata.get("image_urls", []))
        write_lesson_file(result, next(m for m in modules if m["num"] == result.module_num), fetch_date)

    # Module indexes, master index, notice, metadata.
    for module in modules:
        write_module_readme(module, results, fetch_date)
    write_master_readme(modules, results, fetch_date)
    write_notice(fetch_date)

    metadata = {
        "generated": fetch_date,
        "source": BASE_URL,
        "stats": {
            "modules": len(modules),
            "lessons": len(results),
            "full": sum(1 for r in results.values() if r.status == "full"),
            "summary": sum(1 for r in results.values() if r.status != "full"),
            "words": sum(r.words for r in results.values()),
            "reading_minutes": sum(r.reading_time for r in results.values()),
            "images": sum(r.images for r in results.values()),
            "image_bytes": image_bytes,
            "failed_images": len(failed_images),
        },
        "modules": [],
    }
    for module in modules:
        module_meta = {
            "num": module["num"],
            "title": module["title"],
            "slug": module["slug"],
            "dir": f"modules/{module['slug']}",
            "readme": f"modules/{module['slug']}/README.md",
            "html": f"html/modules/m{module['num']:02d}.html",
            "pdf": f"pdf/{module['slug']}.pdf",
            "intro": module["intro"],
            "intro_words": module.get("intro_words", 0),
            "intro_reading_time": module.get("intro_reading_time", 0),
            "videos": module["videos"],
            "lessons": [],
        }
        for lesson in module["lessons"]:
            result = results.get(lesson["id"])
            if not result:
                continue
            module_meta["lessons"].append(
                {
                    "id": lesson["id"],
                    "module": module["num"],
                    "module_title": module["title"],
                    "num": lesson["num"],
                    "major": lesson["major"],
                    "minor": lesson["minor"],
                    "title": lesson["title"],
                    "slug": lesson["slug"],
                    "stem": lesson["stem"],
                    "file": lesson["file"],
                    "html": lesson["html"],
                    "source": lesson["source"],
                    "published": result.metadata.get("published", ""),
                    "tags": result.metadata.get("tags", []),
                    "videos": lesson["videos"],
                    "status": result.status,
                    "error": result.error,
                    "chars": result.chars,
                    "words": result.words,
                    "reading_time": result.reading_time,
                    "images": result.images,
                }
            )
        metadata["modules"].append(module_meta)

    (META_DIR / "lessons.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    usage_errors = [f"{r.key}: {r.error}" for r in results.values() if r.error]
    write_reports(
        modules,
        results,
        fetch_date,
        len(image_map),
        image_bytes,
        failed_images,
        usage_errors,
    )

    print("\nDone.")
    print(f"  Markdown: {STUDY_DIR / 'modules'}")
    print(f"  Images:   {ASSETS_DIR}")
    print(f"  Metadata: {META_DIR / 'lessons.json'}")
    print(f"  Index:    {STUDY_DIR / 'README.md'}")
    print(
        f"  Lessons:  {len(results)} "
        f"({sum(1 for r in results.values() if r.status == 'full')} full, "
        f"{sum(1 for r in results.values() if r.status != 'full')} summary)"
    )


if __name__ == "__main__":
    main()
