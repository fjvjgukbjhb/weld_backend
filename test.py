from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os
import requests
# 创建 FastAPI 应用
# app = FastAPI()

# 设置文件夹路径（请将路径更改为实际的文件夹路径）
local_folder_path = Path("F:/project")

# 将本地文件夹映射为 HTTP 地址
FastAPI().mount("/static", StaticFiles(directory=str(local_folder_path)), name="static")

# # 文件路径
# file_path = local_folder_path / "example.txt"
#
# # 检查文件是否存在
# if file_path.exists():
#     # 读取文件内容
#     with file_path.open("r") as file:
#         file_content = file.read()
#         print(file_content)
# else:
#     print(f"File not found: {file_path}")

# 替换为您的本地 FastAPI 服务地址和端口
base_url = "http://172.16.80.225:8010"

site = f"{base_url}/static/example.txt"


# 发送 GET 请求获取文件内容
response = requests.get(site)

print(site)
print("response", response)

# 检查请求是否成功
if response.status_code == 200:
    # 打印文件内容
    # 读取文件内容
    with site.open("r") as file:
        file_content = file.read()
        print(file_content)
else:
    print(f"Failed to retrieve file. Status code: 555")

#
# import paramiko
#
# # 替换为目标电脑的实际 IP 地址、端口号、用户名和密码
# hostname = "172.16.80.225"
# port = 8010
# username = "whale"
# password = "liangjkvk"
#
# # 创建 SSH 客户端
# client = paramiko.SSHClient()
# client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#
# try:
#     # 连接到目标电脑
#     client.connect(hostname, port=port, username=username, password=password)
#
#     # 远程文件路径
#     remote_file_path = "C:/Users/whale/Desktop/example.txt"
#
#     # 打开 SSH 会话
#     with client.open_sftp() as sftp:
#         try:
#             # 读取文件内容
#             with sftp.file(remote_file_path, "r") as remote_file:
#                 file_content = remote_file.read()
#                 print(file_content)
#         except FileNotFoundError:
#             print(f"Remote file '{remote_file_path}' not found.")
# except Exception as e:
#     print(f"Failed to connect: {e}")
# finally:
#     # 关闭 SSH 连接
#     client.close()
