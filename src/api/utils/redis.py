import redis.asyncio
from fastapi_users.authentication import RedisStrategy

from settings import REDIS_HOST, REDIS_PORT, LIFETIME_SECONDS

redis = redis.asyncio.from_url(f'redis://{REDIS_HOST}:{REDIS_PORT}', decode_responses=True)


def get_redis_strategy() -> RedisStrategy:
    return RedisStrategy(redis, lifetime_seconds=LIFETIME_SECONDS)
