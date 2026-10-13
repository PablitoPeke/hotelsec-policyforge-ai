#!/usr/bin/env bash
# Private same-VPS checkpoint, including a restore rehearsal in a separate database.
set -euo pipefail
umask 077
test "$(id -u)" = 0 || { echo 'Run as root on the authorized VPS.' >&2; exit 1; }
checkout=/opt/hotelsec-policyforge-ai-practica3
db=hotelsec-p3-prod-db-1
stamp=$(date -u +%Y%m%dT%H%M%SZ)
backup="/root/hotelsec-backups/p3-before-update-$stamp"
scratch="backup_check_$(date -u +%Y%m%d%H%M%S)_$$"
mkdir -p "$backup"
docker exec "$db" pg_dump -U hotelsec -d hotelsec -Fc > "$backup/database.backup"
test -s "$backup/database.backup"
docker exec -i "$db" pg_restore --list < "$backup/database.backup" > "$backup/database-contents.txt"
docker exec "$db" createdb -U hotelsec "$scratch"
cleanup() { docker exec "$db" dropdb -U hotelsec --if-exists "$scratch" >/dev/null; }
trap cleanup EXIT
docker exec -i "$db" pg_restore -U hotelsec --exit-on-error --no-owner -d "$scratch" < "$backup/database.backup"
docker exec "$db" psql -U hotelsec -d "$scratch" -Atc 'SELECT version_num FROM alembic_version' > "$backup/restored-schema.txt"
docker exec "$db" pg_dump -U hotelsec -d "$scratch" --schema-only --no-owner > "$backup/restored-schema.sql"
cp "$checkout/.env.production" "$backup/environment.private"
git -C "$checkout" rev-parse HEAD > "$backup/code-commit.txt"
git -C "$checkout" archive HEAD | gzip > "$backup/code.tar.gz"
for service in api web; do
  image=$(docker inspect --format '{{.Image}}' "hotelsec-p3-prod-$service-1")
  docker image tag "$image" "hotelsec-checkpoint-$service:$stamp"
  printf '%s %s\n' "$service" "$image" >> "$backup/images.txt"
  docker image save "hotelsec-checkpoint-$service:$stamp" | gzip > "$backup/$service-image.tar.gz"
  gzip -t "$backup/$service-image.tar.gz"
done
(
  cd "$backup"
  sha256sum database.backup environment.private code.tar.gz api-image.tar.gz web-image.tar.gz > SHA256SUMS
  sha256sum --check SHA256SUMS >/dev/null
)
printf 'Private backup and isolated PostgreSQL restore succeeded: %s\n' "$backup"
printf 'This is not an encrypted off-site backup. Live data was not replaced.\n'
