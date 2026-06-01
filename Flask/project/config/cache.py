import json

import redis

from config.settings import Config


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

        self.redis_client.set(key,json.dumps(value),ex=ttl)

    def get(self, key):

        data = self.redis_client.get(key)

        if data is None:
            return None

        return json.loads(data)

    def delete(self, key):

        self.redis_client.delete(key)


cache = RedisManager()