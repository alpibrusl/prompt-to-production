# SPDX-License-Identifier: EUPL-1.2
# The manuscript is source. Everything in build/ is derived.
#
# This file is also, deliberately, the smallest honest example of what the book
# describes: one command, same result on any machine, nothing built by hand.

PY := python3
SCRIPTS := scripts

.PHONY: help glossary check build epub pdf html audiobook clean all cohort-check cohort-build

help:
	@echo "make glossary      regenerate GLOSSARY.md from glossary.yaml"
	@echo "make check         lint the manuscript against the concept ledger"
	@echo "make epub          build the EPUB (implies glossary)"
	@echo "make pdf           build the PDF  (implies glossary)"
	@echo "make html          build a single-file HTML (implies glossary)"
	@echo "make all           check + build all three formats"
	@echo "make cohort-check  lint the cohort curriculum against this book's chapters"
	@echo "make cohort-build  build the cohort student handout + facilitator guide"
	@echo "make clean         remove build artifacts"

glossary:
	@$(PY) $(SCRIPTS)/build_glossary.py

check:
	@$(PY) $(SCRIPTS)/check_terms.py

epub: glossary
	@bookkit build -f epub

pdf: glossary
	@bookkit build -f pdf

html: glossary
	@bookkit build -f html

build: epub

all: check epub html

# One podcastkit episode per chapter: script.json (the narration, chunked for
# TTS) + episode.yaml (the voice cast). This is the *source* an audio renderer
# consumes — rendering it to MP3 is podcastkit's job and needs a TTS backend.
audiobook:
	@bookkit audiobook -b . -d build/audiobook
	@echo "next: podcastkit generate -e build/audiobook/chapter_01 && podcastkit assemble -e build/audiobook/chapter_01"

# bookkit returns 9 for a dry run by its own exit-code convention, which make
# would otherwise treat as failure. 9 is the success case for this target.
audiobook-plan:
	@bookkit audiobook -b . --dry-run || [ $$? -eq 9 ]

clean:
	@rm -rf build GLOSSARY.md cohort/build
	@echo "cleaned"

# The cohort curriculum -- see cohort/README.md. Needs cohortkit:
# pip install "cohortkit @ git+https://github.com/alpibrusl/cohort-kit@main"
cohort-check:
	@cohortkit check cohort --book-path .

cohort-build:
	@cohortkit build cohort --out cohort/build --book-path .
