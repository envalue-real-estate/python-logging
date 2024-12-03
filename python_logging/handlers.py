import logging
import os

import redis


class RedisHandler(logging.Handler):
    list_name = 'logs'

    def __init__(self, host: str, port: int = 6379, db: int = 0):
        self.redis = redis.Redis(host=host, port=port, db=db, password=os.getenv('REDIS_PASSWORD'))
        super().__init__()

    def emit(self, record):
        self.redis.lpush('logs', self.format(record))

    def flush(self):
        self.redis.flushdb()

    def close(self):
        self.redis.close()
        super().close()
