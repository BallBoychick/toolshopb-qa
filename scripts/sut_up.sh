#!/usr/bin/env bash
set -euo pipefail

SUT_DIR="${SUT_DIR:-sut}"
SUT_REF="${SUT_REF:-main}"
export SPRINT="${SPRINT:-sprint5}"

if [ ! -d "$SUT_DIR/.git" ]; then
  git init -q "$SUT_DIR"
  git -C "$SUT_DIR" remote add origin https://github.com/testsmith-io/practice-software-testing.git
fi
git -C "$SUT_DIR" fetch --depth 1 origin "$SUT_REF"
git -C "$SUT_DIR" checkout -q FETCH_HEAD

cd "$SUT_DIR"
docker compose -f docker-compose.yml up -d

# БД и vendor могут быть ещё не готовы: повторяем миграцию с сидом
for i in $(seq 1 30); do
  if docker compose -f docker-compose.yml exec -T laravel-api php artisan migrate:refresh --seed; then
    break
  fi
  echo "API not ready yet (attempt $i), waiting..."; sleep 10
done

wait_for() {
  for i in $(seq 1 90); do
    curl -fsS -o /dev/null "$1" && { echo "$1 is up"; return 0; }
    sleep 10
  done
  echo "Timeout waiting for $1"; return 1
}
wait_for http://localhost:8091/products
wait_for http://localhost:4200