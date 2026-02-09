# =============================================================================
# Integration Tests — API Endpoints
# =============================================================================
#
# These tests start a Plumber API in a background process and test with httr.
# Requires: running PostgreSQL, R packages plumber, httr, jsonlite, sodium.
#
# To run: ensure DB is up, then: Rscript -e "testthat::test_dir('tests/api')"

source("tests/api/helper-setup.R")

# Helper: make API requests
api_url <- function(path) {
  port <- Sys.getenv("TEST_API_PORT", "8888")
  paste0("http://localhost:", port, path)
}

# These tests are designed to be run manually against a running API.
# They will skip automatically if the API is not running.
skip_if_no_api <- function() {
  tryCatch(
    {
      res <- httr::GET(api_url("/health"), httr::timeout(2))
      if (httr::status_code(res) != 200) skip("API not running")
    },
    error = function(e) skip("API not running")
  )
}

test_that("GET /health returns ok", {
  skip_if_no_api()
  res <- httr::GET(api_url("/health"))
  body <- httr::content(res, "parsed")
  expect_equal(body$status, "ok")
})

test_that("GET /topics returns topic list", {
  skip_if_no_api()
  res <- httr::GET(api_url("/topics"))
  body <- httr::content(res, "parsed")
  expect_true(length(body) >= 8)
})

test_that("full student workflow: register -> session -> problem -> answer -> progress", {
  skip_if_no_api()
  skip_if_no_db()

  # Clean up first
  con <- get_test_con()
  clean_test_data(con)
  DBI::dbDisconnect(con)

  # 1. Register
  reg_res <- httr::POST(
    api_url("/students"),
    body = list(email = "workflow@test.edu", password = "test123", name = "Workflow Test"),
    encode = "json"
  )
  reg_body <- httr::content(reg_res, "parsed")
  expect_equal(httr::status_code(reg_res), 200)
  student_id <- reg_body$student_id
  expect_true(nchar(student_id) > 0)

  # 2. Login
  login_res <- httr::POST(
    api_url("/students/login"),
    body = list(email = "workflow@test.edu", password = "test123"),
    encode = "json"
  )
  login_body <- httr::content(login_res, "parsed")
  expect_equal(login_body$student_id, student_id)

  # 3. Start session
  sess_res <- httr::POST(
    api_url("/sessions"),
    body = list(student_id = student_id),
    encode = "json"
  )
  sess_body <- httr::content(sess_res, "parsed")
  expect_equal(httr::status_code(sess_res), 200)
  session_id <- sess_body$session_id
  expect_true(nchar(session_id) > 0)

  # 4. Get next problem
  prob_res <- httr::GET(api_url(paste0("/problems/next?student_id=", student_id)))
  prob_body <- httr::content(prob_res, "parsed")
  expect_equal(httr::status_code(prob_res), 200)
  expect_true(nchar(prob_body$problem_id) > 0)
  expect_true(nchar(prob_body$statement) > 0)
  # Should NOT contain the answer
  expect_null(prob_body$answer)
  expect_null(prob_body$solution_steps)

  # 5. Submit answer
  check_res <- httr::POST(
    api_url("/problems/check"),
    body = list(
      student_id = student_id,
      session_id = session_id,
      problem_id = prob_body$problem_id,
      answer = "wrong_answer"
    ),
    encode = "json"
  )
  check_body <- httr::content(check_res, "parsed")
  expect_equal(httr::status_code(check_res), 200)
  expect_false(check_body$correct)
  expect_true(nchar(check_body$correct_answer) > 0)
  expect_true(length(check_body$solution_steps) > 0)

  # 6. End session
  end_res <- httr::POST(api_url(paste0("/sessions/", session_id, "/end")))
  end_body <- httr::content(end_res, "parsed")
  expect_equal(httr::status_code(end_res), 200)
  expect_equal(end_body$problems_served, 1)

  # 7. Check progress
  prog_res <- httr::GET(api_url(paste0("/students/", student_id, "/progress")))
  prog_body <- httr::content(prog_res, "parsed")
  expect_equal(prog_body$total_attempts, 1)
  expect_equal(prog_body$total_correct, 0)
})

test_that("duplicate email registration fails", {
  skip_if_no_api()
  skip_if_no_db()

  con <- get_test_con()
  clean_test_data(con)
  DBI::dbDisconnect(con)

  # Register once
  httr::POST(
    api_url("/students"),
    body = list(email = "dupe@test.edu", password = "pw1", name = "First"),
    encode = "json"
  )

  # Try duplicate
  res <- httr::POST(
    api_url("/students"),
    body = list(email = "dupe@test.edu", password = "pw2", name = "Second"),
    encode = "json"
  )
  body <- httr::content(res, "parsed")
  expect_equal(httr::status_code(res), 400)
})

test_that("wrong password login fails", {
  skip_if_no_api()
  skip_if_no_db()

  con <- get_test_con()
  clean_test_data(con)
  DBI::dbDisconnect(con)

  httr::POST(
    api_url("/students"),
    body = list(email = "wrongpw@test.edu", password = "correct", name = "Test"),
    encode = "json"
  )

  res <- httr::POST(
    api_url("/students/login"),
    body = list(email = "wrongpw@test.edu", password = "wrong"),
    encode = "json"
  )
  expect_equal(httr::status_code(res), 401)
})
