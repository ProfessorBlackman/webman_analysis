from django.conf import settings
from redis import Redis
import redis

from webman_analysis.loggers import redis_logger

redis_client = None


try:
    host = settings.REDIS_CONFIG.get('host')
    port = settings.REDIS_CONFIG.get('port')
    db = settings.REDIS_CONFIG.get('db')
    pool = redis.ConnectionPool.from_url(f"redis://{host}:{port}/{db}")

    with Redis(connection_pool=pool) as client:
        redis_client = client
except Exception as error:
    redis_client = None
    redis_logger.error(f"Redis connection error: {error}")