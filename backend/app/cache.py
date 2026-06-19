import json
import logging
from typing import Any

import redis

from app.config import settings

logger = logging.getLogger(__name__)

MEMO_KEY = "memo:{memo_id}"
RECENT_KEY = "memos:recent:{limit}"
CACHE_TTL = 300

_client: redis.Redis | None = None


def get_redis() -> redis.Redis:
    global _client
    if _client is None:
        _client = redis.from_url(settings.redis_url, decode_responses=True)
    return _client


def ping() -> bool:
    try:
        return get_redis().ping()
    except redis.RedisError:
        return False


def _memo_key(memo_id: int) -> str:
    return MEMO_KEY.format(memo_id=memo_id)


def _recent_key(limit: int) -> str:
    return RECENT_KEY.format(limit=limit)


def get_memo(memo_id: int) -> dict[str, Any] | None:
    try:
        data = get_redis().get(_memo_key(memo_id))
        if data:
            logger.info("Cache HIT: memo:%s", memo_id)
            return json.loads(data)
        logger.info("Cache MISS: memo:%s", memo_id)
        return None
    except redis.RedisError as exc:
        logger.warning("Redis error on get memo:%s - %s", memo_id, exc)
        return None


def set_memo(memo: dict[str, Any]) -> None:
    try:
        get_redis().setex(
            _memo_key(memo["id"]), CACHE_TTL, json.dumps(memo, default=str)
        )
    except redis.RedisError as exc:
        logger.warning("Redis error on set memo:%s - %s", memo.get("id"), exc)


def get_recent_memos(limit: int) -> list[dict[str, Any]] | None:
    try:
        data = get_redis().get(_recent_key(limit))
        if data:
            logger.info("Cache HIT: recent memos (limit=%s)", limit)
            return json.loads(data)
        logger.info("Cache MISS: recent memos (limit=%s)", limit)
        return None
    except redis.RedisError as exc:
        logger.warning("Redis error on get recent memos - %s", exc)
        return None


def set_recent_memos(limit: int, memos: list[dict[str, Any]]) -> None:
    try:
        get_redis().setex(
            _recent_key(limit), CACHE_TTL, json.dumps(memos, default=str)
        )
    except redis.RedisError as exc:
        logger.warning("Redis error on set recent memos - %s", exc)


def invalidate_memo(memo_id: int) -> None:
    try:
        client = get_redis()
        client.delete(_memo_key(memo_id))
        for key in client.scan_iter("memos:recent:*"):
            client.delete(key)
        logger.info("Cache invalidated: memo:%s and recent lists", memo_id)
    except redis.RedisError as exc:
        logger.warning("Redis error on invalidate memo:%s - %s", memo_id, exc)


def invalidate_recent_lists() -> None:
    try:
        client = get_redis()
        for key in client.scan_iter("memos:recent:*"):
            client.delete(key)
        logger.info("Cache invalidated: recent lists")
    except redis.RedisError as exc:
        logger.warning("Redis error on invalidate recent lists - %s", exc)
