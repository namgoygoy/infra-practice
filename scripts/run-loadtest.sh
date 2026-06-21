#!/usr/bin/env bash
# 점진적 부하 테스트 (headless)
# 사용: ./scripts/run-loadtest.sh http://[EC2_PUBLIC_IP]:8000 MemoReader

set -euo pipefail

HOST="${1:-http://localhost:8000}"
USER_CLASS="${2:-MemoReader}"
DURATION="${3:-60s}"

echo "Target: $HOST"
echo "User class: $USER_CLASS"
echo "Duration per step: $DURATION"
echo

for USERS in 10 50 100; do
  SPAWN_RATE=$((USERS / 10))
  [ "$SPAWN_RATE" -lt 1 ] && SPAWN_RATE=1

  echo "=== Users: $USERS | Spawn rate: $SPAWN_RATE/s ==="
  locust \
    --headless \
    --host "$HOST" \
    --users "$USERS" \
    --spawn-rate "$SPAWN_RATE" \
    --run-time "$DURATION" \
    --only-summary \
    --html "loadtest-results/${USER_CLASS}-users-${USERS}.html" \
    --csv "loadtest-results/${USER_CLASS}-users-${USERS}" \
    "$USER_CLASS"
  echo
done

echo "Results saved to loadtest-results/"
