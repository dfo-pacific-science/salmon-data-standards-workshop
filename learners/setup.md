---
title: Setup
---

## What you will be ready to do

The common biologist pathway starts with ordinary tables and prepares the materials needed for FAIR publication: a reviewed Salmon Data Package (SDP), a validated EML 2.2 metadata file, and a preview of the exact objects that `metasalmon` or `metasalmonpy` would upload to the Knowledge Network for Biocomplexity (KNB). Learners whose roles go further can also prepare shared-term proposals or plan an organizational vocabulary or ontology with mappings to the Salmon Domain Ontology. A live catalog upload is available only to participants who have the required credentials and authority to redistribute the data.

## What to bring

Bring a laptop and choose an R, Python, or spreadsheet lane. **You do not need to bring or prepare your own dataset.** Everyone follows the included `nuseds-fraser-coho-sample.csv`: the 30-row, 17-column NuSEDS Fraser Coho teaching sample with selected years from 1996–2024. We use this same table for structure, context, semantic review, code lists, EML, and the catalog dry run.

Session 2 copies the sample CSV and its bundled source dictionary from the installed package into `raw_data/`. Spreadsheet participants receive those identical two source files and a generated SDP folder from the facilitator. The facilitator also supplies source notes and staged copies of the same package for later checkpoints. This workshop does not switch to the separate 173-row, 2023–2024 example.

Near the end, **Session 7 is an optional bring-your-own-dataset activity**. If you want to try it, bring a small salmon-related dataset you are allowed to discuss, together with any codebook, methods, or caveat notes. Supported inputs are one rectangular CSV, several related CSV tables, or an Excel workbook with rectangular sheets. Keep these optional files separate under `raw_data/own-data/`.

For that optional activity, prepare tidy tables: one header row, variables in columns, observations in rows, and values in cells, following [Wickham's tidy-data formulation](https://doi.org/10.18637/jss.v059.i10). Remove presentation features such as merged cells, repeated headers, and subtotals from the working copy; retain the original source separately. NetCDF, rasters, and other multidimensional formats need a format-specific workflow and are outside this workshop's tabular scope.

If you have no suitable data, use Session 7 to make a transfer plan from the Fraser Coho example. Bringing your own data is never a prerequisite for the core workshop.

## Prepare the project folder before the demo

Create a project folder named something like `salmon-data-workshop`. R users should create or open an RStudio Project in that folder. Python and spreadsheet users can use the same layout.

Create these subfolders before the package demo:

```text
salmon-data-workshop/
  salmon-data-workshop.Rproj  # R users
  raw_data/                   # unchanged input data and context files
  scripts/                    # reproducible R or Python build scripts
  output/                     # generated Salmon Data Packages
```

From R, you can create the folders with:

```r
# Run these commands from the open RStudio Project root.
dir.create("raw_data", showWarnings = FALSE)
dir.create("scripts", showWarnings = FALSE)
dir.create("output", showWarnings = FALSE)
```

During Session 2, copy the bundled Fraser Coho CSV and source dictionary into `raw_data/` and leave those inputs unchanged while building the package. R users will put the reproducible build in `scripts/build_sdp.R`; Python users will use `scripts/build_sdp.py`. Spreadsheet users do not need a build script. The shared output folder is `output/fraser-coho-example-sdp`. Do not put source files directly inside a generated package. Keep optional own-data work in `raw_data/own-data/`, `scripts/build_own_sdp.R` or `scripts/build_own_sdp.py`, and `output/my-salmon-sdp`.

## Software options

Choose the R, Python, or spreadsheet lane that fits how you work. Code-driven activities include examples in both R and Python, with language-specific subsections where the commands differ. Spreadsheet-specific subsections show how to review and edit the same standard package files without code. All three lanes use the same project layout and Salmon Data Package structure, so you can stay with one lane while still following the shared discussion.

### R/metasalmon path

Required:

- R 4.3 or newer;
- RStudio, Positron, or another R editor; and
- the `remotes`, `readr`, `dplyr`, `purrr`, `readxl`, and `metasalmon` packages.

Install the release this lesson is written against, `v0.5.0`, before the workshop:

```r
install.packages(c("remotes", "readr", "dplyr", "purrr", "readxl"))
remotes::install_github("salmon-data-mobilization/metasalmon@v0.5.0")

packageVersion("metasalmon")
```

`packageVersion("metasalmon")` should report `0.5.0`. Install the pinned tag rather than the default branch: `v0.5.0` is the same release recorded in this lesson's own `renv.lock`, so the code you run locally is the code the lesson site was built with. An unpinned install tracks whatever has landed on `main` since, which is how a lesson and a learner quietly stop agreeing.

`v0.5.0` is the release that added the R-native review and editing flow Session 4 teaches — `review_semantics()`, `accept_suggestion()`, `reject_suggestion()`, `apply_sdp_semantics()`, `review_metadata()` and the `set_sdp_*()` setters. An earlier metasalmon will load, and Session 4 will not run.

Facilitators should review the [metasalmon changelog][metasalmon-changelog] when preparing to teach, and bump both the tag above and the lockfile together when the workshop moves to a newer release.

For validated EML export, also install:

```r
install.packages(c("emld", "jsonvalidate"))
```

The credential-free KNB dry run does not need a DataONE login. For a live KNB upload, also install the publication packages and the password-prompt helper used in Session 6:

```r
install.packages(c("dataone", "datapack", "XML", "rstudioapi"))
```

A live upload also needs an ORCID-authenticated short-lived DataONE token and explicit publication authority. Do not store the token in a script, project file, YAML file, or shell history.

Optional:

- An LLM provider key only if you want to try optional LLM-assisted semantic review. The basic quickstart and EML export do not require an LLM.

LLM review is strictly opt-in. Context supplied through `llm_context_files` must be a character vector of existing local file paths, and it does not trigger an LLM call unless `llm_assess = TRUE`. Use only an approved provider and do not send sensitive or restricted material outside an authorized environment.

### Python/metasalmonpy path

`metasalmonpy` is the Python implementation of the `metasalmon` workflow. The packages aim for behavioral parity, with an open catch-up window at the workshop's pinned versions; deliberate, language-idiomatic differences are documented in the [parity guide][metasalmonpy-parity]. Use the Python examples anywhere the workshop presents a Python lane.

**The two lanes are pinned to different releases right now, and that is deliberate.** metasalmon is at `v0.5.0` and metasalmonpy is at `v0.4.0`: the R-native review flow Session 4 teaches has not been ported to Python yet. Pinning the Python lane to its own newest release fixes *reproducibility* — you and the lesson site run the same code — and does not close that gap. Session 4 says where its Python lane is empty and shows a `pandas` read of `semantic_suggestions.csv` instead.

Required:

- Python 3.9 or newer; and
- a terminal, notebook, or Python editor.

Create an environment and install the pinned release directly from GitHub (no Git installation required). The releases carry no wheel assets, so the tag tarball is the pinned artifact:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install \
  "metasalmonpy @ https://github.com/salmon-data-mobilization/metasalmonpy/archive/refs/tags/v0.4.0.tar.gz"
```

Confirm the installed release:

```bash
python -c "import metasalmonpy; print(metasalmonpy.__version__)"
```

That should print `0.4.0`. As in the R lane, install the tag rather than the default branch.

The installed package and Python import are both named `metasalmonpy`. See the [metasalmonpy documentation][metasalmonpy-docs]. Validated EML export uses the optional `eml` extra, and KNB publication uses the optional `knb` extra. To prepare for both, replace `metasalmonpy` with `metasalmonpy[knb]` in the install command above; the `knb` extra includes EML support.

If you plan to read an `.xlsx` workbook in the optional Session 7 activity, also install `openpyxl`:

```bash
python -m pip install openpyxl
```

Python semantic seeding on this sample fails with the tested `metasalmonpy 0.4.0` / pandas `3.0.5` combination. Session 3 uses facilitator-supplied R candidate evidence for the same sample; Python creation and metadata editing remain local. Replace that handoff only after a released combination passes the seeded sample rebuild and the workshop pins are updated.

### Spreadsheet path

Required:

- Microsoft Excel, LibreOffice Calc, or another spreadsheet editor that can save CSV files.

Recommended:

- the project folder described above; and
- the facilitator-provided `nuseds-fraser-coho-sample.csv`, `nuseds-fraser-coho-source-dictionary.csv`, and generated `fraser-coho-example-sdp` folder.

Place the input CSV and source dictionary under `raw_data/`, and the generated package under `output/`. Open its canonical metadata CSVs directly in your spreadsheet editor. The facilitator supplies seeded, reviewed, and EML-ready checkpoints from the same sample as needed, so your discussion and review exercises follow the same data as the code lanes. The [blank SDP CSV template][sdp-template] is an optional reference for the later own-data activity.

## Pre-workshop reading

Read these only if you have time:

1. Salmon Data Package specification: [normative rules][sdp-specification] and [field definitions and accepted values][sdp-field-reference]
2. The shared Fraser Coho sample and code-generated quickstart in Session 2
3. metasalmon quickstart: [create and review a package][metasalmon-quickstart]
4. metasalmon post-review workflow: [validate, export EML, and preview KNB publication][metasalmon-eml-workflow]
5. metasalmonpy quickstart: [create and review the same core package structure in Python][metasalmonpy-docs]
6. Optional for ontology maintainers: [Salmon Domain Ontology conventions][sdo-conventions]

You do not need to read ontology documentation before attending. Session 1 explains the term in plain language before the workshop uses it.

## Setup check

Before the demo, confirm that:

- the project is open at `salmon-data-workshop/`;
- `raw_data/`, `scripts/`, and `output/` exist;
- you can access the bundled Fraser Coho sample through your installed package, or have the facilitator-provided sample and source notes ready for Session 2;
- R or Python users have a place for `scripts/build_sdp.R` or `scripts/build_sdp.py`;
- R users can load `metasalmon` with `library(metasalmon)`, and `packageVersion("metasalmon")` reports `0.5.0`;
- Python users can import `metasalmonpy`, and `metasalmonpy.__version__` reports `0.4.0`; and
- spreadsheet users can open the facilitator-generated Fraser Coho SDP metadata CSVs in their editor.

If your organization restricts software installation, use the spreadsheet lane for the package-structure and metadata-review activities.
