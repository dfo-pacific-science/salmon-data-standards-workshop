---
title: "Capture Fraser Coho Context and Rebuild the Package"
teaching: 40
exercises: 35
---

:::::::::::::::::::::::::::::::::::::: questions

- What does the Fraser Coho table leave unexplained?
- How do I rebuild the same package from unchanged inputs?
- Which source statements belong in metadata, and which remain review questions?
- How do I prepare semantic candidates without invoking an LLM?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Continue with the same 30-row NuSEDS Fraser Coho sample from Session 2.
- Extend one build script using the same dataset ID, table ID, and output path.
- Compare source descriptions with actual values before recording metadata decisions.
- Write a short context note that distinguishes observations from unresolved interpretations.
- Seed the candidates that Session 4 will review, with LLM assessment off.

::::::::::::::::::::::::::::::::::::::::::::::::

## Continue the Fraser Coho package

Keep `raw_data/nuseds-fraser-coho-sample.csv` unchanged. We are extending the Session 2 package, not starting a different dataset. Use these names throughout Sessions 2–6:

| Item | Shared value |
| --- | --- |
| Source data | `raw_data/nuseds-fraser-coho-sample.csv` |
| Supporting dictionary | `raw_data/nuseds-fraser-coho-source-dictionary.csv` |
| Dataset ID | `fraser-coho-example` |
| Table ID | `escapement` |
| Working package | `output/fraser-coho-example-sdp/` |
| Build script | `scripts/build_sdp.R` or `scripts/build_sdp.py` |

Use the script from Session 2. Keep its source-copy checks; replace its original read/create block with the corresponding block below. Run from the workshop project root. Spreadsheet participants continue with their facilitator-generated copy of this same package.

The single-table example is enough to learn the process. [Session 7](session-7.Rmd) provides optional single-CSV, multi-table, and Excel patterns for your own dataset after the shared walkthrough.

## Inspect source context before writing metadata

Open the source dictionary beside the CSV and read the [bundled example notes][metasalmon-example-data]. The dictionary has the older example IDs `nuseds_fraser_coho_sample` and `nuseds_fraser_coho`. Use it as evidence for descriptions; do not paste the whole file over `metadata/column_dictionary.csv`, change the workshop IDs, or treat its existing semantic links as decisions you have already reviewed.

Start with these actual fields:

| Field | What to examine |
| --- | --- |
| `POP_ID`, `POPULATION` | How the source identifies and names a population record. |
| `ANALYSIS_YR` | The years present; distinguish the estimate's analysis year from survey dates. |
| `NATURAL_SPAWNERS_TOTAL` | The source description, the two populated cells, and the 28 blank cells. A blank is not evidence of zero spawners. |
| `ESTIMATE_METHOD` | Different method labels on different rows, including `Area Under the Curve`, `Not Applicable`, and `Unknown Estimate Method`. |
| `ESTIMATE_CLASSIFICATION` | Why abundance classifications may matter when interpreting an estimate. |
| `START_DTT`, `END_DTT` | Survey-period dates, including missing dates, as distinct from `ANALYSIS_YR`. |

The sample contains 30 rows, 17 columns, and analysis years ranging from 1996 to 2024. It does not establish complete coverage over that interval. The separate 173-row 2023–2024 example and its derivation are described in the same upstream notes; those provenance statements must not be copied onto this sample as though they describe its extraction.

## Write the shared context note

Create `raw_data/fraser-coho-context.md` with this starting text. Add your observations and source-backed answers during the exercise; leave questions visible when the available evidence does not settle them.

```text
# Context for the NuSEDS Fraser Coho workshop sample

## Purpose and source
We are documenting the bundled nuseds-fraser-coho-sample.csv practice table.
Record the installed package name and version used to obtain the files.
The source dictionary is supporting evidence, not an accepted mapping ledger.

## What the file contains
30 rows and 17 columns; ANALYSIS_YR ranges from 1996 to 2024.
POP_ID and POPULATION identify the source population record.
ESTIMATE_METHOD and ESTIMATE_CLASSIFICATION vary between records.

## Caveats
This small sample is not a complete Fraser Coho time series.
NATURAL_SPAWNERS_TOTAL has 28 blank values. Do not replace blanks with zero.
The larger 2023-2024 example is a separate dataset.

## Questions for reviewers
What exact biological scope does NATURAL_SPAWNERS_TOTAL have in this source?
How should estimate method and classification affect interpretation?
What evidence establishes the meaning of a missing estimate?
Which source, rights, and contact facts still need confirmation before release?
```

This learner-authored note is a review aid, not new source authority. Keep it under version control with your build script when appropriate. For a handoff, include a reviewed copy of the relevant caveats in the package README or another documented context artifact; files left only in `raw_data/` do not automatically travel with the SDP.

## Rebuild the same package and seed candidates

The source files and note now exist. In this chapter, `overwrite = TRUE` deliberately rebuilds the Session 2 draft at the same path. Preserve any edits that exist only inside `output/` before running; from here on, encode accepted metadata decisions after the create call so reruns apply them again.

::::::::::::::::::::::::::::::::::::: group-tab

### R

```r
library(metasalmon)

# These are file paths. Listing context does not itself request an LLM call.
use_llm_review <- FALSE
context_files <- c(
  file.path("raw_data", "nuseds-fraser-coho-source-dictionary.csv"),
  file.path("raw_data", "fraser-coho-context.md")
)
stopifnot(all(file.exists(context_files)))

fraser_coho <- readr::read_csv(
  file.path("raw_data", "nuseds-fraser-coho-sample.csv"),
  show_col_types = FALSE
)
stopifnot(nrow(fraser_coho) == 30L, ncol(fraser_coho) == 17L)

# Same source, dataset, table, and destination as Session 2.
# Seeding retrieves candidate terms; humans decide them in Session 4.
pkg_path <- create_sdp(
  fraser_coho,
  path = file.path("output", "fraser-coho-example-sdp"),
  dataset_id = "fraser-coho-example",
  table_id = "escapement",
  seed_semantics = TRUE,
  llm_assess = use_llm_review,
  llm_context_files = if (use_llm_review) context_files else NULL,
  check_updates = FALSE,
  overwrite = TRUE
)

source_dictionary <- readr::read_csv(context_files[[1]], show_col_types = FALSE)
context_note <- readr::read_file(context_files[[2]])
```

### Python

For this pinned release, use candidate evidence prepared by the facilitator's R build of the **same sample**. Save its `semantic_suggestions.csv` as `raw_data/fraser-coho-semantic_suggestions.csv`. The facilitator records the package version and lookup date with it. The Python build below stays local, then restores this evidence after writing metadata.

This route avoids a measured `metasalmonpy 0.4.0` / pandas `3.0.5` seeding failure (`Can only compare identically-labeled ... DataFrame objects`). It does not accept any candidate. Retire this handoff when a released Python/dependency combination passes the sample's seeded rebuild and is pinned and tested here.

```python
from pathlib import Path

import pandas as pd
import shutil
from metasalmonpy import create_sdp

context_files = [
    Path("raw_data") / "nuseds-fraser-coho-source-dictionary.csv",
    Path("raw_data") / "fraser-coho-context.md",
]
for context_path in context_files:
    if not context_path.is_file():
        raise FileNotFoundError(context_path)

fraser_coho = pd.read_csv(Path("raw_data") / "nuseds-fraser-coho-sample.csv")
assert fraser_coho.shape == (30, 17)

# Check the supplied evidence before rebuilding the local draft.
suggestions_path = Path("raw_data") / "fraser-coho-semantic_suggestions.csv"
saved_suggestions = pd.read_csv(suggestions_path)
assert not saved_suggestions.empty
assert set(saved_suggestions["dataset_id"]) == {"fraser-coho-example"}
assert set(saved_suggestions["table_id"]) == {"escapement"}

pkg_path = create_sdp(
    fraser_coho,
    path=Path("output") / "fraser-coho-example-sdp",
    dataset_id="fraser-coho-example",
    table_id="escapement",
    seed_semantics=False,
    llm_assess=False,
    llm_context_files=None,
    check_updates=False,
    overwrite=True,
)

source_dictionary = pd.read_csv(context_files[0])
context_note = context_files[1].read_text(encoding="utf-8")
```

### Spreadsheet

Open the two files under `raw_data/` beside the generated metadata CSVs. Review the source descriptions and write the context note above. The facilitator supplies a seeded copy of the same Fraser Coho package for Session 4, including `semantic_suggestions.csv`; preserve your current copy and review log before replacing it.

Keep the same dataset ID `fraser-coho-example` and table ID `escapement`. Record each metadata change and its evidence in the review log. The spreadsheet workflow remains inspectable; an R or Python collaborator runs the executable rebuild and validator.

::::::::::::::::::::::::::::::::::::::::::::::::

In the R lane, `seed_semantics = TRUE` performs vocabulary lookup and may contact vocabulary services. It is separate from LLM assessment and may take a few minutes. The facilitator can supply saved suggestions for the same sample if lookup would interrupt the schedule. Session 4 reads those suggestions without searching again.

`llm_context_files` accepts local file paths, not the parsed dictionary or note. With the R toggle off and the Python call fixed to `False`, `NULL` / `None` avoids ignored-context warnings and no LLM request is made. Optional LLM review is a later, explicit choice after selecting a provider and deciding which context can be sent. `check_updates = FALSE` disables the unrelated version lookup.

## Record a reviewed description in the script

The following text describes the inspected file, not a claim that the dataset is ready for scientific reuse. Append the corresponding block after `create_sdp()`; Session 4 will append semantic decisions after it.

::::::::::::::::::::::::::::::::::::: group-tab

### R

```r
# Setters update the declared metadata fields and retain the review evidence.
set_sdp_dataset(
  pkg_path,
  title = "NuSEDS Fraser Coho workshop sample",
  description = paste(
    "Thirty NuSEDS Fraser Coho sample records with analysis years from 1996 to 2024.",
    "Prepared for workshop practice; not a complete time series.",
    "Blank spawner estimates have not been replaced with zero."
  )
)
set_sdp_table(
  pkg_path,
  "escapement",
  description = "NuSEDS sample records with population, analysis year, estimate and method fields."
)
set_sdp_column(
  pkg_path,
  "POP_ID",
  table = "escapement",
  column_description = "NuSEDS population identifier, retained from the source sample."
)

review_check <- validate_salmon_datapackage(pkg_path, require_iris = FALSE)
review_check$semantic_validation$issues
```

### Python

The pinned Python release does not have the R setters. Record the same decisions as assignments and rebuild the metadata with its writer.

```python
from metasalmonpy import (
    read_salmon_datapackage,
    validate_salmon_datapackage,
    write_salmon_datapackage,
)

reviewed_pkg = read_salmon_datapackage(pkg_path)
reviewed_dataset = reviewed_pkg["dataset"].copy()
reviewed_dataset.loc[:, "title"] = "NuSEDS Fraser Coho workshop sample"
reviewed_dataset.loc[:, "description"] = (
    "Thirty NuSEDS Fraser Coho sample records with analysis years from 1996 to 2024. "
    "Prepared for workshop practice; not a complete time series. "
    "Blank spawner estimates have not been replaced with zero."
)
reviewed_tables = reviewed_pkg["tables"].copy()
reviewed_tables.loc[reviewed_tables["table_id"] == "escapement", "description"] = (
    "NuSEDS sample records with population, analysis year, estimate and method fields."
)
reviewed_dictionary = reviewed_pkg["dictionary"].copy()
column_rows = (
    (reviewed_dictionary["table_id"] == "escapement")
    & (reviewed_dictionary["column_name"] == "POP_ID")
)
reviewed_dictionary.loc[column_rows, "column_description"] = (
    "NuSEDS population identifier, retained from the source sample."
)

pkg_path = write_salmon_datapackage(
    resources=reviewed_pkg["resources"],
    dataset_meta=reviewed_dataset,
    table_meta=reviewed_tables,
    dict_df=reviewed_dictionary,
    codes=reviewed_pkg["codes"],
    path=pkg_path,
    overwrite=True,
)
# Preserve the supplied candidate evidence for Session 4 and every rebuild.
shutil.copyfile(suggestions_path, Path(pkg_path) / "semantic_suggestions.csv")
review_check = validate_salmon_datapackage(pkg_path, require_iris=False)
print(review_check["semantic_validation"]["issues"])
```

### Spreadsheet

Put the reviewed dataset title and description above in `metadata/dataset.csv`, the table description in the `escapement` row of `metadata/tables.csv`, and the `POP_ID` description in its dictionary row. Record the reason and source for each change beside the package. Keep contacts, rights, and uncertain meanings visibly unresolved.

::::::::::::::::::::::::::::::::::::::::::::::::

Do not use `prune = TRUE`: it removes `semantic_suggestions.csv`, which Session 4 needs. Keep the seeded evidence and the decisions together. A later live search can return different candidates; an executable script alone does not freeze a vocabulary release or make a rank number a stable identifier. Compare candidate IRIs when replaying semantic decisions.

## What goes where?

| Fraser Coho context | Best place |
| --- | --- |
| Sample purpose, confirmed provenance, coverage, contact and rights | `metadata/dataset.csv` |
| What an `escapement` record represents | `metadata/tables.csv` |
| Descriptions of `POP_ID`, `ANALYSIS_YR`, estimates, and dates | `metadata/column_dictionary.csv` |
| Meanings of `ESTIMATE_METHOD` and other categorical values | `metadata/codes.csv` |
| Incomplete sample coverage, missing estimates, interpretation questions | Context note and reviewed package README |

A useful description explains the field, what each value represents, its units or format, how it was obtained, and what a reader must not assume. For this sample, `POP_ID` can be described from the dictionary and checked against the table. The precise biological scope of `NATURAL_SPAWNERS_TOTAL` requires source review; copying a plausible definition into that cell does not settle it.

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 1: Make the Fraser Coho context reproducible

1. Confirm the 30 source rows, 17 columns, and unchanged dataset/table IDs.
2. Add the context note and source-dictionary paths to your build script.
3. Run the same-package build with LLM review off. R generates candidates; Python restores the supplied same-sample candidates after its metadata write.
4. Record the dataset description, table description, and `POP_ID` description above. Compare four more source descriptions with their columns; encode supported wording or record the unresolved question in your note.
5. Inspect the generated `semantic_suggestions.csv`. Keep the `escapement.csv` data unchanged and carry this package into Session 4.

Rerun your build script to confirm that the recorded descriptions survive. Preserve a seeded copy for review so you do not need to repeat live searches during the next exercise.

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: keypoints

- The same Fraser Coho source, dataset ID, table ID, and working package continue through the core workshop.
- Source dictionaries inform review; their old IDs and annotations are not automatically accepted metadata.
- Keep inputs, context, and accepted metadata decisions connected through one script or an explicit spreadsheet review log.
- R semantic seeding retrieves the candidates for Session 4; Python uses supplied same-sample evidence. LLM review remains a separate opt-in.
- Missing estimates and incomplete sample coverage must remain visible.
- Optional transfer to a personal dataset comes after the shared publication walkthrough in Session 7.

::::::::::::::::::::::::::::::::::::::::::::::::
