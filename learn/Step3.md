# 3단계: AWS EC2 & Docker 수동 배포

## 수행 내용

- **인프라 구축**: AWS EC2(Ubuntu) 인스턴스 생성, 퍼블릭 고정 IP(Elastic IP) 연결
- **보안 설정**: Security Group에서 필요 포트만 개방 (SSH 22, FE 5173, BE 8000)
- **SSH 키 관리**: `*.pem` 파일을 `~/.ssh`로 이동, 권한 `400` 설정
- **환경 구축**: EC2에 SSH 접속 후 Docker 및 Docker Compose 설치
- **수동 배포**: GitHub에 코드 push → EC2에서 `git clone` → `docker compose up -d --build`
- **외부 접속 검증**: 퍼블릭 IP로 API 문서 및 메모장 앱 접속 확인

## 인프라 구조

외부 유저가 퍼블릭 IP와 개방 포트를 통해 EC2 내부 Docker 컨테이너에 접근하는 구조.

```
[ 외부 유저 / 브라우저 ]
         │
         ▼ (인터넷)
[ AWS EC2 (Ubuntu) ] ── Security Group (인바운드 규칙)
         │
         ├─ Port 5173 → [ Vite Frontend 컨테이너 ]
         ├─ Port 8000 → [ FastAPI Backend 컨테이너 ]
         │                    │
         │                    ├─ [ Redis ]   (내부 통신)
         │                    └─ [ PostgreSQL ] (내부 통신)
```

DB·Redis 포트(5432, 6379)는 Security Group에서 열지 않고, Docker 내부 네트워크에서만 통신.

## Security Group (인바운드 규칙)

| 서비스 | 프로토콜 | 포트 | 소스 | 용도 |
|--------|----------|------|------|------|
| SSH | TCP | 22 | `0.0.0.0/0` | EC2 원격 접속 |
| Frontend | TCP | 5173 | `0.0.0.0/0` | 메모장 UI |
| Backend | TCP | 8000 | `0.0.0.0/0` | API / Swagger |

**설계 포인트**

- Free Tier 사용량 알림 설정으로 예기치 않은 과금 방지
- HTTP 기본 포트(80/443) 대신 프로젝트 포트(5173, 8000) 직접 사용
- DB·Redis는 외부에 노출하지 않음


### 접속 확인

- API 문서: `http://[퍼블릭 IP]:8000/docs`
- 메모장 UI: `http://[퍼블릭 IP]:5173`

## EC2 내부에 저장되는 것

`docker compose up -d --build` 실행 후 EC2에는 아래 4가지가 존재합니다.

### 1. 소스 코드 (`~/app`)

GitHub에서 `git clone`한 프로젝트 원본 파일.

| 경로 | 내용 |
|------|------|
| `frontend/` | React + TypeScript UI 코드 |
| `backend/` | FastAPI, SQLAlchemy, Redis 캐시(`cache.py`) |
| `docker-compose.yml` | 컨테이너 구성 설계도 |

### 2. Docker Images

코드를 실행 가능한 형태로 빌드·압축해 둔 이미지.

- FastAPI 백엔드 이미지 (Python 포함)
- Vite 프론트엔드 이미지 (Node.js 빌드)
- PostgreSQL 16 (공식 이미지)
- Redis 7 (공식 이미지)

### 3. Running Containers

이미지를 기반으로 RAM 위에서 실행 중인 프로세스 (4개).

| 컨테이너 | 역할 |
|----------|------|
| Frontend | 외부 요청 대기 (Port 5173) |
| Backend | API 처리 (Port 8000) |
| Redis | 캐시 조회 (Cache HIT/MISS) |
| PostgreSQL | 메모 데이터 저장 |

### 4. DB Volume (영구 데이터)

컨테이너는 종료되면 내부 데이터가 사라집니다. 이를 방지하기 위해 `docker-compose.yml`에서 PostgreSQL 데이터를 EC2 디스크에 Volume으로 연결합니다.

```yaml
volumes:
  - postgres_data:/var/lib/postgresql/data
```

**PostgreSQL (영구 저장)**

- 메모 `title`, `content`, `created_at`, `updated_at` 등이 EC2 디스크에 보존
- 서버를 재시작해도 데이터 유지

**Redis (휘발성 캐시)**

- RAM에만 저장 → EC2 재부팅 시 캐시 초기화
- 이후 조회 시 DB에서 다시 읽어와 캐시 재생성 (Cache MISS → HIT)