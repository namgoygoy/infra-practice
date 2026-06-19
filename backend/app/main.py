import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import cache
from app.database import Base, engine
from app.routers import memos

logging.basicConfig(level=logging.INFO)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Memo API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(memos.router, prefix="/api")


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "redis": "ok" if cache.ping() else "unavailable",
    }
