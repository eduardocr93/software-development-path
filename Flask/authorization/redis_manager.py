import redis
import json


class RedisManager:

    def __init__(self):

        self.redis_client = redis.Redis(
            host="PLACEHOLDER",
            port=16345,
            password="PLACEHOLDER",
            decode_responses=True
        )

    def set(self, key, value):

        self.redis_client.set(
            key,
            json.dumps(value)
        )

    def get(self, key):

        data = self.redis_client.get(key)

        if data is None:

            return None

        return json.loads(data)

    def delete(self, key):

        self.redis_client.delete(key)