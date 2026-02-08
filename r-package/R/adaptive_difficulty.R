# =============================================================================
# Adaptive Difficulty — Within-topic difficulty adjustment
# =============================================================================

#' Compute the next difficulty level based on recent performance
#'
#' Looks at the last \code{window} results to decide whether to promote,
#' demote, or hold the current difficulty level.
#'
#' @param topic_state A topic_state list
#' @param window Integer, number of recent results to consider (default 4)
#' @param promote_threshold Numeric, fraction correct to increase (default 0.75)
#' @param demote_threshold Numeric, fraction correct below which to decrease (default 0.25)
#' @return Integer 1-5, the recommended difficulty
#' @export
adjust_difficulty <- function(topic_state,
                              window = 4L,
                              promote_threshold = 0.75,
                              demote_threshold = 0.25) {
  current <- topic_state$difficulty
  results <- topic_state$last_n_results

  # Not enough data yet — hold

  if (length(results) < window) {
    return(current)
  }

  recent <- utils::tail(results, window)
  accuracy <- mean(recent)

  if (accuracy >= promote_threshold && current < 5L) {
    return(current + 1L)
  }
  if (accuracy <= demote_threshold && current > 1L) {
    return(current - 1L)
  }
  current
}
