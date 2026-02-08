# =============================================================================
# Template Registry — Store and retrieve problem templates
# =============================================================================

# Internal environment to hold all registered templates
.template_registry <- new.env(parent = emptyenv())

#' Register a problem template
#'
#' Templates are declarative list objects that the generic problem engine
#' consumes to generate randomized problem instances.
#'
#' @param template A list with required fields: template_id, topic_id,
#'   difficulty, params, statement, solve, format_answer
#' @return Invisible template_id
#' @export
register_template <- function(template) {
  required <- c("template_id", "topic_id", "difficulty",
                 "params", "statement", "solve", "format_answer")
  missing <- setdiff(required, names(template))
  if (length(missing) > 0) {
    stop("Template missing required fields: ", paste(missing, collapse = ", "))
  }
  stopifnot(
    is.character(template$template_id),
    is.character(template$topic_id),
    is.numeric(template$difficulty),
    template$difficulty >= 1 && template$difficulty <= 5,
    is.list(template$params),
    is.function(template$statement),
    is.function(template$solve),
    is.function(template$format_answer)
  )
  .template_registry[[template$template_id]] <- template
  invisible(template$template_id)
}

#' Get templates matching a topic and optional difficulty
#'
#' @param topic_id Character topic ID
#' @param difficulty Integer 1-5, or NULL for all difficulties
#' @return List of matching template objects
#' @export
get_templates <- function(topic_id, difficulty = NULL) {
  all_keys <- ls(.template_registry)
  matches <- list()
  for (k in all_keys) {
    tmpl <- .template_registry[[k]]
    if (tmpl$topic_id == topic_id) {
      if (is.null(difficulty) || tmpl$difficulty == difficulty) {
        matches[[length(matches) + 1]] <- tmpl
      }
    }
  }
  matches
}

#' List all registered template IDs
#'
#' @return Character vector of template IDs
#' @export
list_templates <- function() {
  ls(.template_registry)
}

#' Clear all templates (for testing)
#' @keywords internal
clear_templates <- function() {
  rm(list = ls(.template_registry), envir = .template_registry)
}
