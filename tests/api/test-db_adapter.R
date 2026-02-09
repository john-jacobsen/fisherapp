# =============================================================================
# Integration Tests — Database Adapter
# =============================================================================

source("tests/api/helper-setup.R")

test_that("create_student_in_db inserts student and mastery rows", {
  skip_if_no_db()
  con <- get_test_con()
  on.exit({ clean_test_data(con); DBI::dbDisconnect(con) })

  student <- create_student_in_db(con, "test@berkeley.edu", "hashed_pw",
                                  display_name = "Test Student")

  # Check student row exists
  row <- DBI::dbGetQuery(con,
    "SELECT * FROM students WHERE student_id = $1",
    params = list(student$student_id))
  expect_equal(nrow(row), 1)
  expect_equal(row$email[1], "test@berkeley.edu")
  expect_equal(row$display_name[1], "Test Student")

  # Check mastery rows initialized
  mastery <- DBI::dbGetQuery(con,
    "SELECT * FROM mastery_states WHERE student_id = $1",
    params = list(student$student_id))
  active_topics <- get_active_topics()
  expect_equal(nrow(mastery), length(active_topics))
  expect_true(all(mastery$mastery_state == "not_started"))
})

test_that("load_student_model reconstructs from DB", {
  skip_if_no_db()
  con <- get_test_con()
  on.exit({ clean_test_data(con); DBI::dbDisconnect(con) })

  original <- create_student_in_db(con, "load@test.edu", "pw_hash")
  loaded <- load_student_model(con, original$student_id)

  expect_s3_class(loaded, "student_model")
  expect_equal(loaded$student_id, original$student_id)
  expect_equal(loaded$total_attempts, 0L)
  expect_equal(loaded$total_correct, 0L)
  expect_equal(length(loaded$topics), length(get_active_topics()))
  expect_null(loaded$current_session)

  # Check topic states
  for (tid in get_active_topics()) {
    ts <- loaded$topics[[tid]]
    expect_equal(ts$mastery_state, "not_started")
    expect_equal(ts$difficulty, 1L)
    expect_equal(ts$ease_factor, 2.5)
  }
})

test_that("save_student_model persists changes", {
  skip_if_no_db()
  con <- get_test_con()
  on.exit({ clean_test_data(con); DBI::dbDisconnect(con) })

  student <- create_student_in_db(con, "save@test.edu", "pw_hash")

  # Modify student state
  student$total_attempts <- 10L
  student$total_correct <- 8L
  student$topics[["fraction_arithmetic"]]$mastery_state <- "in_progress"
  student$topics[["fraction_arithmetic"]]$difficulty <- 3L
  student$topics[["fraction_arithmetic"]]$attempt_count <- 10L
  student$topics[["fraction_arithmetic"]]$correct_count <- 8L
  student$topics[["fraction_arithmetic"]]$last_n_results <- c(1L, 1L, 0L, 1L, 1L)

  save_student_model(con, student)

  # Reload and verify
  reloaded <- load_student_model(con, student$student_id)
  expect_equal(reloaded$total_attempts, 10L)
  expect_equal(reloaded$total_correct, 8L)

  fa <- reloaded$topics[["fraction_arithmetic"]]
  expect_equal(fa$mastery_state, "in_progress")
  expect_equal(fa$difficulty, 3L)
  expect_equal(fa$attempt_count, 10L)
  expect_equal(fa$correct_count, 8L)
  expect_equal(fa$last_n_results, c(1L, 1L, 0L, 1L, 1L))
})

test_that("session lifecycle persists correctly", {
  skip_if_no_db()
  con <- get_test_con()
  on.exit({ clean_test_data(con); DBI::dbDisconnect(con) })

  student <- create_student_in_db(con, "session@test.edu", "pw_hash")
  student <- start_session(student)
  save_session_start(con, student)

  # Verify session row
  sess_row <- DBI::dbGetQuery(con,
    "SELECT * FROM sessions WHERE session_id = $1",
    params = list(student$current_session$session_id))
  expect_equal(nrow(sess_row), 1)
  expect_true(is.na(sess_row$ended_at[1]) || is.null(sess_row$ended_at[1]))

  # End session
  session_id <- student$current_session$session_id
  student <- end_session(student)
  save_session_end(con, student, session_id)

  # Verify ended
  sess_row2 <- DBI::dbGetQuery(con,
    "SELECT * FROM sessions WHERE session_id = $1",
    params = list(session_id))
  expect_false(is.na(sess_row2$ended_at[1]))
})

test_that("save_attempt inserts problem attempt row", {
  skip_if_no_db()
  con <- get_test_con()
  on.exit({ clean_test_data(con); DBI::dbDisconnect(con) })

  student <- create_student_in_db(con, "attempt@test.edu", "pw_hash")
  student <- start_session(student)
  save_session_start(con, student)

  prob <- generate_problem("fraction_arithmetic", 2, seed = 42)
  result <- check_answer(prob, prob$answer)

  save_attempt(con, student$current_session$session_id,
               student$student_id, prob, prob$answer, result, 1L)

  attempts <- DBI::dbGetQuery(con,
    "SELECT * FROM problem_attempts WHERE session_id = $1",
    params = list(student$current_session$session_id))
  expect_equal(nrow(attempts), 1)
  expect_equal(attempts$topic_id[1], "fraction_arithmetic")
  expect_equal(attempts$difficulty[1], 2L)
  expect_true(attempts$is_correct[1])
})

test_that("lookup_student_by_email works", {
  skip_if_no_db()
  con <- get_test_con()
  on.exit({ clean_test_data(con); DBI::dbDisconnect(con) })

  student <- create_student_in_db(con, "lookup@test.edu", "pw_hash")

  found <- lookup_student_by_email(con, "lookup@test.edu")
  expect_equal(found$student_id[1], student$student_id)

  not_found <- lookup_student_by_email(con, "missing@test.edu")
  expect_null(not_found)
})

test_that("load_student_model returns NULL for missing student", {
  skip_if_no_db()
  con <- get_test_con()
  on.exit(DBI::dbDisconnect(con))

  result <- load_student_model(con, "00000000-0000-0000-0000-000000000000")
  expect_null(result)
})

test_that("parse_pg_int_array handles edge cases", {
  expect_equal(parse_pg_int_array("{}"), integer(0))
  expect_equal(parse_pg_int_array(NULL), integer(0))
  expect_equal(parse_pg_int_array(NA), integer(0))
  expect_equal(parse_pg_int_array(""), integer(0))
  expect_equal(parse_pg_int_array("{1,0,1}"), c(1L, 0L, 1L))
  expect_equal(parse_pg_int_array("{0}"), 0L)
})

test_that("format_pg_int_array formats correctly", {
  expect_equal(format_pg_int_array(integer(0)), "{}")
  expect_equal(format_pg_int_array(c(1L, 0L, 1L)), "{1,0,1}")
  expect_equal(format_pg_int_array(0L), "{0}")
})
