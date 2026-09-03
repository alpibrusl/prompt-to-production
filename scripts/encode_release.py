# SPDX-License-Identifier: EUPL-1.2
"""Re-encode the finished chapters for distribution.

The source is mono 24 kHz TTS, so podcastkit's 192 kbps stereo carries no extra
information — 64 kbps mono is the same audio at a third of the bytes, which is
what makes a whole-book release practical.
"""

import re
import shutil
import subprocess
from pathlib import Path

import yaml

BOOK = Path(__file__).resolve().parent.parent
SRC = BOOK / "build" / "audiobook"
DEST = SRC / "release"

if DEST.exists():
    shutil.rmtree(DEST)
DEST.mkdir(parents=True)


def slug(title: str) -> str:
    title = re.sub(r"^Chapter \d+ — ", "", title)
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


rows = []
chapters = sorted(SRC.glob("chapter_*"))
for d in chapters:
    n = d.name.removeprefix("chapter_")
    title = yaml.safe_load((d / "episode.yaml").read_text())["title"] or "A Note from the Author"
    src = d / f"{d.name}.mp3"
    out = DEST / f"prompt-to-production-{n}-{slug(title)}.mp3"
    subprocess.run(
        [
            "ffmpeg", "-nostdin", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(src),
            "-ac", "1", "-ar", "24000", "-c:a", "libmp3lame", "-b:a", "64k",
            "-metadata", f"title={title}",
            "-metadata", "album=Prompt to Production",
            "-metadata", "artist=Alfonso Sastre",
            "-metadata", f"track={int(n)}/{len(chapters)}",
            "-metadata", "genre=Audiobook",
            "-metadata", "date=2026",
            str(out),
        ],
        check=True,
    )
    rows.append((out.name, src.stat().st_size, out.stat().st_size))

before = sum(r[1] for r in rows)
after = sum(r[2] for r in rows)
for name, b, a in rows:
    print(f"  {name:<62} {a / 1048576:5.1f} MB")
print(f"\n  {len(rows)} files   {before / 1048576:.0f} MB -> {after / 1048576:.0f} MB")
