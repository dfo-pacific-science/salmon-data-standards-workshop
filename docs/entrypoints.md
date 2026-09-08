---
title: Entrypoints
---

# Entrypoints

This repository is a Carpentries/Sandpaper lesson for the Salmon Data Standards Workshop.

## Main lesson surfaces

- `config.yaml`: lesson title, navigation, and visible episode order.
- `index.md`: site landing text.
- `README.md`: repository overview and current workshop promise.
- `episodes/`: learner-facing sessions.
- `learners/setup.md`: setup and prerequisite guidance.
- `learners/reference.md`: glossary and decision aids.
- `instructors/instructor-notes.md`: one-hour and full-day delivery notes.
- `profiles/learner-profiles.md`: target learner personas.

## Software lanes

- R instructions pin `metasalmon` to the **`v0.5.0`** release tag, and `renv/profiles/lesson-requirements/renv.lock` pins the same release, so a learner's install and the lesson build are the same package. Bump the two together — `learners/setup.md` and the lockfile — whenever an episode starts teaching a newer function. The build-log note `episodes/session-4.Rmd` used to emit when the pin was behind what it taught has been removed; the pin is no longer behind, and that was the condition the note named for its own retirement.
- Python instructions pin `metasalmonpy` to the **`v0.4.0`** release tag tarball (its releases carry no wheel assets). **The two lanes are deliberately on different numbers**: the R-native review flow `episodes/session-4.Rmd` teaches shipped in metasalmon 0.5.0 and has not been ported to Python, so that episode's Python lane is empty and says so. Pinning fixes reproducibility on both lanes; only the port closes the capability gap.
- Spreadsheet instructions use facilitator-generated SDP CSVs from the same bundled Fraser Coho sample and appear separately where no code is required.
- `metasalmon` and `metasalmonpy` aim for behavioral parity; the pinned versions retain the review gap above, and deliberate language differences belong in the upstream parity guide.

Python semantic seeding on this sample fails with the tested `metasalmonpy 0.4.0` / pandas `3.0.5` combination. Session 3 uses facilitator-supplied R candidate evidence for the same sample; Python creation and metadata editing remain local. Replace that handoff only after a released combination passes the seeded sample rebuild and the workshop pins are updated.

## Current episode ladder

1. `episodes/session-1.Rmd`: introduce the tiered end goals—FAIR publication, shared-term contribution, and organizational semantic-stewardship planning—plus the salmon data integration system, its SDP and software components, bounded contexts, bridge mappings, and the SDP-to-EML publication direction.
2. `episodes/session-2.Rmd`: copy the bundled 30-row `nuseds-fraser-coho-sample.csv` and source dictionary into `raw_data/`; generate or open `output/fraser-coho-example-sdp` in the selected lane and inspect its structure.
3. `episodes/session-3.Rmd`: keep the same sample in a reproducible `scripts/build_sdp.R` or `.py`, read source notes, write `raw_data/fraser-coho-context.md`, seed semantic candidates, and preserve review decisions across reruns.
4. `episodes/session-4.Rmd`: use the shared NuSEDS Fraser Coho example to run metasalmon's R-native semantic review — `review_semantics()` prints the decision call, the learner pastes it into the build script, and `apply_sdp_semantics()` writes it — covering one measurement IRI, one I-ADOPT decomposition, one unit, one statistical modifier, one table observation-unit IRI, and one deliberate rejection, with optional bundle-aware LLM review named as a separate opt-in.
5. `episodes/session-5.Rmd`: review Fraser Coho code lists, SKOS, and local vocabulary using the same `escapement` table.
6. `episodes/session-6.Rmd`: route sample term gaps; write validated EML from a reviewed checkpoint of the same data; preview KNB publication with a dry run; and create a later version without discarding reviewed metadata.
7. `episodes/session-7.Rmd`: optional 30–45-minute transfer to learner-owned tabular data, with separate `raw_data/own-data/`, `scripts/build_own_sdp.R` or `.py`, and `output/my-salmon-sdp`; learners without data make a transfer plan.
8. `episodes/bonus-session.Rmd`: optional concept mapping extension grounded in the shared sample.

## Styling and presentation

- **Canonical styling system:** author semantic Markdown in Sandpaper and use the global CSS and Bootstrap design tokens supplied by the Varnish theme. Sandpaper's native `group-tab` fenced div is the canonical control for synchronized R, Python, and Spreadsheet alternatives.
- **Style entry pattern:** inside every `group-tab`, use third-level headings in the consistent order `### R`, `### Python`, and `### Spreadsheet`. Sandpaper preserves that heading level and Varnish's existing `h3.tab-header` rule supplies the smaller responsive label size. A tab group shows one software lane at a time.
- **Subsections inside tabs:** Sandpaper converts every Markdown heading inside a `group-tab` into another tab button. Use an ordinary Markdown span with the theme's Bootstrap heading and display classes plus an accessible heading role (for example, `[Subsection]{.h4 .d-block role="heading" aria-level="4"}`) for a visually prominent subsection that must remain inside one software lane.
- **Tokens:** this repository defines no custom design tokens. Colors, spacing, typography, responsive breakpoints, and tab behavior come from Varnish/Bootstrap. Theme assets under `site/docs/assets/` are generated build output and must not be edited.
- **Inline-style policy:** do not add inline CSS, page-local `<style>` elements, template overrides, or parallel JavaScript for language selection. Prefer supported Sandpaper structure and existing Varnish rules; introduce a repository-wide stylesheet only if a future requirement cannot be expressed through those native patterns.
- Edit learner source under `episodes/`, `learners/`, and `index.md`; never hand-edit generated files under `site/`.

## Upstream workflow sources

- `metasalmon`: <https://github.com/salmon-data-mobilization/metasalmon>
- `metasalmonpy` repository: <https://github.com/salmon-data-mobilization/metasalmonpy>
- R/Python parity contract: <https://salmon-data-mobilization.github.io/metasalmonpy/guides/parity.html>
- Salmon Data Package specification: <https://github.com/salmon-data-mobilization/smn-data-pkg/blob/main/SPECIFICATION.md>
- Blank SDP CSV template: <https://github.com/salmon-data-mobilization/smn-data-pkg/tree/main/templates/salmon-data-package-template>
- SDP field reference: <https://github.com/salmon-data-mobilization/smn-data-pkg/blob/main/docs/field-reference.md>
- metasalmon post-review, EML, and KNB workflow: <https://github.com/salmon-data-mobilization/metasalmon/blob/main/vignettes/post-review-package-publication.Rmd>

## Local checks

Use the repo's Sandpaper workflow when R dependencies are available:

```r
sandpaper::check_lesson()
sandpaper::build_lesson()
```

The lesson is documentation-only. It does not run a local app server.
