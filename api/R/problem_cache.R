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

# --- Placement state DB persistence ---
# These functions back the in-memory cache with the database so placement
# progress survives server restarts and browser closes.

#' Persist placement state to the database
#'
#' @param pool Database connection pool
#' @param student_id Character UUID
#' @param state Placement state list
save_placement_state_db <- function(pool, student_id, state) {
  state_json <- jsonlite::toJSON(state, auto_unbox = TRUE, null = "null")
  DBI::dbExecute(pool,
    "INSERT INTO placement_sessions (student_id, state, updated_at)
     VALUES ($1::uuid, $2::jsonb, now())
     ON CONFLICT (student_id) DO UPDATE
       SET state = EXCLUDED.state, updated_at = now()",
    params = list(student_id, as.character(state_json))
  )
}

#' Load placement state from the database
#'
#' @param pool Database connection pool
#' @param student_id Character UUID
#' @return Placement state list, or NULL if not found
load_placement_state_db <- function(pool, student_id) {
  row <- DBI::dbGetQuery(pool,
    "SELECT state FROM placement_sessions WHERE student_id = $1::uuid",
    params = list(student_id)
  )
  if (nrow(row) == 0) return(NULL)
  state <- jsonlite::fromJSON(row$state[1], simplifyVector = FALSE)
  # topo_order is saved as a JSON array and comes back as a list after
  # fromJSON(simplifyVector=FALSE). Convert to character vector so
  # state$topo_order[idx] returns a string, not a list.
  if (!is.null(state$topo_order)) {
    state$topo_order <- unlist(state$topo_order)
  }
  state
}

#' Remove placement state from the database
#'
#' @param pool Database connection pool
#' @param student_id Character UUID
remove_placement_state_db <- function(pool, student_id) {
  DBI::dbExecute(pool,
    "DELETE FROM placement_sessions WHERE student_id = $1::uuid",
    params = list(student_id)
  )
}
