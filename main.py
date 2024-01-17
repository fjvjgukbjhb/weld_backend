import asyncio
from starlette.middleware.base import BaseHTTPMiddleware
import socket
from common import session
from core.server import create_app
from fastapi.openapi.docs import get_swagger_ui_html
import time
from fastapi import Depends, applications, FastAPI

from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os
import requests
'''
Author: 嘉欣 罗 2592734121@qq.com
Date: 2022-12-22 12:49:07
LastEditors: Please set LastEditors
LastEditTime: 2023-07-13 21:36:16
FilePath: \psad-backend\main.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

"""
pip install uvicorn
# 推荐启动方式 main指当前文件名字 app指FastAPI实例化后对象名称
uvicorn main:app --host=127.0.0.1 --port=8010 --reload  --env_file ./core/config/dev.env

类似flask 工厂模式创建
# 生产启动命令 去掉热重载 (可用supervisor托管后台运行)

在main.py同文件下下启动
uvicorn main:app --host=127.0.0.1 --port=8010 --workers=4

# 同样可以也可以配合gunicorn多进程启动  main.py同文件下下启动 默认127.0.0.1:8000端口
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 127.0.0.1:8020

"""

# from common import session
# from fastapi import Depends





def swagger_monkey_patch(*args, **kwargs):
    return get_swagger_ui_html(
        *args, **kwargs,
        swagger_js_url='https://cdn.bootcdn.net/ajax/libs/swagger-ui/4.10.3/swagger-ui-bundle.js',
        swagger_css_url='https://cdn.bootcdn.net/ajax/libs/swagger-ui/4.10.3/swagger-ui.css'
    )


applications.get_swagger_ui_html = swagger_monkey_patch
app = create_app()
host = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
# print('host')
# print(host)
port = 8010


async def reset_db_state():
    session.db._state._state.set(session.db.db_state.copy())
    session.db._state.reset()


# 基于BaseHTTPMiddleware的中间件实例，
class CostimeHeaderMiddleware(BaseHTTPMiddleware):

    # dispatch 必须实现
    async def dispatch(self, request, call_next):
        # print('基于BaseHTTPMiddleware的中间件实例请求开始前')
        start_time = time.time()
        responser = await call_next(request)
        process_time = round(time.time() - start_time, 4)
        # 返回接口响应时间
        responser.headers["X-Process-Time"] = f"{process_time} (s)"
        # print('请求开始前我可以处理事情555555555')
        return responser


# app.add_middleware(CostimeHeaderMiddleware)

# 作者：小钟同学
# 链接：https://juejin.cn/post/6971451349141553165
# 来源：稀土掘金
# 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
def getApiMap():
    apiMap = {}
    if hasattr(route, "methods"):
        print({'path': route.path, 'name': route.name, 'methods': route.methods})
        apiMap[route.path] = route.name
    return apiMap


#
# 设置文件夹路径（请将路径更改为实际的文件夹路径）
WELD_PATH = 'F:/weldProject/weld'
local_folder_path = Path(WELD_PATH)
# 将本地文件夹映射为 HTTP 地址
app.mount("/static1", StaticFiles(directory=str(local_folder_path)), name="static1")

if __name__ == "__main__":
    import uvicorn

    # 输出所有的路由
    for route in app.routes:
        if hasattr(route, "methods"):
            print({'path': route.path, 'name': route.name, 'methods': route.methods})

    asyncio.run(
        uvicorn.run(
            app='main:app',
            # host="127.0.0.1",
            host="172.16.80.225",
# <<<<<<< Updated upstream
#             host='172.16.50.86',
# =======
            # host="172.16.50.121",
# >>>>>>> Stashed changes
            port=port,
            loop="asyncio",
            reload=True,
            # debug=False,
            env_file='./core/config/dev.env',
            # timeout_keep_alive=10,
        )
    )
