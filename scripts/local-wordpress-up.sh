#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="$ROOT_DIR/.env.wordpress"
ENV_EXAMPLE="$ROOT_DIR/.env.wordpress.example"
COMPOSE_FILE="$ROOT_DIR/docker-compose.local.yml"

if [[ ! -f "$ENV_FILE" ]]; then
  cp "$ENV_EXAMPLE" "$ENV_FILE"
  echo "Created $ENV_FILE from template."
fi

set -a
source "$ENV_FILE"
set +a

if [[ ! -d "$ROOT_DIR/frontend/node_modules" ]]; then
  (
    cd "$ROOT_DIR/frontend"
    npm install
  )
fi

if [[ "${FORCE_FRONTEND_BUILD:-0}" == "1" || ! -f "$ROOT_DIR/wordpress/wp-content/themes/wellness-solutions/assets/app/.vite/manifest.json" ]]; then
  (
    cd "$ROOT_DIR/frontend"
    npm run build:wordpress
  )
fi

docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" up -d db wordpress

for _ in {1..60}; do
  if curl -fsS "$WORDPRESS_SITE_URL/wp-login.php" >/dev/null 2>&1; then
    break
  fi
  sleep 2
done

if ! docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" run --rm wp-cli core is-installed >/dev/null 2>&1; then
  docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" run --rm wp-cli core install \
    --url="$WORDPRESS_SITE_URL" \
    --title="$WORDPRESS_SITE_TITLE" \
    --admin_user="$WORDPRESS_ADMIN_USER" \
    --admin_password="$WORDPRESS_ADMIN_PASSWORD" \
    --admin_email="$WORDPRESS_ADMIN_EMAIL" \
    --skip-email
fi

docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" run --rm wp-cli rewrite structure '/%postname%/' --hard >/dev/null
docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" run --rm wp-cli theme activate wellness-solutions >/dev/null

APP_PAGE_ID="$(
  docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" run --rm wp-cli post list \
    --post_type=page \
    --name=wellness-app \
    --field=ID 2>/dev/null | tr -d '\r'
)"

if [[ -z "$APP_PAGE_ID" ]]; then
  APP_PAGE_ID="$(
    docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" run --rm wp-cli post create \
      --post_type=page \
      --post_status=publish \
      --post_title='Wellness App' \
      --post_name='wellness-app' \
      --porcelain | tr -d '\r'
  )"
fi

docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" run --rm wp-cli post meta update \
  "$APP_PAGE_ID" \
  _wp_page_template \
  page-app-shell.php >/dev/null

echo "WordPress site: $WORDPRESS_SITE_URL"
echo "WordPress admin: $WORDPRESS_SITE_URL/wp-admin/"
echo "App shell page: $WORDPRESS_SITE_URL/wellness-app/"
