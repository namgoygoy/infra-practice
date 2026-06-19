### 🗺️ 인프라 전 과정 실습 체크리스트

#### 🟩 1단계: 간단한 메모장 서비스 제작 (개발 기초)

* [x] **개발 환경 세팅 및 프레임워크 선정** (FE: Vite + React/TypeScript, BE: FastAPI + PostgreSQL)
* [x] **기본 CRUD 기능 구현**
* [x] 메모 작성 (Create)
* [x] 메모 목록 및 상세 조회 (Read)
* [x] 메모 수정 (Update)
* [x] 메모 삭제 (Delete)

* [x] **로컬 환경 데이터베이스(DB) 연동** (`docker-compose.yml`로 PostgreSQL 구성)
* [x] **API 기능 테스트 수행** (Postman 이나 브라우저를 통해 각 기능이 정상 작동하는지 확인)

#### 🟩 2단계: Docker + Redis 적용 (컨테이너화 및 캐싱)

* [x] **Redis 연동 코드 추가** (자주 조회하는 메모나 최근 메모를 Redis 캐시에 저장 및 조회하는 로직 구현)
* [x] **Dockerfile 작성** (애플리케이션을 컨테이너 이미지로 빌드하기 위한 스크립트 작성)
* [x] **`docker-compose.yml` 구성** (App 컨테이너와 Redis 컨테이너를 한 번에 띄우고 로컬 네트워크로 연결)
* [x] **로컬 컨테이너 환경 검증** (Docker Compose로 전체 서비스를 구동하고, Redis 캐싱이 제대로 동작하는지 로그 및 성능 확인)

#### 🟩 3단계: AWS EC2 & Docker 수동 배포 (클라우드 인프라 이해)

* [ ] **AWS 계정 생성 및 가상 네트워크(VPC/Subnet) 이해** (기본 VPC 활용 가능)
* [ ] **AWS EC2 인스턴스 생성** (Free Tier 인스턴스 활용, Ubuntu 등 OS 선택)
* [ ] **보안 그룹(Security Group) 설정** (App 포트, SSH 포트 등 꼭 필요한 포트만 인바운드 규칙 열기)
* [ ] **탄력적 IP(Elastic IP) 연결** (서버가 재시작되어도 IP가 바뀌지 않도록 설정)
* [ ] **EC2 서버 접속 및 환경 구축** (SSH로 접속 후 Docker 및 Docker Compose 설치)
* [ ] **수동 배포 진행** (로컬 코드를 EC2로 복사하거나 가상 서버에서 Git Clone 후 `docker-compose up -d` 실행)
* [ ] **외부 접속 테스트** (퍼블릭 IP를 통해 실제 브라우저에서 메모장 앱에 접속 가능한지 확인)

#### 🟩 4단계: GitHub Actions를 통한 CI/CD 파이프라인 구축 (배포 자동화)

* [ ] **Docker Hub(또는 AWS ECR) 레포지토리 생성** (빌드된 이미지를 저장할 공간)
* [ ] **GitHub Repository Secret 설정** (AWS 키, Docker Hub 패스워드 등 민감한 정보 안전하게 저장)
* [ ] **CI (지속적 통합) 워크플로우 작성** (`.github/workflows/ci-cd.yml`)
* [ ] 코드 푸시 시 자동으로 테스트 및 Docker 이미지 빌드
* [ ] 빌드된 이미지를 Docker Hub에 Push


* [ ] **CD (지속적 배포) 워크플로우 추가**
* [ ] EC2 서버에 SSH로 원격 접속하는 스크립트 작성
* [ ] 최신 Docker 이미지 다운로드(Pull) 및 기존 컨테이너 재시작(Restart) 자동화


* [ ] **자동 배포 확인** (코드를 수정 후 GitHub에 Push했을 때, 실제 서비스에 자동으로 반영되는지 최종 확인)

#### 🟩 5단계: 부하 테스트(Load Test) 체험 (인프라 성능 검증)

* [ ] **부하 테스트 툴 선정 및 설치** (Locust, Artillery, Apache JMeter 등 직관적인 툴 추천)
* [ ] **테스트 시나리오 작성**
* [ ] 메인 페이지/메모 목록 조회 (읽기 집중 부하)
* [ ] 짧은 시간 내에 대량의 메모 작성 요청 (쓰기 집중 부하)


* [ ] **점진적 부하 테스트 실행** (가상 유저 수를 10명 -> 50명 -> 100명으로 늘려가며 서버 반응 확인)
* [ ] **인프라 모니터링 및 병목 지점 파악**
* [ ] EC2 내부에서 `top` 또는 `htop` 명령어로 CPU/Memory 사용량 관찰
* [ ] 부하가 걸렸을 때 Redis 캐싱을 적용한 경우와 적용하지 않은 경우의 응답 속도(Latency) 차이 비교 분석


* [ ] **테스트 결과 정리 및 회고** (서버가 버틸 수 있는 최대 RPS(초당 요청 수) 파악 및 개선점 정리)
