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

WORDPRESS_EXEC=(
  docker compose
  --env-file "$ENV_FILE"
  -f "$COMPOSE_FILE"
  exec
  wordpress
)

for _ in {1..60}; do
  if "${WORDPRESS_EXEC[@]}" sh -lc "curl -fsS http://127.0.0.1/wp-login.php >/dev/null" >/dev/null 2>&1; then
    break
  fi
  sleep 2
done

"${WORDPRESS_EXEC[@]}" \
  env \
  WORDPRESS_SITE_TITLE="$WORDPRESS_SITE_TITLE" \
  WORDPRESS_ADMIN_USER="$WORDPRESS_ADMIN_USER" \
  WORDPRESS_ADMIN_PASSWORD="$WORDPRESS_ADMIN_PASSWORD" \
  WORDPRESS_ADMIN_EMAIL="$WORDPRESS_ADMIN_EMAIL" \
  php /workspace-scripts/local-wordpress-bootstrap.php >/dev/null

echo "WordPress site: $WORDPRESS_SITE_URL"
echo "WordPress admin: $WORDPRESS_SITE_URL/wp-admin/"
echo "App shell page: $WORDPRESS_SITE_URL/wellness-app/"
