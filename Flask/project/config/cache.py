import json
import logging

import redis

from config.settings import Config

logger = logging.getLogger(__name__)


class RedisManager:

    def __init__(self):

        self.redis_client = redis.Redis(
            host=Config.REDIS_HOST,
            port=Config.REDIS_PORT,
            username=Config.REDIS_USERNAME or None,
            password=Config.REDIS_PASSWORD or None,
            db=Config.REDIS_DB,
            decode_responses=True
        )

    def set(self, key, value, ttl=60):

        try:
            self.redis_client.set(key, json.dumps(value), ex=ttl)
        except redis.exceptions.RedisError as error:
            logger.warning("Redis cache SET failed; continuing without cache: %s", error)

    def get(self, key):

        try:
            data = self.redis_client.get(key)
        except redis.exceptions.RedisError as error:
            logger.warning("Redis cache GET failed; continuing without cache: %s", error)
            return None

        if data is None:
            return None

        return json.loads(data)

    def delete(self, key):

        try:
            self.redis_client.delete(key)
        except redis.exceptions.RedisError as error:
            logger.warning("Redis cache DELETE failed; continuing without cache: %s", error)


cache = RedisManager()