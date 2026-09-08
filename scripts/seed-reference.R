# Save real deterministic candidate evidence for the shared classroom queue.
# Run on a NEW copy of the facilitator draft. This makes no LLM calls.
library(metasalmon)
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 1L) stop("Supply a new copy of the draft checkpoint.")
stopifnot(as.character(packageVersion("metasalmon")) == "0.5.0")
path <- normalizePath(args[[1]])
if (file.exists(file.path(path, "semantic_suggestions.csv"))) stop("Candidate evidence already exists; use a new copy.")
pkg <- read_salmon_datapackage(path)
# Restrict the queue to the main variable and one instructive categorical field.
# The source resource remains the unchanged 173-row, 14-column table.
selected <- pkg$dictionary[pkg$dictionary$column_name %in% c("NATURAL_ADULT_SPAWNERS", "AREA"), , drop = FALSE]
result <- suggest_semantics(df = pkg$resources, dict = selected,
  codes = pkg$codes[pkg$codes$column_name == "AREA", , drop = FALSE],
  sources = c("smn", "gcdfo"), max_per_role = 3L, llm_assess = FALSE)
suggestions <- semantic_suggestions(result)
if (is.null(suggestions) || !nrow(suggestions)) stop("No candidates returned; inspect retrieval before publishing the checkpoint.")
readr::write_csv(suggestions, file.path(path, "semantic_suggestions.csv"), na = "")
jsonlite::write_json(list(
  kind = "deterministic-retrieval", utc = format(Sys.time(), tz = "UTC", usetz = TRUE),
  package = "metasalmon", version = as.character(packageVersion("metasalmon")),
  sources = c("smn", "gcdfo"), target_columns = selected$column_name,
  llm_assess = FALSE, decisions_applied = FALSE,
  note = "Real retrieved candidates, including unsuitable candidates. Neither rankings nor query text establish source meaning; consult the official dictionary."
), file.path(path, "candidate-provenance.json"), auto_unbox = TRUE, pretty = TRUE)
writeLines(c("# Candidate checkpoint", "",
  "The data and initial metadata match draft-sdp. semantic_suggestions.csv adds",
  "real deterministic retrieval evidence, without applying it or calling AI.",
  "Retrieval can inherit misleading query text, including a natural-origin",
  "constraint from the field name. Review it against the human source model.",
  "Scientific review of the reference interpretation remains pending."
), file.path(path, "STAGE.md"))
queue <- review_semantics(path, columns = unique(suggestions$column_name))
print(queue)
