from unittest.mock import Mock

import redis

from config.cache import RedisManager


def test_get_falls_back_to_cache_miss_when_redis_is_unavailable(caplog):
    manager = RedisManager()
    manager.redis_client = Mock()
    manager.redis_client.get.side_effect = redis.exceptions.ConnectionError("Redis unavailable")

    assert manager.get("products_all") is None
    assert "continuing without cache" in caplog.text


def test_cache_writes_and_deletes_do_not_break_api_when_redis_is_unavailable(caplog):
    manager = RedisManager()
    manager.redis_client = Mock()
    manager.redis_client.set.side_effect = redis.exceptions.ConnectionError("Redis unavailable")
    manager.redis_client.delete.side_effect = redis.exceptions.ConnectionError("Redis unavailable")

    manager.set("products_all", [])
    manager.delete("products_all")

    assert caplog.text.count("continuing without cache") == 2
