#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author ----> leif.xing
@mail   ----> leif.xing@gmail.com
"""

import redis


class RedisInstance(object):
    def __init__(self, host="localhost"):
        self.rc = redis.StrictRedis(host, decode_responses=True)


class RedisPubSub(object):
    def __init__(self):
        self._conn = redis.Redis(host='127.0.0.1', port=6379)
        self.channel = 'task'

    def publish(self, msg):
        self._conn.publish(self.channel, msg)
        return True

    def subscribe(self):
        pub = self._conn.pubsub()
        pub.subscribe(self.channel)
        pub.parse_response()
        return pub


class RedisHashMap(object):
    def __init__(self, instance=None, key="HM", host="localhost"):
        """
        key用于筛选过滤，name用于设置hash map的名称
        :instance: 是否有redis的instance，有则无需再次创建
        :param key:
        :param host:
        """
        self.key = key
        self.name = ""
        self._rc = redis.StrictRedis(host, decode_responses=True) \
            if not instance else instance

    def hash_keys(self):
        return self._rc.keys("%s_*" % self.key)

    def set_hash(self, data):
        self._rc.hmset(self.name, data)

    def del_hash(self):
        self._rc.delete(self.name)

    def get_hash(self):
        return self._rc.hgetall(self.name)

    def hash_exists(self):
        if self._rc.exists(self.name):
            return True
        else:
            return False

    def rm_all(self):
        for hash_name in self.hash_keys():
            print(hash_name)
            self.name = hash_name
            if self.hash_exists():
                self.del_hash()

    def hash_list(self):
        ret_list = []
        for hash_name in self.hash_keys():
            self.name = hash_name
            hash_data = self.get_hash()
            ret_list.append(hash_data)
        return ret_list


class RedisList(object):
    def __init__(self, instance=None, name='', host="localhost"):
        self.name = name
        self.item = None
        self.idx = -5000
        self._rc = redis.StrictRedis(host, decode_responses=True) \
            if not instance else instance

    def push(self, item):
        self._rc.rpush(self.name, item)

    def lpop(self):
        self.item = self._rc.lpop(self.name)

    def rpop(self):
        self.item = self._rc.rpop(self.name)

    def exists(self, item):
        return True if item in self._rc.lrange(self.name, 0, -1) else False

    def items(self):
        return self._rc.lrange(self.name, 0, -1)

    def index(self, item):
        self.idx = self._rc.lindex(self.name, item)

    def rm(self, item):
        self._rc.lrem(self.name, 0, item)

    def len(self):
        return self._rc.llen(self.name)

    def delete(self):
        self._rc.delete(self.name)

    def deserial(self):
        return eval(self.item)


class RedisQueue(object):
    """
    Simple Queue with Redis Backend
    """
    def __init__(self, name, namespace='queue', **redis_kwargs):
        self.__db = redis.Redis(**redis_kwargs)
        self.key = '%s:%s' % (namespace, name)

    def qsize(self):
        """
        Return the approximate size of the queue
        """
        return self.__db.llen(self.key)

    def empty(self):
        """
        Return True if the queue is empty, False otherwise
        """
        return self.qsize() == 0

    def put(self, item):
        """
        Put item into the queue
        """
        self.__db.rpush(self.key, item)

    def get(self, block=True, timeout=None):
        """
        Remove and return an item from the queue
        If optional args block is true and timeout is None (the default), block
        if necessary until an item is available
        """
        if block:
            item = self.__db.blpop(self.key, timeout=timeout)
        else:
            item = self.__db.lpop(self.key)

        if item:
            item = item[1]
        return item

    def get_nowait(self):
        """
        Equivalent to get(False)
        """
        return self.get(False)

    def clear(self):
        """
        Clear queue
        """
        for i in range(self.qsize()):
            self.get()
