FROM rocker/r-ver:4.3.0

# System dependencies for RPostgres and other packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    zlib1g-dev \
    libsodium-dev \
    && rm -rf /var/lib/apt/lists/*

# Install R package dependencies
RUN R -e "install.packages(c( \
    'plumber', \
    'DBI', \
    'RPostgres', \
    'pool', \
    'jsonlite', \
    'yaml', \
    'uuid', \
    'glue', \
    'stringr', \
    'sodium', \
    'httr', \
    'openssl' \
  ), repos = 'https://cran.r-project.org')"

# Install the fisherapp R package
COPY r-package /tmp/r-package
RUN R -e "install.packages('/tmp/r-package', repos = NULL, type = 'source')" \
    && rm -rf /tmp/r-package

# Copy the API layer
COPY api /app/api
WORKDIR /app

EXPOSE 8000

CMD ["Rscript", "api/run.R"]
