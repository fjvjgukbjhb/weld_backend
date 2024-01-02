'''
Author: 嘉欣 罗 2592734121@qq.com
Date: 2022-12-22 12:49:07
LastEditors: Please set LastEditors
LastEditTime: 2023-05-10 14:36:19
FilePath: \psad-backend\core\config\config.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''


import os
import socket

from typing import Union, Optional, Dict
from pathlib import Path
from pydantic import AnyHttpUrl, BaseSettings, IPvAnyAddress


class Settings(BaseSettings):
    # class Config:
    #     env_file = ".env"
    # 开发模式配置
    DEBUG: bool = True
    # 项目文档
    TITLE: str = "产品选型与设计项目"
    DESCRIPTION: str = "整体描述"
    # 文档地址 默认为docs 生产环境关闭 None
    DOCS_URL: str = "/api/docs"
    # 文档关联请求数据接口
    OPENAPI_URL: str = "/api/openapi.json"
    # redoc 文档
    REDOC_URL: Optional[str] = "/api/redoc"

    # token过期时间 分钟
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # 生成token的加密算法
    ALGORITHM: str = "HS256"

    # 生产环境保管好 SECRET_KEY
    # SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

    SECRET_KEY: str = '(-ASp+_)-Ulhw0848hnvVG-iqKyJSD&*&^-H3C9mqEqSl8KN-YRzRE'

    # 项目根路径
    BASE_PATH: str = os.path.dirname(os.path.dirname(
        os.path.dirname((os.path.abspath(__file__)))))
    print(BASE_PATH)
    LOG_PATH: str = BASE_PATH

    # LOG_PATH: str = 'D:/'
    # 配置你的Mysql环境
    MYSQL_USERNAME: str = "root"
    MYSQL_PASSWORD: str = "root"
    MYSQL_HOST: str = "localhost"
    # MYSQL_HOST: str = "api-psad"
    MYSQL_PORT: int = 3306
    MYSQL_DATABASE: str = 'psad'

    # MYSQL_HOST: str = os.getenv('MYSQL_HOST'),
    # MYSQL_PORT: int = os.getenv('MYSQL_PORT'),
    # MYSQL_USERNAME: str = os.getenv('MYSQL_USERNAME'),
    # MYSQL_PASSWORD : str = os.getenv('MYSQL_PASSWORD'),

    SERVER_HOST: str = socket.gethostbyname(
        socket.getfqdn(socket.gethostname()))
    SERVER_PORT: int = 8010

    SERVER_URL: str = f"http://{SERVER_HOST}:{SERVER_PORT}"
    # redis配置
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PASSWORD: str = "123456"
    REDIS_DB: int = 0
    REDIS_PORT: int = 6379
    REDIS_URL: str = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}?encoding=utf-8"
    REDIS_TIMEOUT: int = 5  # redis连接超时时间

    # CASBIN_MODEL_PATH: str = "./resource/rbac_model.conf"

    UPLOAD_FILE_URL = 'http://172.16.50.127:8080/api/minIO/upload'
    # APP_NAME = ''
    # class Config:
    #     env_file = "dev.env"



settings = Settings()
# print(settings.APP_NAME)_env_file='dev.env'

