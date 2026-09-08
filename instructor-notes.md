---
title: 'Instructor Notes'
---

## Teaching stance

Start with the end goal and the shared NuSEDS Fraser Coho sample. In the first five minutes, say:

> How far you take this workflow depends on your goals. The common biologist pathway is FAIR publication through a reviewed Salmon Data Package, validated EML, and a guarded catalog plan. The pathway can extend to proposing missing shared terms or planning how organizational terminology will be governed and mapped to the Salmon Domain Ontology. A live upload is a separate, authorized publication action.

Everyone uses `nuseds-fraser-coho-sample.csv` from first inspection through the final dry run: 30 rows, 17 columns, and selected years from 1996–2024. Introduce own data only in optional Session 7, after the shared workflow. No learner-owned dataset is required.

The first hands-on win is still a package that someone else can review. The first code example should only generate templates; do not turn it into a full semantic or publication demonstration.

Before using specialized language, say:

> An ontology is a maintained set of concepts and definitions that also records how the concepts relate. Biologists can complete the common pathway by reusing shared definitions; data stewards and digital librarians can follow the advanced pathway for organizational vocabularies, ontologies, and bridge mappings.

Say "link to a shared definition" before introducing "semantic link" or "semantic mapping." Present R and Python as parallel language lanes while naming the current Session 4 Python review gap. Give spreadsheet participants a generated package from the same sample and point them to the no-code subsection.

Repeat these messages throughout:

- A clear description is better than a forced IRI.
- A decision that is not in the script did not happen. The pasted call is the audit trail.
- Not every field needs an ontology term.
- Measurement columns deserve the most careful semantic review.
- Local context should be preserved and mapped, not renamed away.
- New-term requests are evidence packages for maintainers.
- A dataset may contain several tables; a flat file contains one rectangular table.
- The EML sidecar records facts and authority that cannot be inferred safely.
- A credential-free KNB dry run is different from a persistent live upload.

## One-hour introduction

Use this when the goal is awareness and recruitment. Keep the same Fraser Coho sample on screen for every demonstration; invite later own-data practice as a next step.

| Time | Activity |
| --- | --- |
| 0:00-0:05 | Introduce the tiered destinations; focus this format on reviewed SDP -> valid EML -> guarded catalog plan |
| 0:05-0:15 | Introduce the integration system and give a high-level tour of the SDP structure |
| 0:15-0:20 | Confirm the project plus `raw_data/`, `scripts/`, and `output/` before code |
| 0:20-0:32 | Run the simple `create_sdp()` template-generation example; point out the R, Python, and spreadsheet lanes |
| 0:32-0:45 | Review key field definitions, one measurement row, and one code row |
| 0:45-0:55 | Trace SDP fields into EML and inspect a credential-free KNB dry-run manifest |
| 0:55-1:00 | Explain rerun safety, authorization boundaries, and next steps |

Do not teach ontology editing in the one-hour format.

## Full-day workshop

| Time | Activity |
| --- | --- |
| 0:00-0:30 | Integration-system overview, dataset/table/flat-file definitions, and high-level package anatomy |
| 0:30-0:45 | Create/open project and confirm `raw_data/`, `scripts/`, and `output/` |
| 0:45-1:30 | Generate or open the shared Fraser Coho draft package and inspect its structure |
| 1:30-2:15 | Save the reproducible sample build and peer-review package structure |
| 2:15-3:00 | Read the sample source notes, capture context, and seed semantic candidates |
| 3:00-4:00 | Review Fraser Coho measurement semantics |
| 4:00-4:45 | Review the sample code lists and SKOS/profile choices |
| 4:45-5:15 | Route sample term gaps and draft requests |
| 5:15-6:00 | Strict validation, sample EML export, KNB dry run, and later-version workflow |
| 6:00-6:45 | Optional Session 7: start a separate own-data package or make a transfer plan |

These are 6–6¾ hours of teaching and activities; add breaks and lunch to the delivery schedule. Allow 30–45 minutes for optional Session 7. If time is tight, retain the shared end-to-end workflow and offer own-data practice as follow-up.

## Mixed-audience facilitation

Spreadsheet participants use the canonical metadata CSVs from a facilitator-generated package of the same Fraser Coho sample, rather than assembling a different blank-template example. Automated validation, EML export, manifest generation, and publication currently require R or Python; explain that boundary without treating either code implementation as primary.

Recommended table roles:

- source reader: checks the supplied dictionary and notes for evidence about meaning;
- package editor: edits the metadata CSV cells;
- reviewer: asks what could be misunderstood;
- mapper: checks suggestions and records gaps.

## Checkpoint prompts

After Session 1:

- Can another person find the data table?
- Can they tell what each row represents?
- Can learners distinguish a dataset, table, flat file, and workbook?
- Are required metadata blanks visible?
- Can learners explain an ontology as shared concepts, definitions, and relationships?
- Can learners name the end product and explain why EML needs an explicit mapping sidecar?

After Session 2:

- Was the project and folder layout ready before the demo?
- Did the chosen R or Python path generate `output/fraser-coho-example-sdp`, or did the spreadsheet path open that same facilitator-generated sample package?
- Are the unchanged CSV and source dictionary under `raw_data/`?
- Can learners explain that Sessions 2–6 keep using this sample and own-data transfer is optional in Session 7?
- Which fields still contain placeholders or `REVIEW:` suggestions?

After Session 3:

- Are the prepared source data and context files together and unchanged under `raw_data/`, reproducible R/Python builds under `scripts/`, and generated packages under `output/`?
- Can learners read `raw_data/nuseds-fraser-coho-sample.csv` using a path relative to the project root?
- Do the build and metadata consistently identify dataset `fraser-coho-example` and table `escapement`?
- Have they distinguished facts supported by the source dictionary from questions that remain unresolved?
- Is enough context present to prevent obvious misuse?
- Can they explain what an unsafe rerun could overwrite and how a new version protects reviewed work?

After Session 4:

- Which measurement mappings are accepted?
- Which are rejected, and is the reason recorded in the script rather than only in the room?
- Can a learner point at the line in `scripts/build_sdp.R` that made each decision, and rerun it?
- Are units treated separately from I-ADOPT roles, statistical modifiers used only for aggregations, and methods placed at the table, protocol, or code level rather than in the dictionary?
- Can they say what the review queue does *not* show them?

After Sessions 5 and 6:

- Which terms are shared candidates?
- Which are DFO-specific?
- Which should stay local/profile?
- Is there enough evidence to make a useful request?
- Did strict validation pass before EML export?
- Which facts came directly from SDP, and which required `eml-mapping.yml`?
- Was catalog work a dry run or an authorized live upload?
- If updating an older package, was a new version written instead of overwriting reviewed or published state?

After optional Session 7:

- Is own-data work separate from the shared sample, with its own input, build script, and output folder?
- Has the learner explained the new table's row meaning and recorded one unresolved question?
- Have they reviewed which decisions transfer, instead of copying Fraser Coho mappings into unrelated data?

## Common pitfalls

- Learners try to fill every semantic field. Redirect to "measurements first."
- Learners trust `REVIEW:` suggestions. Ask them to read the definition and scope.
- Learners read the retrieval score as a confidence score. It is neither. `AREA` in the shared example retrieves an ENVO body of water at score 9.35 and is wrong; use it as the worked counterexample.
- Learners assume `rank = 1` was the best of several. In a one-shot seeded package each slot's shortlist is one candidate deep, so `rank = 1` is usually the only rank there is. Show them `Ranks available: 1.`
- Learners decide in the console and never paste the call into the script. That is the spreadsheet problem in a new costume; stop and have them paste before moving on.
- Learners treat an empty review queue as a finished package. The queue shows shortlists, not gaps; the validation report is the authority.
- Groups debate ontology classes too early. Bring them back to the package row, column, code value, or caveat.
- Local method bins get proposed as shared terms. Ask whether another organization would use the same definition.
- Participants add extra columns to canonical metadata CSVs. Put extra context in the README or sidecar notes instead.
- Participants call a workbook, sheet, dataset, and table the same thing. Ask what the whole collection is, how many rectangular tables it contains, and what one row means in each.
- Participants expect NetCDF to work because Excel workbooks do. Explain that multi-sheet tabular input is different from multidimensional scientific arrays.
- Participants rerun `create_sdp(..., overwrite = TRUE)` after manual edits. Stop and read the reviewed package or write a new versioned folder.
- Participants assume an EML file can be made by renaming another XML file. Show schema validation and the sidecar requirements.
- Participants treat `public = FALSE` as a disposable server-side draft. A live KNB call still creates persistent production objects; use a local dry run for teaching.

## Facilitator preparation

Before delivery:

- use exactly the bundled `nuseds-fraser-coho-sample.csv` throughout; do not substitute the separate 173-row `nuseds-fraser-coho-2023-2024.csv` partway through;
- prepare an RStudio Project containing `raw_data/`, `scripts/`, and `output/`. Session 2 copies the CSV and `column_dictionary.csv` renamed `nuseds-fraser-coho-source-dictionary.csv` from the installed package into `raw_data/`;
- give spreadsheet learners those same two source files and a generated `output/fraser-coho-example-sdp` folder. Keep the source dictionary as review evidence: its legacy IDs and annotations must not replace the generated metadata directly;
- prepare the reproducible sample build at `scripts/build_sdp.R` or `scripts/build_sdp.py`, using dataset ID `fraser-coho-example`, table ID `escapement`, and `output/fraser-coho-example-sdp`;
- prepare the Session 3 context-note activity at `raw_data/fraser-coho-context.md`, distinguishing source-supported descriptions, teaching notes, and unresolved questions;
- install the pinned releases — R/`metasalmon` **v0.5.0** and Python/`metasalmonpy` **v0.4.0**, per `learners/setup.md` — and verify the examples in each language being taught. The two numbers differ on purpose: Session 4's review flow shipped in metasalmon 0.5.0 and has no Python port yet;
- prepare the `NATURAL_SPAWNERS_TOTAL` measurement review using the sample source notes;
- prepare a seeded checkpoint of the same sample before teaching if vocabulary lookup is slow or unavailable. Build separate seeded, reviewed, and EML-ready checkpoints with the same dataset/table IDs, rows, and values, label their stage clearly, and retain the build/review decisions that produced each one. Session 4's native queue review does not need new network calls;
- supply the R-seeded `semantic_suggestions.csv` as `raw_data/fraser-coho-semantic_suggestions.csv` for Python learners, recording the package version and lookup date. Session 3 validates its sample IDs and restores it after the local metadata write; direct Python seeding failed with the tested `metasalmonpy 0.4.0` / pandas `3.0.5` combination;
- prepare the `ESTIMATE_METHOD` code-list review from this same sample;
- prepare one unresolved term with routing rationale;
- if demonstrating optional LLM review, use an approved provider and non-sensitive context, and show how bundle decisions can be downgraded to manual review;
- prepare a strictly valid, fully reviewed checkpoint of this same 30-row sample with real checksum-bound EML sidecars for Session 6. Verify that it preserves the shared input's rows and values; metadata checkpoints must not silently substitute another sample. Retain sources for descriptive metadata and any licence or provenance claim; the bundled README's fuller-example derivation does not establish the tiny sample's exact extraction history. Do not fabricate facts during delivery;
- generate and review that sample checkpoint's credential-free KNB dry-run manifest before teaching. If the necessary evidence or publication-ready metadata is unavailable, teach the failing gate and unresolved requirements; do not switch datasets to obtain a passing example;
- decide whether strict validation and EML export in the taught R or Python lane will be learner-run or instructor-led;
- reserve 30–45 minutes for optional Session 7. Own-data inputs go in `raw_data/own-data/`, builds in `scripts/build_own_sdp.R` or `scripts/build_own_sdp.py`, and output in `output/my-salmon-sdp`; learners without their own data make a transfer plan from the sample; and
- default to no live catalog upload. If a live demonstration is explicitly authorized, pre-confirm credentials, redistribution authority, intended access, rollback/recovery expectations, and how `published_pending_catalog` will be reported.
