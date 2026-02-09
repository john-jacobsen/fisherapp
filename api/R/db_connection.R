# =============================================================================
# Database Connection Pool
# =============================================================================

#' Create a database connection pool from environment variables
#'
#' @return A pool object
create_db_pool <- function() {
  pool::dbPool(
    drv      = RPostgres::Postgres(),
    host     = Sys.getenv("DB_HOST", "localhost"),
    port     = as.integer(Sys.getenv("DB_PORT", "5432")),
    dbname   = Sys.getenv("DB_NAME", "fisherapp"),
    user     = Sys.getenv("DB_USER", "fisherapp"),
    password = Sys.getenv("DB_PASSWORD", "changeme_in_production"),
    minSize  = 1,
    maxSize  = 5
  )
}
