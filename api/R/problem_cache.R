# =============================================================================
# Problem Cache — In-memory store for generated problems
# =============================================================================
# Problems are cached server-side between GET /problems/next and POST /problems/check.
# The client never sees the correct answer until after submission.

# Cache environment (private to this module)
.problem_cache <- new.env(parent = emptyenv())

# Cache TTL in seconds (30 minutes)
CACHE_TTL <- 1800

#' Store a problem in the cache
#'
#' @param problem A fisherapp_problem object
cache_problem <- function(problem) {
  .problem_cache[[problem$problem_id]] <- list(
    problem    = problem,
    created_at = Sys.time()
  )
}

#' Retrieve a problem from the cache
#'
#' @param problem_id Character UUID
#' @return The fisherapp_problem object, or NULL if not found/expired
get_cached_problem <- function(problem_id) {
  entry <- .problem_cache[[problem_id]]
  if (is.null(entry)) return(NULL)

  # Check TTL
  if (as.numeric(difftime(Sys.time(), entry$created_at, units = "secs")) > CACHE_TTL) {
    rm(list = problem_id, envir = .problem_cache)
    return(NULL)
  }

  entry$problem
}

#' Remove a problem from the cache
#'
#' @param problem_id Character UUID
remove_cached_problem <- function(problem_id) {
  if (exists(problem_id, envir = .problem_cache)) {
    rm(list = problem_id, envir = .problem_cache)
  }
}

#' Clean expired entries from the cache
clean_cache <- function() {
  now <- Sys.time()
  for (pid in ls(.problem_cache)) {
    entry <- .problem_cache[[pid]]
    if (as.numeric(difftime(now, entry$created_at, units = "secs")) > CACHE_TTL) {
      rm(list = pid, envir = .problem_cache)
    }
  }
}

# --- Placement state cache ---
# Placement tests need server-side state between requests.

.placement_cache <- new.env(parent = emptyenv())

#' Store placement state
#'
#' @param student_id Character UUID
#' @param state List with placement progress
cache_placement_state <- function(student_id, state) {
  .placement_cache[[student_id]] <- list(
    state      = state,
    created_at = Sys.time()
  )
}

#' Retrieve placement state
#'
#' @param student_id Character UUID
#' @return Placement state list, or NULL
get_placement_state <- function(student_id) {
  entry <- .placement_cache[[student_id]]
  if (is.null(entry)) return(NULL)
  # 1 hour TTL for placement
  if (as.numeric(difftime(Sys.time(), entry$created_at, units = "secs")) > 3600) {
    rm(list = student_id, envir = .placement_cache)
    return(NULL)
  }
  entry$state
}

#' Remove placement state
#'
#' @param student_id Character UUID
remove_placement_state <- function(student_id) {
  if (exists(student_id, envir = .placement_cache)) {
    rm(list = student_id, envir = .placement_cache)
  }
}
