---
title: "Optional Extension: From the Dataset Graph to Ontology Work"
teaching: 20
exercises: 25
---

:::::::::::::::::::::::::::::::::::::: questions

- Which parts of our human graph could become formal ontology statements?
- Which definitions need local stewardship, and which can be shared?
- What review is needed before formalizing the model?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Revisit the required human graph and identify a small formalization question.
- Distinguish source fields, concepts, individual observations, and stored values.
- Draft a scoped ontology or vocabulary contribution with evidence and open questions.

::::::::::::::::::::::::::::::::::::::::::::::::

## Extend the graph you already made

The graph was required before packaging and AI in Chapters 2–3. This optional extension returns to that same Fraser Coho graph after the common workflow. Keep the same 173-row, 14-column source; the task is to examine its meaning more carefully.

[OWL](glossary.html#ontology) can represent formal classes, properties, and logical relationships. A useful classroom diagram is a starting point for that work, not a validated OWL ontology. A line labelled “relates to” needs a more precise meaning before it becomes a formal assertion.

## Choose one small part of the model

Use a node and its connections from `worksheets/dataset-nodes.csv` and `worksheets/dataset-edges.csv`. Candidates include a source estimate record, the population it concerns, the reported result, the variable measured, its analysis-year context, or the method used. Do not equate a table row with a fully specified observation activity merely because an estimate is stored there.

Ask:

- Is each node a concept, an individual observation, a source column, an identifier, or a literal value?
- What does each directed edge assert, and what evidence supports it?
- Does a qualifier describe the entity, the variable, the observation process, or the source system?
- Which unresolved source question must be settled before this statement is formalized?
- Which definition belongs to the shared salmon model, and which depends on DFO or NuSEDS practice?

Preserve the distinction between an analysis year and survey dates, between population-year context and a proven row key, and between the source's “natural” wording and an unsupported natural-origin interpretation.

## Keep shared and local stewardship explicit

The Salmon Domain Ontology provides shared anchors. A local vocabulary can retain organization-specific meanings and connect to shared concepts with a mapping supported by the evidence. An exact relationship makes a stronger claim than a related or broader relationship; choose the relationship only after comparing definitions and scope.

Building an organizational vocabulary requires named stewards, a review process, stable identifiers, publication, and maintenance. This extension produces a proposal for that process or a small term request; it does not establish governance merely by drawing the graph.

Use the [Salmon Domain Ontology conventions][sdo-conventions] and [modules and bridges guide][sdo-bridge-guide] when developing a formal contribution. Record uncertainty and proposed placement rather than minting authoritative-looking identifiers during the exercise.

::::::::::::::::::::::::::::::::::::: challenge

## Activity: prepare a formalization question

In 25 minutes, choose three to five connected nodes from the human graph. Rewrite the edge labels as precise statements, identify their possible model roles, and attach source evidence. Mark at least one statement as supported, uncertain, or requiring a domain decision, with the reason.

Produce one small diagram plus a paragraph explaining what would need review before OWL formalization or organizational vocabulary publication. Share the draft for scientific and modelling review; do not treat the act of writing it as independent verification.

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: keypoints

- Human modelling is part of the core workflow; formal ontology authoring is an extension.
- Source columns, concepts, observations, and values must remain distinguishable.
- Local authority and evidence determine which definitions can be shared and how they map.

::::::::::::::::::::::::::::::::::::::::::::::::
