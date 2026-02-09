# =============================================================================
# BerkeleyStats Tutor — API Entry Point
# =============================================================================

library(plumber)

host <- Sys.getenv("API_HOST", "0.0.0.0")
port <- as.integer(Sys.getenv("API_PORT", "8000"))

pr <- plumber::plumb("api/plumber.R")
pr$run(host = host, port = port)
