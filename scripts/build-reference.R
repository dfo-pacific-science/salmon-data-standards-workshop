# Facilitator artifact preparation, not a learner shortcut past peer review.
# Run: Rscript --vanilla scripts/build-reference.R <new-output-directory>
# Produces a technically validated working example. It does not claim Bruno or
# Tom reviewed it, contact a catalog, or enable an LLM.
library(metasalmon)
library(readr)
library(dplyr)
stopifnot(as.character(packageVersion("metasalmon")) == "0.5.0")
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 1L) stop("Supply a new output directory.")
destination <- args[[1]]
if (!grepl("^(/|[A-Za-z]:[/\\\\])", destination)) destination <- file.path(getwd(), destination)
destination <- normalizePath(destination, mustWork = FALSE)
if (dir.exists(destination)) stop("Output already exists; choose a new directory.")
kit <- normalizePath("episodes/files/fraser-coho-workshop")
setwd(kit)
source("scripts/workshop.R")
raw <- read_workshop_source()
human <- readr::read_csv("reference/data-dictionary-working.csv",
  col_types = cols(.default = col_character()), show_col_types = FALSE)
create_sdp(list(escapement = raw), path = destination,
  dataset_id = "fraser-coho-workshop", table_id = "escapement",
  seed_semantics = FALSE, llm_assess = FALSE, check_updates = FALSE,
  overwrite = FALSE)
pkg <- fill_workshop_metadata(read_salmon_datapackage(destination), human)
write_workshop_package(pkg, destination, overwrite = TRUE)
writeLines(c(
  "# Working reference status", "",
  "This facilitator-prepared example is an agent-authored technical draft.",
  "Bruno and Tom have not reviewed or approved its scientific interpretations.",
  "Passing structural validation does not establish that approval.",
  "Use the separate scientific-review packet to record their actual decisions."
), file.path(destination, "REVIEW-STATUS.md"))
writeLines(c("# Draft checkpoint", "",
  "Unchanged source data plus working descriptions and supplied technical type/role bindings.",
  "All semantic IRI assignments are blank; automatic code links were cleared.",
  "Definitions are a comparison aid after your own preparation and peer review.",
  "See REVIEW-STATUS.md. Graph, decomposition and richer source evidence remain",
  "in the teaching project's worksheets/reference folders, not in canonical metadata."
), file.path(destination, "STAGE.md"))
message("Prepared unseeded working reference at ", destination)
