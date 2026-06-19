# 1단계: 메모장 서비스

## 수행 내용

- **FE**: Vite + React + TypeScript로 메모 목록/작성/수정/삭제 UI 구현
- **BE**: FastAPI + SQLAlchemy로 CRUD API 구현
- **DB**: `docker-compose.yml`로 PostgreSQL 로컬 구성
- **연동**: Vite dev server proxy(`/api` → `localhost:8000`)로 FE-BE 통신

## 프로젝트 구조

```
backend/app/   main, models, schemas, crud, routers/memos
frontend/src/  api/memos.ts, App.tsx
docker-compose.yml
```

## 엔드포인트 설계

RESTful 리소스 `/api/memos` 기준으로 CRUD 매핑.

| Method | Path | 역할 | 응답 |
|--------|------|------|------|
| GET | `/api/memos` | 목록 조회 | `Memo[]` |
| GET | `/api/memos/{id}` | 상세 조회 | `Memo` / 404 |
| POST | `/api/memos` | 생성 | `Memo` (201) |
| PUT | `/api/memos/{id}` | 수정 | `Memo` / 404 |
| DELETE | `/api/memos/{id}` | 삭제 | 204 / 404 |

**설계 포인트**

- URL은 명사(`memos`), 동작은 HTTP Method로 표현
- 요청/응답은 Pydantic 스키마로 분리 (`MemoCreate`, `MemoUpdate`, `MemoResponse`)
- DB 접근은 `crud.py`, 라우팅은 `routers/memos.py`로 계층 분리
- 없는 리소스는 `404`, 생성은 `201`, 삭제는 본문 없는 `204`

**Memo 스키마**: `id`, `title`, `content`, `created_at`, `updated_at`

## 실행

```bash
docker compose up -d
cd backend && source .venv/bin/activate && uvicorn app.main:app --reload --port 8000
cd frontend && npm run dev
```

- 앱: http://localhost:5173
- API 문서: http://localhost:8000/docs
