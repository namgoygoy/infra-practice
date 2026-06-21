# 4단계: GitHub Actions CI/CD 파이프라인

## 파이프라인 개요

코드를 `main` 브랜치에 push하면 서버에 반영되기까지 3단계로 자동 실행됩니다.

```
[ 로컬 push ] → ① Trigger → ② CI (빌드·Push) → ③ CD (EC2 배포)
```

## ① Trigger

- 로컬에서 코드 수정 후 `git push origin main`
- `.github/workflows/ci-cd.yml`이 push 이벤트 감지
- GitHub Actions가 `ubuntu-latest` 러너에서 워크플로우 시작

## ② CI (지속적 통합)

1. 최신 소스코드 checkout
2. GitHub Secrets의 Docker Hub 인증 정보로 로그인
3. `frontend/`, `backend/` Dockerfile로 각각 이미지 빌드
4. Docker Hub에 `:latest` 태그로 push

| 이미지 | 태그 예시 |
|--------|-----------|
| Backend | `{DOCKER_USERNAME}/memo-backend:latest` |
| Frontend | `{DOCKER_USERNAME}/memo-frontend:latest` |

## ③ CD (지속적 배포)

CI 완료 후 GitHub Secrets(`EC2_HOST`, `EC2_SSH_KEY`)로 EC2에 SSH 접속하여 아래 명령을 순차 실행합니다.

| 명령 | 역할 |
|------|------|
| `git pull origin main` | 최신 코드·`docker-compose.yml` 동기화 |
| `docker compose pull` | Docker Hub에서 최신 FE/BE 이미지 다운로드 |
| `docker compose up -d --build` | 컨테이너 교체 및 재기동 |
| `docker image prune -f` | 미사용 이미지 삭제 (디스크 정리) |

## 배포 확인

- GitHub Actions 워크플로우 성공 여부 확인
- `http://[퍼블릭 IP]:5173` 접속 → 헤더 우측 **배포 확인 배지**(`v1.0.0`) 노출 확인
