"""
Locust 부하 테스트 시나리오 (5단계)

실행 예:
  pip install -r requirements-locust.txt
  locust --host http://[EC2_PUBLIC_IP]:8000

읽기 집중:
  locust --host http://localhost:8000 MemoReader

쓰기 집중:
  locust --host http://localhost:8000 MemoWriter

혼합 (기본):
  locust --host http://localhost:8000
"""

import os
import random
import uuid

from locust import HttpUser, between, task


class MemoReader(HttpUser):
    """메모 목록·상세 조회 (읽기 집중)"""

    weight = 3
    wait_time = between(0.5, 2)
    memo_ids: list[int] = []

    @task(3)
    def list_memos(self) -> None:
        response = self.client.get("/api/memos", name="GET /api/memos")
        if response.ok:
            memos = response.json()
            self.memo_ids = [memo["id"] for memo in memos]

    @task(1)
    def read_memo(self) -> None:
        if not self.memo_ids:
            self.list_memos()
            return

        memo_id = random.choice(self.memo_ids)
        self.client.get(f"/api/memos/{memo_id}", name="GET /api/memos/{id}")

    @task(1)
    def health_check(self) -> None:
        self.client.get("/health", name="GET /health")


class MemoWriter(HttpUser):
    """메모 작성 (쓰기 집중)"""

    weight = 1
    wait_time = between(0.3, 1)

    @task
    def create_memo(self) -> None:
        suffix = uuid.uuid4().hex[:8]
        payload = {
            "title": f"load-test-{suffix}",
            "content": "Locust write load test",
        }
        self.client.post("/api/memos", json=payload, name="POST /api/memos")
