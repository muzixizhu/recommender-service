import redis
from redis.exceptions import WatchError


class RedisDb:

    def __init__(self):
        self.redis_db_host = 'riot-api-limits.redis.cache.windows.net'
        self.redis_db_port = 6380
        self.redis_db_password = 'lLIlAeuwTTrX0B4ueyDT4MWfdGBDPDR9OJDeqNJ2fv4='
        self.redis_db = None

    def connect_to_redis_db(self, reconnect=False):
        if type(self.redis_db).__name__ != 'StrictRedis' or reconnect:
            try:
                self.redis_db = redis.StrictRedis(host=self.redis_db_host,
                                                  port=self.redis_db_port,
                                                  db=0,
                                                  password=self.redis_db_password,
                                                  ssl=True,
                                                  socket_connect_timeout=10,
                                                  retry_on_timeout=True)
            except Exception as ex:
                print('Encountered exception in method {0}.{1}:'.format('RedisDb', 'connect_to_redis_db'))
                print(ex)

                return False

        return True

    def set_expire(self, name, expiration_seconds = 0):
        if expiration_seconds > 0:
            self.redis_db.expire(name, expiration_seconds)

    def get_hash(self, name, attribute):
        return self.redis_db.hget(name, attribute)

    def set_hash(self, name, attribute, value, expiration_seconds=0):
        self.redis_db.hset(name, attribute, value)
        self.set_expire(name, expiration_seconds)

    def queue_push(self, name, value):
        self.redis_db.rpush(name, value)

    def queue_pop(self, name):
        return self.redis_db.lpop(name).decode("utf-8")

    def increment(self, name, value, expiration_seconds = 0):
        incr_result = self.redis_db.incr(name, value)
        self.set_expire(name, expiration_seconds)
        return incr_result

    def get_value(self, name):
        return self.redis_db.get(name)

    def set_value(self, name, value, expiration_seconds = 0):
        self.redis_db.set(name, value)
        self.set_expire(name, expiration_seconds)

    def delete_value(self, key):
        self.redis_db.delete(key)

    def get_len(self, name):
        return self.redis_db.llen(name)

    def exists(self, name):
        return self.redis_db.exists(name)

    def get_list_of_set_values(self, name):
        values_list = []
        members = self.redis_db.smembers(name)
        for member in members:
            if member is not None:
                values_list.append(member.decode("utf-8"))
        return values_list

    def put_list_to_set(self, name, values_list = [], expiration_seconds=0):
        for value in values_list:
            self.redis_db.sadd(name, value)
        self.set_expire(name, expiration_seconds)

    def pop_random_values_from_set(self, name, values_count = 0):
        values_list = []
        for i in range(0, values_count):
            set_value = self.redis_db.spop(name)
            if set_value is not None:
                values_list.append(int(set_value.decode("utf-8")))
        return values_list

    def get_set_cardinality(self, name):
        return self.redis_db.scard(name)

    def get_pipeline(self):
        return self.redis_db.pipeline()

    def get_all_hash_attributes_values(self, name):
        return self.redis_db.hscan(name)

    def get_ttl(self, name):
        return self.redis_db.ttl(name)


if __name__ == '__main__':
    db = RedisDb()
    con = db.connect_to_redis_db()
    db.set_value('myfoo', 8888, 60)
    print('Val from redis {}'.format(db.get_value('myfoo')))