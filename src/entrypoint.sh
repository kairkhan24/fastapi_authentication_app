#!/usr/bin/env bash

wait_for_postgres() {
  until pg_isready -h postgres -p 5432 -U postgres -d postgres -q; do
    echo "PostgreSQL is not ready yet. Waiting..."
    sleep 1
  done
  echo "PostgreSQL is ready."
}

set -e

DEFAULT_MODULE_NAME=src.main

MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-app}
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8000}
LOG_LEVEL=${LOG_LEVEL:-info}
LOG_CONFIG=${LOG_CONFIG:-/app/logging.ini}

## Implemention
echo "Waiting for postgres..."
wait_for_postgres

# Migrate
alembic upgrade head

# Start Uvicorn with live reload
exec uvicorn --reload --proxy-headers --host $HOST --port $PORT --log-config $LOG_CONFIG "$APP_MODULE"