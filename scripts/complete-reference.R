# Add explicit technical selections and EML to a NEW working-reference copy.
# This is a facilitator build helper, not independent scientific approval.
# Requires the output of build-reference.R; no live deposit or LLM call.
library(metasalmon)
library(readr)
library(dplyr)
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 1L) stop("Supply the working reference package path.")
path <- normalizePath(args[[1]])
kit <- normalizePath("episodes/files/fraser-coho-workshop")
source(file.path(kit, "scripts/workshop.R"))
pkg <- read_salmon_datapackage(path)
# Code meanings belong with the exact source values, not one invented method
# for the whole table. Preserve the richer source/question record in the kit;
# only supported canonical fields are written into the SDP code list.
code_notes <- read_csv(file.path(kit, "reference/code-definitions-working.csv"),
  col_types = cols(.default = col_character()), show_col_types = FALSE)
code_key <- function(x) paste(x$column_name, x$code_value, sep = "\r")
if (anyDuplicated(code_key(code_notes)) || !setequal(code_key(code_notes), code_key(pkg$codes))) stop("Working code definitions must match every observed categorical code exactly.")
code_notes <- code_notes[match(code_key(pkg$codes), code_key(code_notes)), , drop = FALSE]
pkg$codes$code_description <- paste(code_notes$code_description,
  "Evidence:", code_notes$evidence, "Retrieved:", code_notes$source_retrieved_utc,
  "Caveat:", code_notes$source_caveat, "Open question:", code_notes$open_question)
measurement <- pkg$dictionary$column_name == "NATURAL_ADULT_SPAWNERS"
pkg$dictionary$term_iri[measurement] <- "https://w3id.org/gcdfo/salmon#SpawnerAbundance"
pkg$dictionary$property_iri[measurement] <- "https://w3id.org/smn/Abundance"
pkg$dictionary$entity_iri[measurement] <- "https://w3id.org/smn/Population"
pkg$dictionary$unit_iri[measurement] <- "http://qudt.org/vocab/unit/INDIV"
pkg$dictionary$term_type[measurement] <- "owl_class"
pkg$dictionary$unit_label[measurement] <- "Individual"
# No claim that every row is one unique population-year observation, and no
# natural-origin constraint inferred from the word NATURAL in the column name.
pkg$tables$observation_unit <- "Population described within source location and analysis-year context; multiple records can describe a population-year pair."
pkg$tables$observation_unit_iri <- "https://w3id.org/smn/Population"
write_workshop_package(pkg, path, overwrite = TRUE)
pkg <- read_salmon_datapackage(path)
validation <- validate_salmon_datapackage(path, require_iris = TRUE)
if (nrow(validation$issues)) { print(validation$issues); stop("Strict SDP gate failed.") }

# Use the existing evidence producer pattern from metasalmon's rehearsal.
# The released package validates these closure files but does not export their
# producer. Retire the internal calls below when that public producer ships;
# keep the workshop pinned and test this helper before changing its version.
requests <- tibble::tribble(
  ~iri, ~role, ~query,
  "https://w3id.org/gcdfo/salmon#SpawnerAbundance", "variable", "spawner abundance",
  "https://w3id.org/smn/Abundance", "property", "abundance",
  "https://w3id.org/smn/Population", "entity", "population"
)
vocab <- purrr::pmap_dfr(requests, function(iri, role, query) {
  hits <- find_terms(query, role = role, sources = c("smn", "gcdfo"))
  hit <- hits[hits$iri == iri, , drop = FALSE]
  if (nrow(hit) != 1L || is.na(hit$definition[[1]]) || !nzchar(hit$definition[[1]])) stop("Could not resolve vocabulary evidence: ", iri)
  kind <- as.character(hit$resource_kind[[1]])
  tibble::tibble(iri = iri, label = as.character(hit$label[[1]]),
    definition = as.character(hit$definition[[1]]), source = as.character(hit$source[[1]]),
    ontology = as.character(hit$ontology[[1]]), resource_kind = kind,
    type_iris = as.character(hit$type_iris[[1]]),
    native_type = switch(tolower(kind), class = "owl:Class", concept = "skos:Concept", namedindividual = "owl:NamedIndividual", kind),
    source_url = if (hit$source[[1]] == "smn") "https://w3id.org/smn/" else "https://w3id.org/gcdfo/salmon",
    source_artifact_sha256 = "")
})
vocab <- bind_rows(vocab, tibble::tibble(
  iri = "http://qudt.org/vocab/unit/INDIV", label = "Individual",
  # This is a summary of QUDT's asserted types and quantity-kind relationship,
  # not a verbatim skos:definition (the source supplies no such definition).
  definition = "Counting unit labelled Individual; associated with the Population quantity kind. Workshop summary of the QUDT assertions, not a quoted definition.",
  source = "qudt", ontology = "qudt", resource_kind = "Unit",
  type_iris = "http://qudt.org/schema/qudt/Unit", native_type = "qudt:Unit",
  source_url = "http://qudt.org/vocab/unit/INDIV", source_artifact_sha256 = ""))
stopifnot(setequal(vocab$iri, metasalmon:::.ms_eml_canonical_measurement_iris(path, pkg)))
vocab$reviewed_snapshot_sha256 <- vapply(seq_len(nrow(vocab)), function(i) metasalmon:::.ms_eml_vocabulary_snapshot_sha256(vocab[i, , drop = FALSE]), character(1))
vocab_path <- file.path(path, "metadata/semantic_vocabulary.csv")
write_csv(vocab, vocab_path, na = "")
targets <- metasalmon:::.ms_eml_canonical_review_targets(pkg)
review <- targets |>
  mutate(decision = "accepted", confidence = "medium",
    review_rationale = paste("Agent technical selection for a teaching draft, based on the source field definition and cited vocabulary. Independent scientific review by Bruno and Tom is pending. No natural-origin constraint or unique population-year key is asserted.")) |>
  select(dataset_id, table_id, column_name, target_scope, target_sdp_field,
         dictionary_role, decision, confidence, review_rationale, iri)
review_path <- file.path(path, "reviewed_semantic_selections.csv")
write_csv(review, review_path, na = "")
sha <- function(p) digest::digest(file = p, algo = "sha256", serialize = FALSE)
source_manifest <- jsonlite::read_json(file.path(kit, "raw_data/source-manifest.json"))
readme <- Filter(function(x) x$path == "raw_data/upstream-example-data-README.md", source_manifest$files)[[1]]
mapping <- list(
  version = 1L, status = "final", dataset_id = "fraser-coho-workshop",
  series_key = "nuseds-fraser-coho-workshop-test", system = "knb", language = "eng",
  publication_date = format(Sys.Date()),
  semantic_vocabulary = list(path = "metadata/semantic_vocabulary.csv", sha256 = sha(vocab_path)),
  semantic_review = list(path = "reviewed_semantic_selections.csv", sha256 = sha(review_path)),
  publication = list(public = TRUE),
  rights_authorization = list(status = "confirmed", evidence = paste(
    "Open Canada record c48669a3-045b-400d-b730-48aafe8c5ee6 identifies the source publisher as Fisheries and Oceans Canada and the licence as Open Government Licence - Canada.",
    "The licence permits redistribution with attribution. This teaching derivative makes no claim of DFO endorsement.")),
  source_provenance = list(source_citation = pkg$dataset$source_citation[[1]],
    provenance_note = pkg$dataset$provenance_note[[1]], supporting_document = list(
      citation = "metasalmon contributors. Built-in NuSEDS example data, v0.5.0.",
      url = readme$source_url, sha256 = readme$sha256)),
  creators = list(list(organization_name = "Fisheries and Oceans Canada (source data)")),
  metadata_providers = list(list(given_name = "Brett", surname = "Johnson",
    email = "brett.johnson@dfo-mpo.gc.ca", orcid = "https://orcid.org/0000-0001-9317-0364")),
  contacts = list(list(given_name = "Brett", surname = "Johnson", email = "brett.johnson@dfo-mpo.gc.ca")),
  publisher = list(organization_name = "Salmon Data Standards Workshop (teaching derivative)"),
  intellectual_rights = list(paragraphs = c(
    "Contains information licensed under the Open Government Licence - Canada (https://open.canada.ca/en/open-government-licence-canada).",
    "The source data publisher is Fisheries and Oceans Canada. This KNB test teaching derivative does not imply endorsement, replace the Open Canada publication, or provide durable preservation.")),
  methods = list(list(description = paste(
    "Source records report spawner estimates and ESTIMATE_METHOD; methods vary among records.",
    "The 173-row teaching slice is derived by the pinned metasalmon script.",
    "The official dictionary defines the adult field as mature salmon excluding jacks; natural origin is not inferred.",
    "Working semantic selections are agent-authored and await independent scientific review."))),
  taxonomic_coverage = list(scientific_name = "Oncorhynchus kisutch", common_name = "Coho salmon", rank = "Species"),
  tables = list(escapement = list(attributes = list()))
)
for (i in seq_len(nrow(pkg$dictionary))) {
  r <- pkg$dictionary[i, , drop = FALSE]
  spec <- if (r$value_type == "date") list(measurement_scale = "dateTime", format_string = "YYYY-MM-DD") else if (r$column_role == "measurement") list(measurement_scale = "ratio", eml_unit = "number", number_type = "real", minimum = 0, minimum_exclusive = FALSE) else list(measurement_scale = "nominal")
  mapping$tables$escapement$attributes[[r$column_name]] <- spec
}
yaml::write_yaml(mapping, file.path(path, "metadata/eml-mapping.yml"))
write_eml_from_sdp(path, knb_environment = "test", overwrite = TRUE)
publish_sdp_to_knb(path, public = TRUE, dry_run = TRUE, representation = "expanded",
                   knb_environment = "test", overwrite = TRUE)
writeLines(c("# Working reference checkpoint", "",
  "Source data are unchanged. The dictionary carries four explicit technical",
  "measurement-role IRIs and a population observation-unit link. The code list",
  "adds source-backed working explanations and unresolved questions, without",
  "silently accepting method/classification code IRIs.", "",
  "The EML mapping status 'final' records technical export closure only.",
  "Independent scientific review by Bruno and Tom remains pending, as stated",
  "in REVIEW-STATUS.md and in the exported metadata. The reference graph and",
  "richer interpretation worksheets remain companion artifacts in the kit.", "",
  "MetaSalmon strict and EML checks pass. The independent specification",
  "validator is still blocked by the semantic descriptor comparison defect.",
  "The test publication manifest is a dry run: no upload or catalog verification."
), file.path(path, "STAGE.md"))
message("Technical SDP/EML/test-plan checks passed. Scientific review remains pending; no upload occurred.")
