---
title: "Optional Extension: Concept Mapping Game"
teaching: 60
exercises: 45
---

:::::::::::::::::::::::::::::::::::::: questions

- How do different people group the same salmon terms?
- What hidden assumptions are embedded in compound terms?
- How can visual mapping prepare a better term request?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Experience why local terms can be ambiguous.
- Decompose compound salmon terms into simpler pieces.
- Sketch relationships without requiring ontology editing tools.

::::::::::::::::::::::::::::::::::::::::::::::::

## When to use this extension

Use this after learners have seen the Salmon Data Package structure. Keep the shared NuSEDS Fraser Coho sample as the case, either as a warm-up before Session 4 or as a vocabulary extension. The optional bring-your-own-dataset activity is Session 7.

## Activity 1: Sort the vocabulary

Give each group cards drawn from the sample's columns, code values, and review vocabulary. Keep column names distinct from the concepts and values they record:

```text
POP_ID
POPULATION
AREA
WATERBODY
ANALYSIS_YR
SPECIES
RUN_TYPE
NATURAL_SPAWNERS_TOTAL
ESTIMATE_METHOD
ESTIMATE_CLASSIFICATION
FULL_CU_IN
Area Under the Curve
Unknown Estimate Method
natural-origin
abundance
individual
```

Ask groups to sort the cards into categories that make sense to them. Compare the groups and discuss where the categories differ.

## Activity 2: Decompose a compound term

Use `NATURAL_SPAWNERS_TOTAL`, described by the source dictionary as estimated total natural-origin spawners. Compare the compound wording with the two non-empty sample values and the blank records. Do not assume a blank means zero.

Ask:

- What is the thing being observed?
- What property is measured or asserted?
- What constraints narrow the meaning?
- What method or event context matters?
- Which pieces belong in package metadata, a code list, a README note, or a term request?

## Activity 3: Sketch a small map

Sketch the same measurement and its context: `NATURAL_SPAWNERS_TOTAL`, abundance, natural-origin spawners, unit, the `POP_ID` and `ANALYSIS_YR` row context, and row-varying `ESTIMATE_METHOD`. Connect the boxes with plain-language relationships:

- is a type of;
- measures;
- has unit;
- uses method;
- has constraint;
- close to but not identical to.

The point is not to create a formal ontology. The point is to make hidden meaning visible before a mapping or term request is made.

::::::::::::::::::::::::::::::::::::: keypoints

- People often classify the same terms differently.
- Compound terms hide entities, properties, constraints, and methods.
- Visual maps help create better metadata and better term requests.

::::::::::::::::::::::::::::::::::::::::::::::::
