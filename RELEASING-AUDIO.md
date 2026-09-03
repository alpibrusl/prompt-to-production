# Publishing the audiobook

The audiobook is a build artifact. It is not committed — `build/` is in
`.gitignore`, and a repository that teaches Chapter 4 should not carry 275 MB of
derived MP3s in its history, where every re-render after a prose edit would add
another permanent copy.

It is published as **GitHub Release assets** instead: outside git history, up to
2 GB per file, versioned by tag, with a stable download URL per chapter.

## Before releasing

The release tags a commit, so the manuscript that produced the audio has to be
*in* that commit. Two things must be true first.

**1. content-kit is pushed.** This book's `Makefile` and CI call
`bookkit check terms`, `bookkit check prose` and `bookkit glossary`. Push the
books before content-kit and every book's CI goes red on a missing command.

**2. The manuscript is committed.** `git status` clean for `chapters/`. If the
prose has moved since the last render, re-render first — `podcastkit generate`
now tracks the text behind each voice line, so only the changed lines cost
anything.

## Render and encode

```bash
make audiobook                                    # sources, from the manuscript
for d in build/audiobook/chapter_*; do
  podcastkit generate -e "$d" && podcastkit assemble -e "$d"
done
```

About 22 minutes for all 17 chapters with Kokoro on an M4 Max, and free.

The chapter MP3s come out at 192 kbps stereo, which is podcastkit's default and
three times bigger than this material needs: the source is mono 24 kHz TTS, so
the extra bitrate and the second channel carry nothing. Re-encode for
distribution — 275 MB becomes 92 MB for identical audio:

```bash
python3 scripts/encode_release.py     # → build/audiobook/release/*.mp3
```

That also writes title/album/artist/track metadata, so the files sort correctly
in a podcast app rather than arriving as seventeen untitled tracks.

## Publish

```bash
gh release create audio-v1 \
  --title "Prompt to Production — audiobook" \
  --notes-file RELEASE-NOTES.md \
  build/audiobook/release/*.mp3
```

Tag the audio separately from the manuscript (`audio-v1`, not `v1`) so a
re-render after an editorial pass does not imply a new edition of the book.
