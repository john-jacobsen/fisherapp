# =============================================================================
# Problem Cache — In-memory store for generated problems
# =============================================================================
# Problems are cached server-side between GET /problems/next and POST /problems/check.
# The client never sees the correct answer until after submission.
# Problems never expire — students can take as long as they need.

# Cache environment (private to this module)
.problem_cache <- new.env(parent = emptyenv())

#' Store a problem in the cache
#'
#' @param problem A fisherapp_problem object
cache_problem <- function(problem) {
  .problem_cache[[problem$problem_id]] <- problem
}

#' Retrieve a problem from the cache
#'
#' @param problem_id Character UUID
#' @return The fisherapp_problem object, or NULL if not found
get_cached_problem <- function(problem_id) {
  .problem_cache[[problem_id]]
}

#' Remove a problem from the cache (called after successful answer submission)
#'
#' @param problem_id Character UUID
remove_cached_problem <- function(problem_id) {
  if (exists(problem_id, envir = .problem_cache)) {
    rm(list = problem_id, envir = .problem_cache)
  }
}

#' No-op: kept for compatibility with periodic call in plumber.R
clean_cache <- function() invisible(NULL)

# --- Placement state cache ---
# Placement tests need server-side state between requests.

.placement_cache <- new.env(parent = emptyenv())

#' Store placement state
#'
#' @param student_id Character UUID
#' @param state List with placement progress
cache_placement_state <- function(student_id, state) {
  .placement_cache[[student_id]] <- state
}

#' Retrieve placement state
#'
#' @param student_id Character UUID
#' @return Placement state list, or NULL
get_placement_state <- function(student_id) {
  .placement_cache[[student_id]]
}

#' Remove placement state
#'
#' @param student_id Character UUID
remove_placement_state <- function(student_id) {
  if (exists(student_id, envir = .placement_cache)) {
    rm(list = student_id, envir = .placement_cache)
  }
}
