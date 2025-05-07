#!/bin/sh
set -e

echo "Aspettando Postgres..."

POSTGRES_HOST=${POSTGRES_HOST:-postgres}
POSTGRES_PORT=${POSTGRES_PORT:-5432}

until nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  echo "Postgres non è ancora pronto - riprovo fra 5 secondi..."
  sleep 5
done

echo "Postgres è pronto! Avvio il backend."

exec uvicorn app.main:app --host 0.0.0.0 --port 8000
