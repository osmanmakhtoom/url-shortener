#!/bin/bash
set -e

DB_NAME="${DB_NAME:-shortener}"
DB_USER="${DB_USER:-shortener_user}"
DB_PASS="${DB_PASS:-supersecretpassword}"

echo "Initializing Postgres DB: $DB_NAME, User: $DB_USER"

psql -v ON_ERROR_STOP=1 --username "${DB_USER}" --dbname "${DB_NAME}" <<-EOSQL

-- Create role if it doesn't exist
DO
\$do\$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '${DB_USER}') THEN
      CREATE ROLE ${DB_USER} LOGIN PASSWORD '${DB_PASS}';
   END IF;
END
\$do\$;

-- Create database if it doesn't exist
DO
\$do\$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = '${DB_NAME}') THEN
      CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};
   END IF;
END
\$do\$;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER};

-- Optional schema
CREATE SCHEMA IF NOT EXISTS shortener_schema AUTHORIZATION ${DB_USER};

EOSQL

echo "Postgres initialization completed."
