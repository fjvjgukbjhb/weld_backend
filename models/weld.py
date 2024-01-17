from typing import Any
from venv import create

import aiohttp
from certifi import where
# TODO:userinfo=>user_text
from peewee import CharField, IntegerField, DateTimeField, JOIN, Model, fn, FloatField
from peewee_async import select

from common.session import BaseModel, paginator, db, async_db
# from weld_function.stft import stft
from utils.tools_func import convert_num_arr, convert_arr
import scipy.signal as signal
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import requests
import base64

class WeldGene(BaseModel):
    id = IntegerField(primary_key=True)
    weldBeadCode = CharField(column_name='weldBeadCode')
    weldMethod = CharField(column_name='weldMethod')
    weldMaterialInf = CharField(column_name='weldMaterialInf')
    weldWorker = CharField(column_name='weldWorker')
    weldGrooveType = CharField(column_name='weldGrooveType')
    standard = CharField(column_name='standard')
    weldDetailPicture = CharField(column_name='weldDetailPicture')
    # weldProcessData = CharField(column_name='weldProcessData')
    # testReportData = CharField(column_name='testReportData')

    createAt = DateTimeField(column_name='create_at')
    updateAt = DateTimeField(column_name='update_at')
    weldData = CharField(column_name='weld_data')
    weldLineImg = CharField(column_name='weld_line_img')
    RT = CharField(column_name='RT')
    UT = CharField(column_name='UT')
    MT = CharField(column_name='MT')
    PT = CharField(column_name='PT')
    craft = CharField(column_name='craft')

    class Meta:
        table_name = 'detailed_list'


    @classmethod
    async def select_all(cls):  #
        # db = await async_db.execute(WeldGene.select().order_by(WeldGene.createAt.desc()).dicts())
        db = await async_db.execute(WeldGene.select().dicts())
        print(db)
        # db = User_action.select().order_by(User_action.actionTime.desc()).dicts()
        # data = db.offset((pageNo - 1) * pageSize).limit(pageSize).dicts()
        if db:
            return list(db)
        else:
            return []
        # 查询：通过用户名称及分类查询信息

    # @classmethod
    # async def select_by(cls, code, treeNode, standard):
    #     # if params['id']:
    #     #     id = params['updateAt'][0]
    #     #     endTime = params['updateAt'][1]
    #     # else:
    #     #     beginTime = ''
    #     #     endTime = ''
    #     print(code, treeNode, standard)
    #
    #     if code == None and treeNode == None and standard == None :
    #         print("没有查询信息")
    #         result = "没有查询信息"
    #         return result
    #     else:
    #         db = await async_db.execute(WeldGene.select().where(
    #             WeldGene.weldBeadCode.contains(str(code)),
    #             WeldGene.weldGrooveType.contains(str(treeNode)),
    #             WeldGene.standard.contains(str(standard))
    #         ).order_by(WeldGene.updateAt.desc()).dicts())
    #         # db = await async_db.execute(WeldGene.select().where(
    #         #     WeldGene.weldBeadCode==code or
    #         #     WeldGene.weldGrooveType==treeNode or
    #         #      WeldGene.standard==standard
    #         # ).order_by(WeldGene.updateAt.desc()).paginate(int(start),int(length)).dicts())
    #
    #         # print("输出", len(db))
    #         if db:
    #             result = list(db)
    #             return result
    #         else:
    #             return []
    #     # total=len(db)
    #     result = {}
    #     result['total'] = len(db)
    #     data = db.offset((params.pageNo - 1) *
    #                      params.pageSize).limit(params.pageSize).dicts()
    #     result["data"] = list(data)
    #     return result




    @classmethod
    async def select_by(cls, putin: dict):  # 模糊查询
        # putin = str('%' + putin + '%')
        # putin2 = str('%' + putin + '%')
        # putin3 = str('%' + putin + '%')
        # result = await async_db.execute(
        #     UserTest.select().where(UserTest.realName ** putin).dicts())
        print(putin)
        # if isinstance(putin, dict):
        for key, value in putin.items():
            if key == 'inputValue':
                putin = value
                print(value)
                db = await async_db.execute(WeldGene.select().where(
                    WeldGene.weldBeadCode.contains(putin)
                ).dicts())
                result = list(db)

            elif key == 'nodeValue':
                putin = value
                print(putin)
                db = await async_db.execute(WeldGene.select().where(
                    WeldGene.weldGrooveType.contains(putin)
                ).dicts())

                result = list(db)
                print(result)
            elif key == 'identifier':
                putin = value
                print(putin)
                db = await async_db.execute(WeldGene.select().where(
                    WeldGene.standard.contains(putin)
                ).dicts())
                result = list(db)

        # result1 = list(db1)
        # result2 = list(db2)
        # result3 = list(db3)
        # # result = [result1, result2, result3]
        # # result = list(db)
        # print(result2)
        if db:
            # result = list(db1)
            # print(result)
            # result = result1
            return result
        # elif db2:
        #
        #     result = result2
        #     return result
        # elif db3:
        #     result = result3
        #     return result
        else:
            return []
        # # total=len(db)
        result = {}
        result['total'] = len(db)
        data = db.offset((params.pageNo - 1) *
                         params.pageSize).limit(params.pageSize).dicts()
        result["data"] = list(data)
        # result = db
        print(result)
        return result
        # else:
        #     putin = putin
        #
        # db1 = await async_db.execute(WeldGene.select().where(
        #         WeldGene.weldBeadCode.contains(putin),
        #
        # ).dicts())
        # db2 = await async_db.execute(WeldGene.select().where(
        #     WeldGene.weldGrooveType.contains(putin)
        #
        # ).dicts())
        # db3 = await async_db.execute(WeldGene.select().where(
        #     WeldGene.standard.contains(putin)
        # ).dicts())
        # print(putin)
        # # db = db1, db2, db3
        # # # db = await async_db.execute(WeldGene.select().where(
        # # #     WeldGene.weldBeadCode.contains(putin)
        # # # ).dicts())
        # # result = list(db)
        # result1 = list(db1)
        # result2 = list(db2)
        # result3 = list(db3)
        # result = [result1, result2, result3]
        # print(result)
        # if db1:
        #     # result = list(db)
        #     # # print(result)
        #     return result
        # elif db2:
        #     return result
        # elif db3:
        #     return result
        # else:
        #     return []
        # # if db:
        # #     # result = list(db)
        # #     # # print(result)
        # #     return result
        # # else:
        # #     return []
        # # total=len(db)
        # result = {}
        # result['total'] = len(db)
        # data = db.offset((params.pageNo - 1) *
        #                  params.pageSize).limit(params.pageSize).dicts()
        # result["data"] = list(data)
        # # result = db
        # print(result)
        # return result



    # @classmethod
    # async def image_to_base64(cls, url):
    #     print('here')
    #     response = requests.get(url)
    #     print('here2')
    #     # 检查响应状态码
    #     if response.status_code == 200:
    #         # 获取图片内容
    #         image_content = response.content
    #
    #         # 将图片内容进行 Base64 编码
    #         image_base64 = base64.b64encode(image_content)
    #
    #         # 转换为字符串格式
    #         image_base64_str = image_base64.decode('utf-8')
    #         imageBase64Dict = {"imageBase64": image_base64_str}
    #         return imageBase64Dict
    #     else:
    #         # 下载失败，返回空字符串或抛出异常
    #         return "图片转码失败"

    @classmethod
    async def image_to_base64(cls, url):
        print('here')
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=300)) as session:
            async with session.get(url) as response:
                print('here2',response.status)
            # 检查响应状态码
            if response.status == 200:
                # 获取图片内容
                # image_content = await response.read()

                image_content = response.content
                image_content = await response.read()
                print('here2.5', image_content)
                # 将图片内容进行 Base64 编码
                image_base64 = base64.b64encode(image_content)

                # 转换为字符串格式
                image_base64_str = image_base64.decode('utf-8')
                imageBase64Dict = {"imageBase64": image_base64_str}
                print(imageBase64Dict)
                return imageBase64Dict
            else:
                # 下载失败，返回空字符串或抛出异常
                return "图片转码失败"