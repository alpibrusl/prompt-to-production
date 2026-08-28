# The manuscript is source. Everything in build/ is derived.
#
# This file is also, deliberately, the smallest honest example of what the book
# describes: one command, same result on any machine, nothing built by hand.

PY := python3
SCRIPTS := scripts

.PHONY: help glossary check build epub pdf html clean all

help:
	@echo "make glossary  regenerate GLOSSARY.md from glossary.yaml"
	@echo "make check     lint the manuscript against the concept ledger"
	@echo "make epub      build the EPUB (implies glossary)"
	@echo "make pdf       build the PDF  (implies glossary)"
	@echo "make html      build a single-file HTML (implies glossary)"
	@echo "make all       check + build all three formats"
	@echo "make clean     remove build artifacts"

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

clean:
	@rm -rf build GLOSSARY.md
	@echo "cleaned"
