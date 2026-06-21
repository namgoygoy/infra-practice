#!/usr/bin/env bash
# Gunicorn 워커 수별 Locust 부하 테스트 비교
# 사용: ./scripts/compare-gunicorn-workers.sh http://[퍼블릭 IP]:8000

set -euo pipefail

HOST="${1:-http://localhost:8000}"
USERS="${2:-50}"
DURATION="${3:-60s}"
COMPOSE_DIR="${COMPOSE_DIR:-.}"

mkdir -p loadtest-results

for WORKERS in 1 2 4; do
  echo "=== GUNICORN_WORKERS=$WORKERS ==="
  GUNICORN_WORKERS="$WORKERS" docker compose -f "$COMPOSE_DIR/docker-compose.yml" up -d --build app
  sleep 5

  locust \
    --headless \
    --host "$HOST" \
    --users "$USERS" \
    --spawn-rate "$((USERS / 10))" \
    --run-time "$DURATION" \
    --only-summary \
    --html "loadtest-results/gunicorn-workers-${WORKERS}-users-${USERS}.html" \
    --csv "loadtest-results/gunicorn-workers-${WORKERS}-users-${USERS}" \
    MemoReader

  echo
done

echo "Results saved to loadtest-results/gunicorn-workers-*.html"
