---
title: Entrypoints
---

# Entrypoints

This is the canonical source map for the Carpentries/Sandpaper workshop. Edit source Markdown and R Markdown; never hand-edit generated `site/` pages or theme assets.

## Learner and facilitator surfaces

| Source | Responsibility |
| --- | --- |
| `config.yaml` | Navigation: seven chapters, setup, glossary, field reference, reference, extended practice, and an advanced extension. |
| `index.md`, `README.md` | Workshop promise, six-hour sequence, and start links. |
| `episodes/session-1.Rmd` | Overview and endpoint tour, 55 minutes. |
| `episodes/session-2.Rmd` | Human concept graph, 55 minutes. |
| `episodes/session-3.Rmd` | Human dictionary, decomposition, and peer review, 65 minutes. |
| `episodes/session-4.Rmd` | Build the SDP, 40 minutes. |
| `episodes/session-5.Rmd` | Mapping and required human–AI comparison, 70 minutes. |
| `episodes/session-6.Rmd` | Codes and term gaps, 30 minutes. |
| `episodes/session-7.Rmd` | Validation, EML, and test publication, 45 minutes. |
| `learners/setup.md` | Download, project layout, package pins, and optional live AI setup. |
| `learners/glossary.md` | Plain-language concepts and stable first-use anchors. |
| `learners/field-reference.md` | Workshop field guide linked to the canonical SDP specification. |
| `learners/reference.md` | Paths, checkpoints, software boundaries, and `#teaching-record` status. |
| `learners/extended-practice.md` | Five optional same-source labs outside the 360-minute route; the Chapter 2–3 human checkpoint remains required. |
| `learners/advanced.md` | Optional ontology formalization after the six-hour sequence; the canonical page moved from `episodes/bonus-session.Rmd`. |
| `instructors/instructor-notes.md` | Six-hour facilitation and preparation checks. |
| `profiles/learner-profiles.md` | Design needs and success criteria for each audience. |
| `links.md` | Shared external references and workshop-kit download link. |

The source is `nuseds-fraser-coho-2023-2024.csv`, 173 rows and 14 columns. Project root `fraser-coho-workshop/`, dataset ID `fraser-coho-workshop`, table ID `escapement`, and output `output/fraser-coho-workshop-sdp` are fixed across the seven chapters.

## Kit and evidence

- `episodes/files/fraser-coho-workshop/`: canonical kit inputs, worksheets, scripts, recorded AI outputs, and `draft-sdp`, `seeded-sdp`, and `reference-sdp` checkpoints.
- `episodes/files/fraser-coho-workshop.zip`: downloadable archive of that kit, served as `files/fraser-coho-workshop.zip`.
- `learners/reference.md#teaching-record`: the learner-facing status of the public KNB Test Node rehearsal. Replace pending wording only after verifying the actual record and receipt.

The reference is a technical draft pending Bruno and Tom's domain review. Do not turn a passing check or test upload into an approval claim. Keep recorded AI output distinguishable from human-authored teaching material; the required comparison must remain available without accounts, keys, or purchased credits.

## Maintainer scripts

| Script | Responsibility |
| --- | --- |
| `scripts/build-reference.R` | Build the technical reference package from the declared workshop inputs. |
| `scripts/seed-reference.R` | Generate and retain semantic candidate evidence for the reference workflow. |
| `scripts/complete-reference.R` | Apply the documented technical reference metadata and export preparation. |
| `scripts/check-workshop.py` | Check consistency across the source lesson, kit, paths, and identifiers. |
| `scripts/build-workshop-kit.py` | Assemble the downloadable kit from its canonical source artifacts. |
| `scripts/verify-test-record.py` | Verify the test catalog record through anonymous, read-only requests; it does not upload or change access. |

Read each script's inputs and options before running it. Keep its technical results separate from pending domain review and the actual test publication receipt.

## Software and source authority

R setup and the lesson lockfile pin metasalmon **v0.5.0**; Python setup pins metasalmonpy **v0.4.0**. The R-native review queue and metadata setters are not available in this Python release. The Python lane uses the stated alternatives and supplied candidate evidence. Verify the full path against a newly released version before retiring a workaround, and change setup and build pins together.

The [SDP specification](https://github.com/salmon-data-mobilization/smn-data-pkg/blob/main/SPECIFICATION.md) owns format validity; its [field reference](https://github.com/salmon-data-mobilization/smn-data-pkg/blob/main/docs/field-reference.md) owns the full field inventory. Workshop guides explain these sources rather than creating a parallel schema or validator.

## Presentation conventions

Use Sandpaper's native `group-tab` control for software alternatives. Inside it, only `### R`, `### Python`, and `### Spreadsheet` are tab headings, in that order. For a subsection within a lane, use a span such as `[Subsection]{.h4 .d-block role="heading" aria-level="4"}`; another Markdown heading creates another tab.

Varnish/Bootstrap owns colors, spacing, typography, and tab behavior. Do not add page-local CSS or custom tab JavaScript. Inspect rendered pages when changing headings, tables, diagrams, or download links.

Known theme limitation: with Sandpaper 0.20.2 and Varnish 1.1.1, the fixed “Search the All In One page” button overlaps the lesson title at a 560-pixel viewport, even with the shortened workshop title. The installed theme exposes no lesson-level search-label or global stylesheet override. Keep the canonical theme and recheck this limitation after a Varnish upgrade; retire this note when the header fits at narrow widths.

## Checks

From the repository root, run the workshop consistency check and the Sandpaper checks:

```bash
python3 scripts/check-workshop.py
Rscript --vanilla -e 'sandpaper::check_lesson()'
Rscript --vanilla -e 'sandpaper::build_lesson(rebuild = TRUE, preview = FALSE)'
git diff --check
```

The rendered site is `site/docs/`. `check_lesson()` checks lesson structure; inspect the built pages and local links as well. Sandpaper places setup inside `index.html#setup`, renders glossary and reference pages at the site root, and rewrites links to Markdown files as HTML links. Downloadable Markdown references therefore need matching HTML companions or another explicitly supported download route.

The consistency script checks the lesson/kit contract; it does not replace running the literal R/Python build, validating the generated package and EML, or verifying the actual test catalog record. Technical checks do not supply domain review.

## Site deployment

`.github/workflows/sandpaper-main.yaml` builds and deploys on a push to `main` or `master`, or a manual workflow run. It provisions R 4.4.2, Pandoc, and the lesson dependencies, then runs `sandpaper:::ci_deploy(reset = reset)`. A successful local build is evidence about the local toolchain; inspect the workflow outcome before claiming the published site is current.
