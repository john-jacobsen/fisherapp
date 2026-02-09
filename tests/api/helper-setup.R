# =============================================================================
# Test Helper — Database setup/teardown for API integration tests
# =============================================================================
#
# These tests require a running PostgreSQL instance. Set environment variables:
#   DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
#
# To run: Rscript -e "testthat::test_dir('tests/api')"
# Or with Docker: docker-compose up db, then run tests locally.

library(testthat)
library(DBI)
library(RPostgres)
library(fisherapp)

# Skip all tests if no database connection available
skip_if_no_db <- function() {
  tryCatch(
    {
      con <- DBI::dbConnect(
        RPostgres::Postgres(),
        host     = Sys.getenv("DB_HOST", "localhost"),
        port     = as.integer(Sys.getenv("DB_PORT", "5432")),
        dbname   = Sys.getenv("DB_NAME", "fisherapp"),
        user     = Sys.getenv("DB_USER", "fisherapp"),
        password = Sys.getenv("DB_PASSWORD", "changeme_in_production")
      )
      DBI::dbDisconnect(con)
    },
    error = function(e) {
      skip("Database not available")
    }
  )
}

# Get a fresh database connection for testing
get_test_con <- function() {
  DBI::dbConnect(
    RPostgres::Postgres(),
    host     = Sys.getenv("DB_HOST", "localhost"),
    port     = as.integer(Sys.getenv("DB_PORT", "5432")),
    dbname   = Sys.getenv("DB_NAME", "fisherapp"),
    user     = Sys.getenv("DB_USER", "fisherapp"),
    password = Sys.getenv("DB_PASSWORD", "changeme_in_production")
  )
}

# Clean test data (remove all rows but keep schema)
clean_test_data <- function(con) {
  DBI::dbExecute(con, "DELETE FROM problem_attempts")
  DBI::dbExecute(con, "DELETE FROM mastery_states")
  DBI::dbExecute(con, "DELETE FROM sessions")
  DBI::dbExecute(con, "DELETE FROM students")
}
