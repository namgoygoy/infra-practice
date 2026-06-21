# 5단계: Locust 부하 테스트

## 준비

```bash
pip install -r requirements-locust.txt
mkdir -p loadtest-results
```

대상 서버: EC2 퍼블릭 IP 또는 로컬 `http://localhost:8000`

## 시나리오

| User 클래스 | 역할 | API |
|-------------|------|-----|
| `MemoReader` | 읽기 집중 | `GET /api/memos`, `GET /api/memos/{id}`, `GET /health` |
| `MemoWriter` | 쓰기 집중 | `POST /api/memos` |

기본 실행 시 `MemoReader:MemoWriter = 3:1` (읽기 비중).

## 실행

### Web UI (권장)

```bash
locust --host http://[퍼블릭 IP]:8000
```

브라우저 `http://localhost:8089` → Users·Spawn rate 설정 후 Start.

### Headless (점진적 부하)

```bash
chmod +x scripts/run-loadtest.sh

# 읽기 집중: 10 → 50 → 100 users
./scripts/run-loadtest.sh http://[퍼블릭 IP]:8000 MemoReader

# 쓰기 집중
./scripts/run-loadtest.sh http://[퍼블릭 IP]:8000 MemoWriter
```

결과: `loadtest-results/` (HTML, CSV)

## EC2 모니터링

부하 테스트 중 EC2 SSH 접속 후:

```bash
top          # CPU / Memory
docker stats # 컨테이너별 리소스
docker logs memo-api --tail 50   # Cache HIT/MISS
```

## Gunicorn 멀티프로세싱 비교

백엔드는 `Gunicorn + UvicornWorker`로 실행됩니다. 워커 수를 바꿔 Locust로 지연율을 비교합니다.

| 설정 | 파일 |
|------|------|
| Gunicorn 설정 | `backend/gunicorn.conf.py` |
| 워커 수 | 환경변수 `GUNICORN_WORKERS` (기본 4) |

### 워커 수 변경 후 재배포

```bash
# 단일 프로세스 (비교 기준)
GUNICORN_WORKERS=1 docker compose up -d --build app

# 멀티 워커
GUNICORN_WORKERS=4 docker compose up -d --build app
```

워커 프로세스 확인:

```bash
docker exec memo-api ps aux | grep gunicorn
```

### Locust 비교 테스트

동일 조건(Users 50, 60s)으로 워커 1 → 2 → 4 순서 테스트:

```bash
chmod +x scripts/compare-gunicorn-workers.sh
./scripts/compare-gunicorn-workers.sh http://[퍼블릭 IP]:8000
```

| Workers | RPS | 평균(ms) | p95(ms) | 실패율 |
|---------|------|----------|---------|--------|
| 1 | | | | |
| 2 | | | | |
| 4 | | | | |

## Redis 캐시 비교

1. **캐시 ON**: Redis 컨테이너 실행 상태에서 `MemoReader` 테스트
2. **캐시 OFF**: `docker stop memo-redis` 후 동일 조건 재테스트 (DB fallback)

| 항목 | 캐시 ON | 캐시 OFF |
|------|--------|---------|
| 평균 응답(ms) | | |
| RPS | | |
| 실패율 | | |

## 결과 정리 (회고)

| Users | RPS | 평균(ms) | p95(ms) | 실패율 | 비고 |
|-------|------|----------|---------|--------|------|
| 10 | | | | | |
| 50 | | | | | |
| 100 | | | | | |

- 병목 지점:
- 개선 아이디어:
