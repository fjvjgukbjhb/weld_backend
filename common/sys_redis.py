#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/28 20:34
# @Author  : CoderCharm
# @File    : sys_redis.py
# @Software: PyCharm
# @Github  : github/CoderCharm
# @Email   : wg_python@163.com
# @Desc    :
"""

通过class 实例化对象可以直接修改内部属性的特性
再通过魔法方法，赋予实例化对象 具有内部属性_redis_client的方法和属性

主要参考 flask-redis扩展实现
https://github.com/underyx/flask-redis/blob/master/flask_redis/client.py

redis 连接

"""
import os
import sys
from redis import Redis, AuthenticationError

from common.logger import logger
from core.config import settings


class RedisCli(object):

    def __init__(self, *, host: str, port: int, password: str, db: int, socket_timeout: int = 5):
        # redis对象 在 @app.on_event("startup") 中连接创建
        self._redis_client = None
        self.host = host
        self.port = port
        self.password = password
        self.db = db
        self.socket_timeout = socket_timeout

    def init_redis_connect(self) -> None:
        """
        初始化连接
        :return:
        """
        try:
            self._redis_client = Redis(
                host=self.host,
                port=self.port,
                password=self.password,
                db=self.db,
                socket_timeout=self.socket_timeout,
                decode_responses=True  # 解码
            )
            if not self._redis_client.ping():
                logger.info("连接redis超时")
                print("连接redis超时")
                sys.exit()
        except (AuthenticationError, Exception) as e:
            logger.info(f"连接redis异常 {e}")
            print(f"host: {self.host}")
            print(f"port: {self.port}")
            print(f"password: {self.password}")
            print(f"db: {self.db}")
            print(f"socket_timeout: {self.socket_timeout}")
            sys.exit()

    # 使实例化后的对象 赋予redis对象的的方法和属性
    def __getattr__(self, name):
        return getattr(self._redis_client, name)

    def __getitem__(self, name):
        return self._redis_client[name]

    def __setitem__(self, name, value):
        self._redis_client[name] = value

    def __delitem__(self, name):
        del self._redis_client[name]


# print("os.getenv('REDIS_HOST')")
# print(os.getenv('REDIS_HOST'))
# 创建redis连接对象
redis_client= RedisCli(
    # host=settings.REDIS_HOST,
    # port=settings.REDIS_PORT,
    # password=settings.REDIS_PASSWORD,
    # db=settings.REDIS_DB,
    # socket_timeout=settings.REDIS_TIMEOUT

    host=os.getenv('REDIS_HOST'),
    port=int(os.getenv('REDIS_PORT')) if os.getenv('REDIS_PORT') else os.getenv('REDIS_PORT'),
    password=os.getenv('REDIS_PASSWORD'),
    db=int(os.getenv('REDIS_DB')) if os.getenv('REDIS_DB') else os.getenv('REDIS_DB'),
    socket_timeout=int(os.getenv('REDIS_TIMEOUT')) if os.getenv('REDIS_TIMEOUT') else os.getenv('REDIS_TIMEOUT')
)

# 只允许导出 redis_client 实例化对象
__all__ = ["redis_client"]
