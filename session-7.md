---
title: "Optional: Apply the Workflow to Your Own Dataset"
teaching: 10
exercises: 35
---

:::::::::::::::::::::::::::::::::::::: questions

- Which parts of the Fraser Coho workflow transfer to another dataset?
- How do I begin a draft from one CSV, several related tables, or an Excel workbook?
- What context and review decisions do I need before continuing?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Start a separate draft package or transfer plan while preserving the Fraser Coho workshop work.
- Choose an input pattern for one or several tidy tables.
- Record source context, one review decision or question, and a next step.

::::::::::::::::::::::::::::::::::::::::::::::::

## Transfer what you have practised

Sessions 1–6 followed the included NuSEDS Fraser Coho example through the full workshop workflow. This optional 30–45 minute activity is a first application to another dataset. Aim for a small, inspectable draft; completing the activity does not make it ready for publication.

Choose a dataset you are permitted to use in the workshop. One table is enough. No new dataset is required: if you did not bring one, write a transfer plan using the Fraser Coho workflow as your reference. Identify the inputs and row meaning you would need, context questions, the input pattern you would choose, and a next step. You can optionally copy the included Fraser Coho source CSV into the separate activity folder and practise the build steps too; keep its source identity and caveats in your context note.

## Keep a separate workspace for this activity

Keep the Fraser Coho sources, build script, and outputs from Sessions 1–6. Create these additional paths inside the same workshop project:

```text
raw_data/own-data/              # source copies and context for this activity
scripts/build_own_sdp.R         # R lane; use .py for the Python lane
output/my-salmon-sdp/           # a separate draft package
```

Put your chosen source files under `raw_data/own-data/` and leave the original tables unchanged. Use the build script to make tidy working tables: one variable per column, one observation per row, and one value per cell. Spreadsheet participants should work on a copy and record their transformations in a review log.

Write `raw_data/own-data/context.md` with a few sentences covering the source, what each row represents, how values were obtained, and one caveat or uncertainty. Add paths or links to an existing dictionary or methods document when you have one. Distinguish known facts from questions for the data holder.

## Choose one input pattern and create a draft

In the R or Python lane, choose **one** of the three import patterns below, adapt its file and sheet names, and then add the shared build step. Run the script from the workshop project root. A named list in R or dictionary in Python lets the same build step handle one or several tables; its names become the table IDs. Use stable IDs containing letters, numbers, and underscores.

::::::::::::::::::::::::::::::::::::: group-tab

### R

Start `scripts/build_own_sdp.R` with:

```r
library(metasalmon)

own_data_dir <- file.path("raw_data", "own-data")
```

[One flat CSV]{.h4 .d-block .mt-4 role="heading" aria-level="4"}

```r
# Keep the source file unchanged; add any required transformations here.
own_tables <- list(
  observations = readr::read_csv(
    file.path(own_data_dir, "my-salmon-data.csv"),
    show_col_types = FALSE
  )
)
```

[Several CSV tables in one dataset]{.h4 .d-block .mt-4 role="heading" aria-level="4"}

```r
# These are related tables belonging to one dataset, not separate datasets.
own_tables <- list(
  escapement = readr::read_csv(
    file.path(own_data_dir, "escapement.csv"),
    show_col_types = FALSE
  ),
  sites = readr::read_csv(
    file.path(own_data_dir, "sites.csv"),
    show_col_types = FALSE
  )
)
```

[Excel workbook with several sheets]{.h4 .d-block .mt-4 role="heading" aria-level="4"}

```r
workbook_path <- file.path(own_data_dir, "my-salmon-workbook.xlsx")

# Name each rectangular sheet explicitly so someone can reproduce the import.
own_tables <- list(
  escapement = readxl::read_excel(workbook_path, sheet = "Escapement"),
  sites = readxl::read_excel(workbook_path, sheet = "Sites")
)
```

[Shared build step]{.h4 .d-block .mt-4 role="heading" aria-level="4"}

```r
# Generate a local draft first; semantic review is a later, deliberate step.
own_pkg_path <- create_sdp(
  own_tables,
  path = file.path("output", "my-salmon-sdp"),
  dataset_id = "my-salmon-data",
  seed_semantics = FALSE,
  llm_assess = FALSE,
  check_updates = FALSE,
  overwrite = FALSE
)
```

### Python

Start `scripts/build_own_sdp.py` with:

```python
from pathlib import Path

import pandas as pd
from metasalmonpy import create_sdp

own_data_dir = Path("raw_data") / "own-data"
```

[One flat CSV]{.h4 .d-block .mt-4 role="heading" aria-level="4"}

```python
# Keep the source file unchanged; add any required transformations here.
own_tables = {
    "observations": pd.read_csv(own_data_dir / "my-salmon-data.csv"),
}
```

[Several CSV tables in one dataset]{.h4 .d-block .mt-4 role="heading" aria-level="4"}

```python
# These are related tables belonging to one dataset, not separate datasets.
own_tables = {
    "escapement": pd.read_csv(own_data_dir / "escapement.csv"),
    "sites": pd.read_csv(own_data_dir / "sites.csv"),
}
```

[Excel workbook with several sheets]{.h4 .d-block .mt-4 role="heading" aria-level="4"}

Pandas uses `openpyxl` to read `.xlsx` files. Name each rectangular sheet explicitly.

```python
workbook_path = own_data_dir / "my-salmon-workbook.xlsx"

own_tables = {
    "escapement": pd.read_excel(workbook_path, sheet_name="Escapement"),
    "sites": pd.read_excel(workbook_path, sheet_name="Sites"),
}
```

[Shared build step]{.h4 .d-block .mt-4 role="heading" aria-level="4"}

```python
# Generate a local draft first; semantic review is a later, deliberate step.
own_pkg_path = create_sdp(
    own_tables,
    path=Path("output") / "my-salmon-sdp",
    dataset_id="my-salmon-data",
    seed_semantics=False,
    llm_assess=False,
    check_updates=False,
    overwrite=False,
)
```

### Spreadsheet

Copy the [blank SDP CSV template][sdp-template] into `output/my-salmon-sdp/`. Use a separate blank template for this new draft so Fraser Coho metadata is not accidentally attributed to another source. Keep the original files under `raw_data/own-data/` and preserve the template's headers and folder structure.

[One flat CSV]{.h4 .d-block .mt-4 role="heading" aria-level="4"}

Save a tidy working copy under the draft's `data/` folder. Fill one dataset row in `metadata/dataset.csv`, one table row in `metadata/tables.csv`, and one dictionary row per column in `metadata/column_dictionary.csv`. Use the [SDP field reference][sdp-field-reference] as needed.

[Several CSV tables in one dataset]{.h4 .d-block .mt-4 role="heading" aria-level="4"}

Keep one dataset row, add one row per table to `metadata/tables.csv`, and save one CSV per table under `data/`. Give each table a unique ID and use it consistently in the column dictionary and any code descriptions.

[Excel workbook with several sheets]{.h4 .d-block .mt-4 role="heading" aria-level="4"}

Treat each rectangular sheet as a table. Save a CSV copy of each, then follow the several-table pattern. Record any reshaping, removed title rows, or other changes in a review log beside the draft. Spreadsheet inspection does not run automated validation; ask for an R or Python helper when you reach that step.

::::::::::::::::::::::::::::::::::::::::::::::::

The code uses `overwrite = FALSE` / `overwrite=False` to protect an existing draft. For another attempt, choose a new output path, or deliberately enable overwrite only after preserving edits and recording accepted decisions in the build script, following Session 3. Keep using `own_pkg_path` for this activity so the earlier `pkg_path` still refers to the Fraser Coho package.

Semantic seeding and LLM assessment are off in this first draft. It will not yet contain the suggestions needed for the semantic review activity. When you are ready, transfer the seeding and review steps from Sessions 3–5 to this separate script and package. Python learners need a collaborator to prepare candidate evidence for their new data while the Session 3 seeding limitation remains; never copy Fraser Coho suggestions onto another dataset. Any later LLM-assisted review remains an explicit choice, using only context files appropriate to send to the selected provider.

::::::::::::::::::::::::::::::::::::: challenge

## Activity: Produce a draft and a useful next step

Spend about 5 minutes choosing your source and writing its context, 10–15 minutes importing it, and 15–20 minutes reviewing the draft and planning what comes next.

If you are taking the plan-only route, use that time to write the four transfer-plan items above. Identify what you would need to establish rather than inventing data or running imports for files you do not have.

1. Create the separate draft using the input pattern that matches your source.
2. Inspect its dataset, table, and column metadata. Use the free-text review pattern from Session 3 to improve one description; spreadsheet users can edit the corresponding CSV and record the decision in their review log.
3. Record one supported review decision **or** one question you need a data holder to answer. Include the evidence or missing context behind it in `context.md`.
4. Choose one next step: clarify a field, describe a code, seed and review semantic candidates, run a validation check, or review publication permissions and metadata.

For the build route, finish with **one separate draft, one context note, one review decision or question, and one next step**. For the plan-only route, finish with **one transfer plan naming inputs and row meaning, context questions, a chosen input pattern, and a next step**. Compare your result with a partner if time allows. Unresolved questions are a useful result; retain them rather than filling gaps with assumptions. Publication and term-request submission still require the review and authorization steps practised in Session 6.

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: keypoints

- The shared Fraser Coho example remains the complete workshop reference.
- Your own dataset is an optional transfer activity after the shared workflow.
- Use separate input, script, and output paths to preserve the completed example.
- One dataset can contain one or several tidy tables.
- A useful first draft records context, uncertainty, and the next review step.

::::::::::::::::::::::::::::::::::::::::::::::::
