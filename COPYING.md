# Licensing

This repository holds two different kinds of work, under two different licences.

## The manuscript — CC BY-NC 4.0

`chapters/`, `glossary.yaml`, and the glossary generated from it are licensed
under the Creative Commons Attribution-NonCommercial 4.0 International Licence.

You may share and adapt the text, provided you give appropriate credit and do
not use it commercially. Unlike the previous licence on this manuscript, an
adaptation is not required to carry the same licence.

Full text: <https://creativecommons.org/licenses/by-nc/4.0/legalcode>

## The code — EUPL-1.2

`scripts/`, the `Makefile`, `style.css`, and the CI configuration are licensed
under the **European Union Public Licence v1.2**, the same licence as
[content-kit](https://github.com/alpibrusl/content-kit), the toolchain this book
is built with. The full text is in [`LICENSE`](LICENSE).

The EUPL is an OSI-approved licence: use, study, modify and redistribute freely,
including commercially, provided that derivative works you distribute are shared
under the EUPL or a compatible licence.

Keeping the code under the same licence as content-kit is deliberate — the
scripts here are prototypes of proposals filed against that project
([#9](https://github.com/alpibrusl/content-kit/issues/9),
[#10](https://github.com/alpibrusl/content-kit/issues/10),
[#11](https://github.com/alpibrusl/content-kit/issues/11)), and matching licences
means they can move upstream without a relicensing question.

## Why the split

The two bodies of work want different things. The manuscript is a book: sharing
it is welcome, selling it is not, and adaptations should stay open. The tooling
is software meant to be reused, including commercially, with the copyleft that
keeps improvements available.
