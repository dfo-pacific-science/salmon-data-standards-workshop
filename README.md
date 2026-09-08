# Salmon Data Standards Workshop

This six-hour workshop follows one **NuSEDS Fraser Coho 2023–2024 dataset** from human interpretation to a Salmon Data Package and a KNB Test Node publication exercise. Everyone uses the included `nuseds-fraser-coho-2023-2024.csv`: **173 rows and 14 columns**. No personal dataset is needed.

Participants first draw how observations, results, populations, methods, and units relate. They write and peer-review a data dictionary before asking software to suggest mappings. They then compare human decisions with recorded AI outputs, document code meanings and gaps, and inspect validation, EML, and a test catalog record. The reference package is a technical draft pending Bruno and Tom's domain review; a passing software check does not supply that review.

## The six-hour sequence

| Chapter | Activity | Minutes |
| --- | --- | ---: |
| 1 | See the complete workflow and the shared data | 55 |
| 2 | Draw a human concept graph | 55 |
| 3 | Write a dictionary, decompose a measurement, and peer-review | 65 |
| 4 | Build the Salmon Data Package | 40 |
| 5 | Review mappings and compare human and AI reasoning | 70 |
| 6 | Describe codes and record term gaps | 30 |
| 7 | Validate, export EML, and inspect test publication | 45 |
| | **Teaching and activities; add breaks and lunch** | **360** |

## Start here

- [Setup](learners/setup.md): download the workshop kit and choose spreadsheet, R, or Python tools.
- [Glossary](learners/glossary.md): plain-language terms linked from their first use in the lesson.
- [Field reference](learners/field-reference.md): package files, required fields, and links to the canonical SDP specification.
- [Reference and teaching record](learners/reference.md#teaching-record): checkpoints, software boundaries, and test catalog status.
- [Instructor notes](instructors/instructor-notes.md): timing, preparation, and review criteria.
- [Extended practice](learners/extended-practice.md): five optional labs using the same source, after the human graph and dictionary checkpoints.
- [Advanced extension](learners/advanced.md): optional ontology formalization after the six-hour workshop, using the same human graph.

Extended practice is outside the 360-minute schedule. The labs investigate repeated population–year records, missingness and method context, code sources, a reviewed metadata edit across R and Python, and validation/EML/manifest evidence. They use the included data and local artifacts without requiring live AI or a deposit.

The project is `fraser-coho-workshop/`. Keep the source at `raw_data/nuseds-fraser-coho-2023-2024.csv`, the build at `scripts/build_sdp.R` or `scripts/build_sdp.py`, and the working package at `output/fraser-coho-workshop-sdp`. Dataset ID `fraser-coho-workshop` and table ID `escapement` remain consistent throughout. The kit contains `draft-sdp`, `seeded-sdp`, and `reference-sdp` checkpoints from the same data.

## Tools and access

The lesson pins R `metasalmon` to **v0.5.0** and Python `metasalmonpy` to **v0.4.0**. The Python release does not yet provide the R-native review and metadata setters; its lane uses the documented alternatives and supplied evidence. Spreadsheet participants review the same files and decisions.

The human–AI comparison is required, using supplied recorded outputs. Live AI calls are optional. Participants need no AI account, API key, purchased credits, or catalog account to complete the workshop. Optional OpenRouter practice uses a free model with no paid fallback; optional Ollama practice can use a local model.

Catalog work uses a separately authorized **KNB Test Node** teaching record under Brett's identity. It does not authorize a production deposit or imply Bruno and Tom have reviewed the scientific meanings. See the [teaching-record status](learners/reference.md#teaching-record) before presenting a live result.

## Repository maintenance

Edit lesson sources under `episodes/` and `learners/`; do not edit generated `site/` output. Kit source files are under `episodes/files/fraser-coho-workshop/`, and the downloadable ZIP is `episodes/files/fraser-coho-workshop.zip`. [Entrypoints](docs/entrypoints.md) records the source map, build commands, and checks.

The [Salmon Data Package specification](https://github.com/salmon-data-mobilization/smn-data-pkg/blob/main/SPECIFICATION.md), [metasalmon](https://github.com/salmon-data-mobilization/metasalmon), and [metasalmonpy](https://github.com/salmon-data-mobilization/metasalmonpy) own the underlying formats and software contracts.
