FROM redis:alpine
COPY redis.conf /usr/local/etc/redis/redis.conf

CMD [ "sh", "-c", "exec redis-server --requirepass $REDIS_PASSWORD"]