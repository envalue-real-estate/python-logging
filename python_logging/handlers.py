import logging
import os

import redis


class RedisHandler(logging.Handler):
    list_name = 'logs'

    def __init__(self, host: str, port: int = 6379, db: int = 0):
        self._host = host
        self._port = port
        self._db = db
        self._connection = None
        super().__init__()

    def emit(self, record):
        self._connect().lpush('logs', self.format(record))

    def flush(self):
        if self._connection:
            self._connection.flushdb()

    def close(self):
        if self._connection:
            self._connection.close()
        super().close()

    def _connect(self) -> redis.Redis:
        if self._connection is None:
            self._connection = redis.Redis(host=self._host, port=self._port, db=self._db, password=os.getenv('REDIS_PASSWORD'))
        return self._connection
