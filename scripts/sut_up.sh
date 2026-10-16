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
DC="docker compose -f docker-compose.yml"

fix_permissions() {
  $DC exec -T -u root laravel-api sh -c \
    'mkdir -p storage/logs storage/framework/cache storage/framework/sessions storage/framework/views bootstrap/cache \
     && chmod -R 777 storage bootstrap/cache'
}

$DC up -d

# 1. Права до того, как composer начнёт писать кэш, и перезапуск composer
fix_permissions
$DC restart composer || true

# 2. Ждём, пока composer закончит (признак: package:discover создал packages.php)
for i in $(seq 1 60); do
  if $DC exec -T laravel-api test -f bootstrap/cache/packages.php; then
    echo "Composer install finished"; break
  fi
  echo "Waiting for composer (attempt $i)..."; sleep 10
done

# 3. Файлы, созданные под root, должны быть доступны PHP-FPM
fix_permissions

# 4. Миграция с сидом (повторяем, пока БД не готова); если не вышло, падаем сразу
ok=0
for i in $(seq 1 30); do
  if $DC exec -T laravel-api php artisan migrate:refresh --seed; then ok=1; break; fi
  echo "Migration failed (attempt $i), retrying..."; sleep 10
done
[ "$ok" = 1 ] || { echo "Migration never succeeded"; exit 1; }

# 5. FULLTEXT-индекс для /products/search (без него поиск отвечает 500)
$DC exec -T laravel-api php artisan tinker \
  --execute="try { DB::statement('ALTER TABLE products ADD FULLTEXT INDEX products_name_fulltext (name)'); } catch (Throwable \$e) { echo 'fulltext index: '.\$e->getMessage(); }"

fix_permissions

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