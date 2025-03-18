#!/bin/bash
set -e

# Run the PostgreSQL initialization steps
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    ALTER USER postgres WITH PASSWORD 'zany12';
    CREATE EXTENSION IF NOT EXISTS vector;
EOSQL

# Add authentication configurations
echo "host all all 0.0.0.0/0 md5" >> /var/lib/postgresql/data/pg_hba.conf
echo "local all all trust" >> /var/lib/postgresql/data/pg_hba.conf 