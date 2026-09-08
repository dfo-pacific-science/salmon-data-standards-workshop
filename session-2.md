---
title: "Create a Draft Salmon Data Package"
teaching: 55
exercises: 40
---

:::::::::::::::::::::::::::::::::::::: questions

- What must I set up before running the demo?
- What will the bundled quickstart data show me?
- What input structures does `create_sdp()` support?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Confirm the project, `raw_data/`, `scripts/`, and `output/` layout, unless you already completed this during setup.
- Run the bundled example unchanged to generate and inspect templates.
- Keep the same Fraser Coho data and package identity through Sessions 2–6.
- Identify supported single-table, multi-table, and workbook inputs.

::::::::::::::::::::::::::::::::::::::::::::::::

## Before the quickstart: confirm the project and folders

If you already created this project and its folders in **Summary and Setup**, skip this section. Otherwise, work from one project root so every path in the lesson is relative and reproducible.

1. R users: in RStudio choose **File > New Project**, then create a new project or open the folder you prepared during setup.
2. Confirm that the working project is `salmon-data-workshop/`; do not call `setwd()` to jump elsewhere.
3. Create the input, script, and output folders before calling `create_sdp()`.

```r
# Run from the open RStudio Project root.
dir.create("raw_data", showWarnings = FALSE)
dir.create("scripts", showWarnings = FALSE)
dir.create("output", showWarnings = FALSE)
```

```text
salmon-data-workshop/
  salmon-data-workshop.Rproj
  raw_data/                   # unchanged data and context inputs
  scripts/                    # build_sdp.R or build_sdp.py
  output/                     # generated package folders
```

Keep the prepared dataset, codebooks, methods, caveats, and other context inputs together under `raw_data/` and do not edit them in place while building a package. R users save the code below as `scripts/build_sdp.R`; Python users use `scripts/build_sdp.py`. Spreadsheet users keep a review log. Session 3 extends that same script.

## One Fraser Coho example throughout the workshop

Everyone uses `nuseds-fraser-coho-sample.csv`: the included 30-row, 17-column NuSEDS Fraser Coho practice table, with analysis years ranging from 1996 to 2024. It stays with us through context capture, semantic review, code lists, EML, and the publication preview. Spreadsheet participants inspect a facilitator-generated package from these same rows.

Keep the source unchanged. This small sample is not a complete Fraser Coho time series; blank spawner estimates are not zeroes. Do not substitute the separate 173-row `nuseds-fraser-coho-2023-2024.csv` example. [Session 7](session-7.Rmd) is the optional bring-your-own-dataset activity after the shared workflow.

## What "draft" means

A draft package is allowed to contain blanks, placeholders, and review markers. The first example has one purpose: generate the package structure and starter metadata so you can inspect it. It is not a finished description of the source dataset and it does not export EML yet.

## Generate or open the prepared quickstart

Choose **R**, **Python**, or **Spreadsheet** below. Your selection is synchronized with the other software choices on this page.

::::::::::::::::::::::::::::::::::::: group-tab

### R

`metasalmon` includes a small NuSEDS-derived practice table. Generate its templates with semantic searching turned off so the first result is fast and local.

```r
library(metasalmon)

# Copy the bundled data and its source dictionary into the project once.
# On a rerun, verify existing copies instead of replacing source inputs.
source_files <- c(
  "nuseds-fraser-coho-sample.csv" = "nuseds-fraser-coho-sample.csv",
  "nuseds-fraser-coho-source-dictionary.csv" = "column_dictionary.csv"
)
for (local_name in names(source_files)) {
  bundled_path <- system.file(
    "extdata", source_files[[local_name]], package = "metasalmon"
  )
  stopifnot(nzchar(bundled_path))
  local_path <- file.path("raw_data", local_name)
  if (file.exists(local_path)) {
    stopifnot(unname(tools::md5sum(local_path)) ==
                unname(tools::md5sum(bundled_path)))
  } else {
    stopifnot(file.copy(bundled_path, local_path, overwrite = FALSE))
  }
}

data_path <- file.path("raw_data", "nuseds-fraser-coho-sample.csv")
fraser_coho <- readr::read_csv(data_path, show_col_types = FALSE)
stopifnot(nrow(fraser_coho) == 30L, ncol(fraser_coho) == 17L)

# Generate a new package once. overwrite = FALSE protects an existing folder.
pkg_path <- create_sdp(
  fraser_coho,
  path = file.path("output", "fraser-coho-example-sdp"),
  dataset_id = "fraser-coho-example",
  table_id = "escapement",
  seed_semantics = FALSE,
  check_updates = FALSE,
  overwrite = FALSE
)

list.files(pkg_path, recursive = TRUE)
```

### Python

`metasalmonpy` includes the same NuSEDS-derived practice table. Generate its templates with semantic searching turned off so the first result is fast and local.

```python
from importlib.resources import files
from pathlib import Path

import pandas as pd
from metasalmonpy import create_sdp

# Read packaged resources as bytes so source copies are identical.
raw_data_dir = Path("raw_data")
raw_data_dir.mkdir(exist_ok=True)
source_files = {
    "nuseds-fraser-coho-sample.csv": "nuseds-fraser-coho-sample.csv",
    "nuseds-fraser-coho-source-dictionary.csv": "column_dictionary.csv",
}
for local_name, bundled_name in source_files.items():
    source_bytes = files("metasalmonpy.data").joinpath(bundled_name).read_bytes()
    local_path = raw_data_dir / local_name
    if local_path.exists():
        if local_path.read_bytes() != source_bytes:
            raise ValueError(f"Source copy differs from the pinned package: {local_path}")
    else:
        local_path.write_bytes(source_bytes)

data_path = raw_data_dir / "nuseds-fraser-coho-sample.csv"
fraser_coho = pd.read_csv(data_path)
assert fraser_coho.shape == (30, 17)

pkg_path = create_sdp(
    fraser_coho,
    path=Path("output") / "fraser-coho-example-sdp",
    dataset_id="fraser-coho-example",
    table_id="escapement",
    seed_semantics=False,
    check_updates=False,
    overwrite=False,
)

for path in sorted(
    path for path in pkg_path.rglob("*") if path.is_file()
):
    print(path.relative_to(pkg_path))
```

### Spreadsheet

Ask the facilitator for the Fraser Coho draft package generated with the R quickstart above. Put it at `output/fraser-coho-example-sdp/` and put the accompanying `nuseds-fraser-coho-sample.csv` and `nuseds-fraser-coho-source-dictionary.csv` in `raw_data/`. Open its metadata CSVs with Excel or LibreOffice Calc, keeping identifiers and code values as text.

You are reviewing the same 30 rows as the R and Python learners. Keep the data, folder structure, and metadata headers unchanged; write review notes separately until Session 3. You do not need a personal dataset or a blank package for the core walkthrough.

::::::::::::::::::::::::::::::::::::::::::::::::

The copied source dictionary is supporting evidence: its original dataset/table IDs and annotations are not the decisions for this workshop package. Session 3 reviews its descriptions without replacing the generated dictionary.

For the R and Python lanes, `seed_semantics = FALSE` / `seed_semantics=False` is the fast classroom option. It skips live searches for links to shared definitions. Session 3 turns those searches on in R and gives Python learners saved candidate evidence from the same sample. Session 4 reviews that evidence.

## Inspect the package files

Open these files in this order. All three lanes inspect a generated Fraser Coho package.

1. `README-review.txt`
2. `metadata/column_dictionary.csv`
3. `metadata/tables.csv`
4. `metadata/dataset.csv`
5. `metadata/codes.csv`, when present
6. `semantic_suggestions.csv`, when present

All three lanes use this package structure. The source CSV is preserved in `raw_data/`; the writer names the packaged table `data/escapement.csv` after its table ID.

```text
output/fraser-coho-example-sdp/
  README-review.txt
  datapackage.json
  .metasalmon-package          # R writer bookkeeping; Python uses .metasalmonpy-package
  metadata/
    dataset.csv
    tables.csv
    column_dictionary.csv
    codes.csv                  # present when categorical columns exist
  data/
    escapement.csv              # filename follows the table ID
```

If semantic seeding is enabled later, the package may also include `semantic_suggestions.csv`, and metadata fields may contain `REVIEW: <iri>` draft values. An **IRI** is a stable web identifier for a shared term. The `REVIEW:` prefix means that the proposed match has not been accepted.

## Transfer later: what other input structures are supported?

The shared walkthrough uses one CSV. Session 7 shows how to adapt it to other inputs. `create_sdp()` does not open an arbitrary source file by itself. First use an appropriate reader to create R data frames; then pass one data frame or a named list of data frames.

| Source | Preparation | `create_sdp()` input |
| --- | --- | --- |
| One CSV or flat table | `readr::read_csv()` | One data frame; `table_id` supplies its table name. |
| Multiple CSVs | Read each CSV separately. | A named list such as `list(escapement = ..., sites = ...)`. |
| Excel workbook with several sheets | Use `readxl::read_excel()` once per rectangular sheet/table. | A named list, with safe unique table IDs as names. |
| NetCDF, raster, nested arrays | Not directly supported by this tabular workflow. | Use a format-specific packaging workflow, or a reviewed tabular derivative that does not misrepresent the source. |

The output data resources are CSV. Keep merged headings, presentation-only rows, subtotals, and multiple tables on one sheet out of the rectangular data frames passed to `create_sdp()`.

## Field definitions and accepted values

Use the [SDP field reference][sdp-field-reference] while editing. Four fields that commonly cause confusion are:

| Field | Meaning | Accepted values or rule |
| --- | --- | --- |
| `column_role` | What the column does in the table | `identifier`, `attribute`, `temporal`, `categorical`, or `measurement` |
| `value_type` | The basic type of values in the source column | `integer`, `number`, `string`, `boolean`, `date`, or `datetime` |
| `required` | Whether every data row must contain a value in this source column | `TRUE`, `FALSE`, or blank; this is different from whether an SDP metadata field itself is required. |
| `unit_label` / `unit_iri` | A readable unit and its stable identifier | `unit_label` is text; `unit_iri` is required for measurement rows and must be a valid absolute IRI. |

## Review-state validation

Early validation should catch structure problems without requiring all links to shared definitions to be complete. Use the same software lane you selected above.

::::::::::::::::::::::::::::::::::::: group-tab

### R

```r
review_check <- validate_salmon_datapackage(
  pkg_path,
  require_iris = FALSE
)

review_check$semantic_validation$issues
review_check$semantic_validation$missing_terms
```

### Python

```python
from metasalmonpy import validate_salmon_datapackage

review_check = validate_salmon_datapackage(
    pkg_path,
    require_iris=False,
)

print(review_check["semantic_validation"]["issues"])
print(review_check["semantic_validation"]["missing_terms"])
```

### Spreadsheet

Spreadsheet software does not currently run the SDP validator. For this quickstart, compare the Fraser Coho package's folder structure and metadata headers with the [SDP field reference][sdp-field-reference], and keep unresolved fields or term links visibly in review state. This manual review is not evidence that strict validation has passed.

::::::::::::::::::::::::::::::::::::::::::::::::

In the R and Python lanes, `require_iris = FALSE` / `require_iris=False` allows links to shared definitions to remain unfinished during draft review. Warnings about missing measurement links, placeholders, or `REVIEW:` markers can be acceptable in review state. Use strict validation only when the package is publication-ready.

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 1: Generate and inspect the quickstart templates

Run the bundled quickstart unchanged, then answer:

- Where is the data table?
- Which metadata file describes the dataset, each table, each column, and categorical codes?
- Which fields still need human review?
- Which Fraser Coho fields will need source context before you can describe them?
- Where are the unchanged source and the generated `escapement.csv`?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: keypoints

- Confirm the project and folders unless you already prepared them during setup.
- Keep this Fraser Coho package through Sessions 3–6; optional transfer to your own data comes in Session 7.
- `create_sdp()` accepts one data frame or a named list of tabular data frames, not arbitrary scientific file structures.
- The field reference is the source for definitions and allowed values.

::::::::::::::::::::::::::::::::::::::::::::::::
