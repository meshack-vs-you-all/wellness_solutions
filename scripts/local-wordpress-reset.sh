#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="$ROOT_DIR/.env.wordpress"
COMPOSE_FILE="$ROOT_DIR/docker-compose.local.yml"

docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" down -v --remove-orphans
