# SPDX-License-Identifier: EUPL-1.2
"""Render chapters/*.md into a web-native reader page.

bookkit's own HTML renderer emits a paginated, print-emulating document (fixed
6x9in @page rules, running headers, a table of contents whose page numbers
only resolve under paged media) meant to preview the EPUB/PDF layout. That is
the right tool for proofing the book, and the wrong one for reading it in a
browser. This script renders the same chapter Markdown into an actual web
page instead: a sticky chapter sidebar, dark-mode support and a reading
column sized for a screen rather than a 6x9in page.

Chapter headings come from book.yaml's per-chapter `title` override ("Chapter
N — Title") rather than the manuscript's own H1, matching this book's own
numbering convention. The afterword's title override is deliberately empty,
so it falls back to its own H1 and the "Afterword" label its manuscript
carries in a leading blockquote, rather than being numbered like a chapter.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

import markdown
import yaml

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = Path(__file__).resolve().parent / "reader_template.html"

CHAPTER_PREFIX = re.compile(r"^Chapter\s+\d+\s+—\s+")
LEADING_H1 = re.compile(r"^#\s+(.+?)\s*\n")
LEADING_LABEL = re.compile(r"^\s*>\s*\*\*(.+?)\*\*\s*\n")


def load_chapters(config: dict) -> list[dict]:
    converter = markdown.Markdown(extensions=["extra", "smarty"])
    chapters = []
    last_part = ""
    for number, entry in enumerate(config["chapters"], start=1):
        text = (ROOT / entry["file"]).read_text()

        h1 = LEADING_H1.match(text)
        manuscript_title = h1.group(1).strip() if h1 else entry["file"]
        if h1:
            text = text[h1.end():]

        label_match = LEADING_LABEL.match(text)
        section_label = label_match.group(1).strip() if label_match else None
        if label_match:
            text = text[label_match.end():]

        converter.reset()
        body = converter.convert(text.strip())

        book_title = (entry.get("title") or "").strip()
        part = entry.get("part") or last_part
        last_part = part

        if book_title:
            heading = book_title
            eyebrow = f"{part} · Chapter {number}" if part else f"Chapter {number}"
        else:
            heading = manuscript_title
            eyebrow = section_label or part

        chapters.append(
            {
                "number": number,
                "heading": heading,
                "short_title": CHAPTER_PREFIX.sub("", heading),
                "eyebrow": eyebrow,
                "part": entry.get("part") or "",
                "slug": f"ch{number:02d}",
                "body": body,
            }
        )
    return chapters


def render_sidebar(chapters: list[dict]) -> str:
    items = []
    last_part = None
    for chapter in chapters:
        if chapter["part"] and chapter["part"] != last_part:
            items.append(f'<li class="toc-part">{html.escape(chapter["part"])}</li>')
            last_part = chapter["part"]
        items.append(
            f'<li><a href="#{chapter["slug"]}" data-slug="{chapter["slug"]}">'
            f'<span class="toc-num">{chapter["number"]:02d}</span>'
            f'{html.escape(chapter["short_title"])}</a></li>'
        )
    return "\n".join(items)


def render_chapters(chapters: list[dict]) -> str:
    sections = []
    for i, chapter in enumerate(chapters):
        prev_link = (
            f'<a class="chapter-nav-link prev" href="#{chapters[i - 1]["slug"]}">'
            f'&larr; {html.escape(chapters[i - 1]["short_title"])}</a>'
            if i > 0
            else '<span></span>'
        )
        next_link = (
            f'<a class="chapter-nav-link next" href="#{chapters[i + 1]["slug"]}">'
            f'{html.escape(chapters[i + 1]["short_title"])} &rarr;</a>'
            if i + 1 < len(chapters)
            else '<span></span>'
        )
        eyebrow_html = (
            f'<p class="chapter-eyebrow">{html.escape(chapter["eyebrow"])}</p>\n'
            if chapter["eyebrow"]
            else ""
        )
        sections.append(
            f'<section class="chapter" id="{chapter["slug"]}" data-slug="{chapter["slug"]}">\n'
            f'{eyebrow_html}'
            f'<h1>{html.escape(chapter["heading"])}</h1>\n'
            f'{chapter["body"]}\n'
            f'<nav class="chapter-nav">{prev_link}{next_link}</nav>\n'
            f"</section>"
        )
    return "\n".join(sections)


def main() -> None:
    config = yaml.safe_load((ROOT / "book.yaml").read_text())
    chapters = load_chapters(config)

    out_dir = ROOT / "_site"
    out_dir.mkdir(parents=True, exist_ok=True)

    page = TEMPLATE.read_text()
    page = page.replace("{{REPO}}", "prompt-to-production")
    page = page.replace("{{TITLE}}", html.escape(config["title"]))
    page = page.replace("{{SUBTITLE}}", html.escape(config.get("subtitle", "")))
    page = page.replace("{{AUTHOR}}", html.escape((config.get("author") or {}).get("name") or ""))
    page = page.replace("{{LICENSE}}", html.escape(config["copyright"]["license"]))
    page = page.replace("{{LICENSE_URL}}", html.escape(config["copyright"]["license_url"]))
    page = page.replace("{{SIDEBAR}}", render_sidebar(chapters))
    page = page.replace("{{CHAPTERS}}", render_chapters(chapters))

    (out_dir / "book.html").write_text(page)
    print(f"wrote _site/book.html ({len(chapters)} chapters)")


if __name__ == "__main__":
    main()
