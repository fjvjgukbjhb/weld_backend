from typing import Union
from fastapi import status as http_status
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from utils.tools_func import name_convert_to_camel

# class Resp(object):
#     def __init__(self, status: int, msg: str, code: int):
#         self.status = status
#         self.msg = msg
#         self.code = code
