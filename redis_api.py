import redis
from config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_USERNAME, REDIS_MAX_CONNECTIONS, REDIS_RETRY_ON_TIMEOUT

connection_pool = redis.ConnectionPool(
    host=REDIS_HOST,
    port=REDIS_PORT,
    username=REDIS_USERNAME,
    password=REDIS_PASSWORD,
    decode_responses=True,
    retry_on_timeout=REDIS_RETRY_ON_TIMEOUT,
    max_connections=REDIS_MAX_CONNECTIONS
)


class RedisSession:
    def __enter__(self):
        self.db_session = redis.Redis(connection_pool=connection_pool)
        return self.db_session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db_session.close()
        return False
