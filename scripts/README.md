# Study library scripts

These scripts turn the course README into a separate, offline study library in
`study/`, with the **full articles** behind every lesson (not just the README
summaries), local images, a searchable HTML reader, and PDFs.

The downloaded articles remain the copyright of Outcome School / Amit Shekhar.
They are for personal offline study only. See `study/NOTICE.md`.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r scripts/requirements.txt
```

If you prefer not to use a virtual environment, install the packages with
`python3 -m pip install --user -r scripts/requirements.txt`.

PDF generation additionally needs a Chromium/Chrome executable. The build
script looks for `google-chrome`, `google-chrome-stable`, `chromium`, or
`chromium-browser` on `PATH`. HTML generation works without it.

## Build everything

```bash
python3 scripts/extract_articles.py
python3 scripts/build_site.py
```

The first command fetches all articles and images and writes the Markdown
library. The second renders the HTML reader and PDFs.

## Common options

### Extract only part of the course

```bash
# First five lessons, useful for a quick test
python3 scripts/extract_articles.py --limit 5

# One module
python3 scripts/extract_articles.py --module 3

# Keep remote image URLs instead of downloading images
python3 scripts/extract_articles.py --no-images

# Reuse HTML you saved earlier (file names look like 01-1-1-machine-learning.html)
python3 scripts/extract_articles.py --raw-dir /path/to/raw-html
```

Extraction is safe to re-run. Existing image files are reused; lessons are
rewritten from the current articles.

### Build HTML only, or PDFs only

```bash
python3 scripts/build_site.py --no-pdf
python3 scripts/build_site.py --pdf-only
```

If Chrome is installed somewhere unusual, pass it explicitly:

```bash
python3 scripts/build_site.py --chrome /usr/bin/google-chrome
```

To rebuild a test library in another directory:

```bash
python3 scripts/extract_articles.py --output /tmp/study-test
python3 scripts/build_site.py --study /tmp/study-test
```

## Output

```text
study/
├── README.md                 course index and module table
├── NOTICE.md                 copyright and usage notice
├── modules/                  Markdown lessons grouped by module
│   ├── 00-must-know/
│   ├── 01-machine-learning-foundations/
│   │   ├── README.md
│   │   ├── 01-01-what-is-machine-learning.md
│   │   └── ...
│   └── ...
├── assets/images/            downloaded article images, per lesson
├── html/                     browsable reader
│   ├── index.html            start here
│   ├── lessons/              one HTML page per lesson
│   ├── modules/              module overview pages
│   ├── print/                print layouts used for PDFs
│   └── assets/               CSS, JS, search index, copied images
├── pdf/
│   ├── 01-machine-learning-foundations.pdf
│   ├── ...
│   └── ai-engineering-course-full.pdf
└── _meta/
    ├── lessons.json          machine-readable lesson metadata
    ├── scrape-report.md      per-lesson fetch status
    └── build-report.md       HTML/PDF build report
```

Open `study/html/index.html` directly in a browser. It works over `file://`;
no web server is required. Reading progress is stored in the browser's
`localStorage`.

## How the extraction works

1. **Parse the README** — module headings (`## Module N:`), lesson headings
   (`### N.N Title`), the "Let's get started" blog link, lesson videos, and
   module-level "Videos and more resources" blocks.
2. **Fetch each article** — concurrent requests with retries and a browser user
   agent. A failed article gets a clearly marked summary from the README instead
   of disappearing from the library.
3. **Clean the article** — keep the `article .prose` body, remove the repeated
   author intro, program promotions, newsletter callout, final author bio, and
   social/share lines. Preserve headings, lists, tables, code blocks,
   blockquotes, FAQs, and diagrams.
4. **Download images** — store them under
   `study/assets/images/<lesson-stem>/` and rewrite the Markdown image paths.
   Failed downloads keep the original remote URL.
5. **Write the library** — per-lesson front matter, module indexes, the master
   index, `NOTICE.md`, `lessons.json`, and a scrape report.

## How the site build works

- Markdown is rendered with `markdown-it-py`; code fences are highlighted with
  Pygments.
- The search index is written as `study/html/assets/search-index.js` rather than
  JSON, so full-text search works when the page is opened from `file://`
  (browsers block `fetch()` for local JSON files).
- Every lesson has a generated table of contents. The reader has a dark mode,
  course progress checkboxes, module progress, previous/next navigation, and
  keyboard search (`/`).
- PDFs are produced by headless Chromium from the print pages under
  `study/html/print/`. Each lesson starts on a new page; images, code blocks,
  tables, and blockquotes avoid page breaks.

## Troubleshooting

**`markdownify is required`** — install the dependencies (see Setup).

**Some lessons are marked `summary`** — the article page could not be fetched or
parsed. Check `study/_meta/scrape-report.md` for the error and the original URL.
Re-run extraction later; the site can be temporarily slow.

**PDFs are missing** — install Chromium/Chrome or pass `--chrome`. You can still
use the complete HTML reader and Markdown files.

**Search says the index could not be loaded** — make sure
`study/html/assets/search-index.js` exists. Re-run
`python3 scripts/build_site.py --no-pdf`.

**Images do not show in Markdown** — open the lesson from the `study/` root so
the relative `../../assets/images/...` paths resolve, or use the HTML reader.
