# =============================================================================
# SM-2 Engine — Modified spaced repetition algorithm
# =============================================================================

# Default time scale: 1 interval unit = 1 day (86400 seconds)
# Override with options(fisherapp.time_scale = 60) for testing (1 min = 1 "day")
.time_scale <- function() {
  getOption("fisherapp.time_scale", default = 86400)
}

#' Map a correct/incorrect result to SM-2 quality score (0-5)
#'
#' Simplified mapping for problem-solving context:
#' \itemize{
#'   \item 5: correct at or above working difficulty
#'   \item 4: correct one level below working difficulty
#'   \item 3: correct two or more levels below
#'   \item 2: first incorrect answer
#'   \item 1: repeated incorrect (2nd in a row)
#'   \item 0: 3+ consecutive wrong (blackout)
#' }
#'
#' @param correct Logical. Was the answer correct?
#' @param problem_difficulty Integer 1-5. Difficulty of the problem presented.
#' @param working_difficulty Integer 1-5. Student's current working difficulty.
#' @param consecutive_wrong Integer. Count of consecutive wrong answers.
#' @return Integer 0-5
#' @export
map_quality <- function(correct, problem_difficulty, working_difficulty,
                        consecutive_wrong = 0L) {
  if (correct) {
    gap <- working_difficulty - problem_difficulty
    if (gap <= 0) return(5L)
    if (gap == 1) return(4L)
    return(3L)
  } else {
    if (consecutive_wrong >= 3) return(0L)
    if (consecutive_wrong >= 1) return(1L)
    return(2L)
  }
}

#' Update SM-2 parameters after a review
#'
#' Pure function: takes current topic_state and quality score, returns
#' an updated topic_state. Implements the standard SM-2 algorithm with
#' intervals of 1 day, 6 days, then interval * ease_factor.
#'
#' @param topic_state A topic_state list
#' @param quality Integer 0-5. SM-2 quality score.
#' @param review_time POSIXct. When the review occurred (default: now).
#' @return Updated topic_state list
#' @export
sm2_update <- function(topic_state, quality, review_time = Sys.time()) {
  stopifnot(quality >= 0, quality <= 5)

  # Update ease factor
  new_ef <- topic_state$ease_factor +
    (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
  new_ef <- max(1.3, new_ef)

  if (quality >= 3) {
    # Successful recall
    if (topic_state$repetition == 0L) {
      new_interval <- 1
    } else if (topic_state$repetition == 1L) {
      new_interval <- 6
    } else {
      new_interval <- round(topic_state$interval * new_ef)
    }
    new_rep <- topic_state$repetition + 1L
  } else {
    # Failed recall — reset
    new_rep <- 0L
    new_interval <- 1
  }

  new_next_review <- review_time + (new_interval * .time_scale())

  topic_state$ease_factor <- new_ef
  topic_state$interval    <- new_interval
  topic_state$repetition  <- new_rep
  topic_state$next_review <- new_next_review
  topic_state
}

#' Check if a topic is due for review
#'
#' @param topic_state A topic_state list
#' @param current_time POSIXct (default: now)
#' @return Logical
#' @export
is_due_for_review <- function(topic_state, current_time = Sys.time()) {
  current_time >= topic_state$next_review
}
