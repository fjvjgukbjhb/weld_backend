import asyncio
import base64
import json
from pathlib import Path
from typing import Any, List, Optional
from datetime import datetime, timedelta

import matplotlib
import numpy as np
import openpyxl
import pandas as pd
import peewee
import pytz
import pywt
from casbin.model import function
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, Form, Header, Body
from h11._abnf import status_code
from matplotlib import pyplot as plt
from pandas.conftest import cls
from pywt import threshold
from scipy.signal import savgol_filter, medfilt
from common.session import BaseModel, paginator, db, async_db
from fastapi.responses import FileResponse
from core import security

from models import user_test

from models.user_test import UserTest
from models.user_test import TestPost

from common import deps, logger
from models.usermenu import Usermenu
from models.userrole import RoleMenuRelp, Userrole
# from models.weld import WeldGene
from schemas.response import resp
from schemas.request import sys_user_test_schema
from schemas.request import sys_weld_schema
from playhouse.shortcuts import model_to_dict, dict_to_model
from peewee import fn, IntegrityError
from logic.user_logic import UserInfoLogic
from schemas.request import sys_user_schema
from common.session import db, get_db
from datetime import datetime
from utils.tools_func import rolePremission, tz
# from weld_function.stft import stft
from datetime import datetime
from typing import List
# from fastapi import FastAPI, File, UploadFile
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import shutil
import os
from models.weld import WeldGene
import requests
import aiohttp
from weld_function.picture import Method
from weld_function.stft import DataAnalyzer, FilterMethod

router = APIRouter()


# @router.post("/weld_getData/", summary="傅里叶变换", name="傅里叶变换")
# async def burn_stft_route(route: str):
#     result = await BurnThrough.burn_stft(route)
#     return result
#     burnthrough = burnthrough.dict()
#     try:
#         async with stft():
#             result = await BurnThrough.burn_stft(burnthrough)
#     finally:
#         return result

# 一个简单的路由，用于返回本地文件
# @router.get("/get_file/{file_name}")
# async def get_file(file_name: str):
#     file_path = file_name
#     return FileResponse(file_path)

@router.post("/weld/getData/", summary="新增表格", name="添加表格")
async def query_by(params: dict):
    # print("shuju", params)
    try:
        data = params.get("data")
        name = params.get("name")
        # print(data)
        df = pd.DataFrame(data)
        df.to_excel('weld_function/get_data/normal.xlsx', index=False)

        # 判断表格是否保存
        folder_path = "excel_data/excel_files"
        file_name = ''+name+'.xlsx'
        file_path = os.path.join(folder_path, file_name)

        # 检查文件是否已存在
        if os.path.exists(file_path):
            print(f"文件 '{file_name}' 已存在")
        else:
            # 保存数据
            df.to_excel('excel_data/'+name+'.xlsx', index=False)

        # 第一种滤波方式
        input_file = 'weld_function/get_data/normal.xlsx'
        time_column1 = 'weldTime'
        voltage_column1 = 'weldVol'
        current_column1 = 'weldCur'
        threshold = 10
        wavelet_name = 'db4'
        level = 4

        data = pd.read_excel(input_file)

        # 获取时间和电压数据
        t = data[time_column1].values
        x_voltage = data[voltage_column1].values
        x_current = data[current_column1].values

        # 进行小波包分解
        wavelet = pywt.Wavelet(wavelet_name)
        coeffs_voltage = pywt.wavedec(x_voltage, wavelet, level=level)
        coeffs_current = pywt.wavedec(x_current, wavelet, level=level)

        # 对小波包系数进行滤波
        coeffs_voltage_filt = [pywt.threshold(c, threshold * np.sqrt(2 * np.log2(len(c))), 'soft') for c in
                               coeffs_voltage]
        coeffs_current_filt = [pywt.threshold(c, threshold * np.sqrt(2 * np.log2(len(c))), 'soft') for c in
                               coeffs_current]

        # 重构滤波后的信号
        x_voltage_filt = pywt.waverec(coeffs_voltage_filt, wavelet)
        x_current_filt = pywt.waverec(coeffs_current_filt, wavelet)

        # 将负值设置为绝对值
        x_voltage_filt[x_voltage_filt < 0] = np.abs(x_voltage_filt[x_voltage_filt < 0])
        x_current_filt[x_current_filt < 0] = np.abs(x_current_filt[x_current_filt < 0])

        # 使用reshape将数组转换为一行
        x_voltage_filt = x_voltage_filt.reshape(1, -1)
        x_current_filt = x_current_filt.reshape(1, -1)

        # 创建一个字典列表
        result_list1 = []
        for i, (time, vol, cur) in enumerate(zip(t, x_voltage_filt[0], x_current_filt[0])):
            result_dict = {
                "id": i + 1,
                "weldTime": str(time),  # 假设时间是一个日期时间对象，如果需要，将其转换为字符串
                "weldVol": f"{vol:.2f}",
                "weldCur": f"{cur:.2f}"
            }
            result_list1.append(result_dict)
        # print(result_list1)

        # 第二种滤波方式

        # 电压
        time_column = 'weldTime'
        voltage_column = 'weldVol'
        current_column = 'weldCur'
        window_size = 21
        poly_order = 3

        # 提取列
        t = data[time_column].values
        y_voltage = data[voltage_column].values
        y_current = data[current_column].values

        # Savitzky-Golay 滤波
        y_voltage_sg_filter = savgol_filter(y_voltage, window_size, poly_order)
        y_current_sg_filter = savgol_filter(y_current, window_size, poly_order)

        # 将滤波后的数据保留一位小数
        y_voltage_sg_filter_rounded = np.round(y_voltage_sg_filter, 1)
        y_current_sg_filter_rounded = np.round(y_current_sg_filter, 1)

        # 创建一个字典列表
        result_list2 = []
        for i, (time, vol, cur) in enumerate(zip(t, y_voltage_sg_filter_rounded, y_current_sg_filter_rounded)):
            result_dict = {
                "id": i + 1,
                "weldTime": str(time),  # 假设时间是一个日期时间对象，如果需要，将其转换为字符串
                "weldVol": f"{vol:.2f}",
                "weldCur": f"{cur:.2f}"
            }
            result_list2.append(result_dict)

        # 绘制原始和滤波后的电压数据
        plt.plot(t, y_voltage, label='原始电压')
        plt.plot(t, y_voltage_sg_filter, label=f'Savitzky-Golay 滤波后的电压 (窗口={window_size}, 阶数={poly_order})',
                 color='green')
        plt.xlabel('时间')
        plt.ylabel('电压')
        # plt.legend()
        # plt.show()
        # result3 = result_list3
        # print(result_list2)

        # 第三种滤波方式

        window_size_1 = 5
        window_size_2 = 5

        y_medfilt_11 = medfilt(data[voltage_column].values, kernel_size=window_size_1)
        y_medfilt_12 = medfilt(data[current_column].values, kernel_size=window_size_1)

        # 第二次中值滤波
        y_medfilt_21 = medfilt(y_medfilt_11, kernel_size=window_size_2)
        y_medfilt_22 = medfilt(y_medfilt_12, kernel_size=window_size_2)

        # 创建包含每个记录的字典列表
        records = []
        for i, (time, vol, cur) in enumerate(zip(data[time_column], y_medfilt_21, y_medfilt_22)):
            record = {
                "id": i + 1,
                "weldTime": str(time),  # 使用时间列的值
                "weldVol": f"{vol:.2f}",  # 保留两位小数
                "weldCur": f"{cur:.2f}"  # 保留两位小数
            }
            records.append(record)
            # print(records)

        print("filterData_33", records)

        # if name == 'pile.xlsx':
        # t = [i / df.shape[0] for i in range(df.shape[0])]
        # x = df["weldCur"].values
        # data = x
        # # print("data", data)
        # sampling_rate = 50
        # wavename = "cgau8"  # 小波函数
        # totalscal = 256  # totalscal是对信号进行小波变换时所用尺度序列的长度(通常需要预先设定好)
        # fc = pywt.central_frequency(wavename)  # 计算小波函数的中心频率
        # cparam = 2 * fc * totalscal  # 常数c
        # scales = cparam / np.arange(totalscal, 1, -1)  # 为使转换后的频率序列是一等差序列，尺度序列必须取为这一形式（也即小波尺度）
        # [cwtmatr, frequencies] = pywt.cwt(data, scales, wavename, 1.0 / sampling_rate)  # 连续小波变换模块
        # # 画图
        # plt.figure(figsize=(8, 4))
        # plt.subplot(211)  # 第一整行
        # plt.plot(t, data)
        # plt.xlabel(u"time(s)")
        # plt.title(u"t to f")
        # plt.subplot(212)  # 第二整行

        np.set_printoptions(threshold=np.inf)
        matplotlib.use('TkAgg')

        df = pd.read_excel("weld_function/get_data/normal.xlsx")
        t = [i / df.shape[0] for i in range(df.shape[0])]
        x = df["weldCur"].values
        data = x
        # print("data",data)
        sampling_rate = 50
        wavename = "cgau8"  # 小波函数
        totalscal = 256  # totalscal是对信号进行小波变换时所用尺度序列的长度(通常需要预先设定好)
        fc = pywt.central_frequency(wavename)  # 计算小波函数的中心频率
        cparam = 2 * fc * totalscal  # 常数c
        scales = cparam / np.arange(totalscal, 1, -1)  # 为使转换后的频率序列是一等差序列，尺度序列必须取为这一形式（也即小波尺度）
        [cwtmatr, frequencies] = pywt.cwt(data, scales, wavename, 1.0 / sampling_rate)  # 连续小波变换模块
        # 画图
        plt.figure(figsize=(8, 4))
        plt.subplot(211)  # 第一整行
        plt.plot(t, data)
        plt.xlabel(u"time(s)")
        plt.title(u"t to f")
        plt.subplot(212)  # 第二整行

        plt.contourf(t, frequencies, abs(cwtmatr))
        print("length", len(abs(cwtmatr)))
        plt.ylabel(u"freq(Hz)")
        plt.xlabel(u"time(s)")
        plt.subplots_adjust(hspace=0.4)  # 调整边距和子图的间距 hspace为子图之间的空间保留的高度，平均轴高度的一部分
        # plt.show()

        ##############################################

        # 输出列表包字典
        t1 = list(range(1, len(t) + 1))
        formatted_data = []

        for i in range(len(t1)):
            for j in range(len(frequencies)):
                formatted_data.append({
                    "time": t1[i],
                    "freq": np.round(frequencies[j], 3),
                    "cwt": np.round(abs(cwtmatr[j, i]), 3)
                })
        # print(formatted_data)

        # 按照freq从小到大排序
        formatted_data_sorted = sorted(formatted_data, key=lambda x: x["freq"])

        # 转换为字符串
        # formatted_str = json.dumps(formatted_data, indent=2)
        # print(formatted_str)

        # # 修改格式
        # modified_data = []
        # for item in original_data:
        #     min_len = min(len(item['time']), len(item['freq']), len(item['cwt']))
        #     for i in range(min_len):
        #         # k, v = item
        #         # modified_data[k] = v
        #
        #         modified_data.append({
        #             "time": item['time'][i],
        #             "freq": item['freq'][i],
        #             "cwt": item['cwt'][i]  # 不再使用额外的中括号
        #         })

        # # 转换为字符串
        # formatted_str = str(formatted_data).replace("'", "").replace("[", "{").replace("]", "}").replace("{", "[").replace(
        #     "}", "]")
        # formatted_str = "{" + formatted_str[1:-1] + "}"
        # formatted_str = {}
        # for v in formatted_str1:
        #     formatted_str = v

        df = pd.read_excel('weld_function/get_data/normal.xlsx')
        # 在这里添加清除数据的逻辑，例如清除所有数据：
        df = pd.DataFrame(columns=df.columns)
        # 保存清除后的数据到文件
        df.to_excel(input_file, index=False)

        result = {'wave_Data': result_list1, 'sa_Data_': result_list2, 'centerData': records, 'formatted_str': formatted_data_sorted}
        # print("filterData_3", result["centerData"])
        # print("四三种", result)
        return resp.ok(data=result)
        # else:
        #
        #     df = pd.read_excel('weld_function/get_data/normal.xlsx')
        #     # 在这里添加清除数据的逻辑，例如清除所有数据：
        #     df = pd.DataFrame(columns=df.columns)
        #     # 保存清除后的数据到文件
        #     df.to_excel(input_file, index=False)

            # result = [result_list1, result_list2, records]
            # return resp.ok(data=result)

    except Exception as e:
        print(e)
        return resp.fail(resp.DataNotFound, detail=str(e))



# @router.post("/weld/test/", summary="测试表格", name="测试表格")
# async def create_upload_file(file: UploadFile = File(...)):
#     # 检查文件类型，确保是表格文件
#     if file.content_type != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
#         return {"error": "只接受Excel表格文件 (.xlsx)"}
#
#     # 保存文件到本地
#     #
#     # with open(f'weld_function/get_data/normal.xlsx', "wb") as f:
#     #     f.write(file.file.read())
#     try:
#         # # 指定文件夹名称
#         # folder_name = "get_data/normal.xlsx"
#         # # 获取当前项目的根目录
#         # base_path = Path(__file__).resolve().parent
#         # # 拼接文件夹的完整路径
#         # save_path = base_path / folder_name
#         save_path = 'weld_function/get_data/normal.xlsx'
#
#         with open(f'{save_path}', "wb") as f:
#             f.write(file.file.read())
#         # return {"get_data": file.filename}
#         input_file = 'weld_function/get_data/normal.xlsx'
#         output_file = '小波包电压.json'
#         time_column = 'SendDate'
#         column_name = 'EVoltage'
#         threshold = 10
#
#         FilterMethod.process_wavelet_filtering(input_file, output_file, time_column,  column_name, threshold)
#         result = output_file
#         # df = pd.read_excel('normal.xlsx')
#         # # 在这里添加清除数据的逻辑，例如清除所有数据：
#         # df = pd.DataFrame(columns=df.columns)
#         # # 保存清除后的数据到文件
#         # df.to_excel(save_path, index=False)
#         # print(result)
#         return resp.ok(data=result)
#     except Exception as e:
#         return resp.fail(resp.DataNotFound, detail=str(e))

#查询所有焊接基因库信息
@router.get("/weld/get_all_gene", summary=" 查询所有焊接基因库", name="获取焊接基因库")
async def query_all(pageSize:int,pageNo:int)->Any:

    print(pageSize, pageNo)
    if True:
        data = await WeldGene.select_all()
        print(data)
        total = len(data)

        # 分页
        current = int(pageNo)
        pageSize = int(pageSize)
        result = data[
                 (current * pageSize - pageSize):
                 current * pageSize
                 ]
        # 获取当前脚本文件的绝对路径
        script_path = os.path.abspath(__file__)
        print("Script Path:", script_path)
        print(total)
        return resp.ok(data=result, total=total)


    # 条件查询焊接基因库信息
# @router.post("/weld/get_by_gene", summary=" 条件查询焊接基因库", name="获取焊接基因库")
# async def query_all(code: Any, treeNode: Any, standard: Any) -> Any:
# # async def query_all(code: Any) -> Any:
#     try:
#         item_dict1 = code
#         item_dict2 = treeNode
#         item_dict3 = standard
#         result = await WeldGene.select_by(item_dict1, item_dict2, item_dict3)
#         # result2 = await WeldGene.select_by(item_dict2)
#         # result3 = await WeldGene.select_by(item_dict3)
#         # result_list = [result1, result2, result3]
#         # print("输出", result)
#         # total1 = len(result1)
#         # total2 = len(result2)
#         total = len(result)
#
#         # 分页
#         # current = int(params.pageNo)
#         # current = int(params.current)
#         # pageSize = int(params.pageSize)
#         # result = result[
#         #          (current * pageSize - pageSize):
#         #          current * pageSize
#         #          ]
#
#         return resp.ok(data=result, total=total)
#     except Exception as e:
#         print(e)
#         return resp.fail(resp.DataNotFound, detail=str(e))
#
@router.post("/weld/get_by_gene", summary=" 条件查询焊接基因库", name="获取焊接基因库")
# async def query_putin(putin1: str, putin2: str, putin3: str):
async def query_putin(putin: dict) -> Any:
    result = await WeldGene.select_by(putin)
    # return result
    total = len(result)

    return resp.ok(data=result, total=total)

@router.post("/weld/getHistoryData", summary=" 查询历史数据", name="查询历史数据")
async def query_history(weldBeadCode: dict):
    weldBeadCode = weldBeadCode['weldBeadCode']

    # #获取图片并进行base64转码
    # file_name = 'weld_line.jpg'
    #
    # weldBeadCode = Path(weldBeadCode)
    # print(weldBeadCode, file_name)
    # parent_path = os.getenv('WELD_PATH')
    # base_url = os.getenv('BASE_URL')
    # # subfolder_path = f"{base_url}/static1/{weldBeadCode}"
    # subfolder_path = parent_path / weldBeadCode
    # #
    # # # 使用 exists() 方法检查子文件夹是否存在
    # if subfolder_path.is_dir():
    #     print("exists", True)
    #     site = f"{base_url}/static1/{weldBeadCode}/{file_name}"
    #     print("/////", site)
    #     url = site
    #     imageBase64 = await Method.image_to_base64(url)
    #     print('here3')
    #     # response = requests.get(picture)
    #     # async with aiohttp.ClientSession() as session:
    #     #     async with session.get(picture) as response:
    #     #         print('here2')
    #     #     # 检查响应状态码
    #     #     if response.status == 200:
    #     #         # 获取图片内容
    #     #         image_content = await response.read()
    #     #
    #     #         # 将图片内容进行 Base64 编码
    #     #         image_base64 = base64.b64encode(image_content)
    #     #
    #     #         # 转换为字符串格式
    #     #         image_base64_str = image_base64.decode('utf-8')
    #     #         imageBase64Dict = {"imageBase64": image_base64_str}
    #     #         print(imageBase64Dict)
    #     #
    #     #     else:
    #     #         # 下载失败，返回空字符串或抛出异常
    #     #         return "图片转码失败"
    # else:
    #     raise HTTPException(status_code=404, detail=f"The subfolder '{weldBeadCode}' does not exist.")
    #
    folder_path = 'excel_data'
    # 获取文件夹中所有Excel文件的文件名
    excel_files = [file for file in os.listdir(folder_path) if file.endswith('.xlsx')]


    # 循环处理每个Excel文件
    for file_name1 in excel_files:
        # # 构建完整的文件路径
        # file_path = os.path.join(folder_path, file_name1)
        #
        # # 打开Excel文件
        # workbook = openpyxl.load_workbook(file_path)
        #
        # # 选择默认的工作表（Sheet）
        # sheet = workbook.active
        #
        # # 指定要获取值的单元格坐标
        # row_num = 2
        # column_num = 9
        #
        # # 从指定的单元格获取值
        # Code = sheet.cell(row=row_num, column=column_num).value
        # # 输出获取到的值
        # print(f"单元格({row_num}, {column_num}) 的值为: {Code}")
        if f"{weldBeadCode}.xlsx" == file_name1:
            file_path = os.path.join(folder_path, file_name1)
            data = pd.read_excel(file_path)
            time_column = 'weldTime'
            voltage_column = 'weldVol'
            current_column = 'weldCur'

            t = data[time_column].values
            x_voltage = data[voltage_column].values
            x_current = data[current_column].values
            print(t)

            result_list = []
            for i, (time, vol, cur) in enumerate(zip(t, x_voltage, x_current)):
                result_dict = {
                    "id": i + 1,
                    "weldTime": str(time),  # 假设时间是一个日期时间对象，如果需要，将其转换为字符串
                    "weldVol": f"{vol:.2f}",
                    "weldCur": f"{cur:.2f}"
                }
                result_list.append(result_dict)
            result = result_list

            # result.append(imageBase64Dict)
            file_name = str(f"{weldBeadCode}.xlsx")
            # result.append(file_name)
            print(result[-1])

            total = len(result)
            return resp.ok(data=result,name=file_name,total=total)

@router.post("/weld/get_file", summary=" 查询文件", name="查询文件")
async def query_putin(putin: dict) -> Any:
    # weldBeadCode = weldBeadCode['weldBeadCode']
    # print(putin)
    weldBeadCode = putin['weldBeadCode']
    file_name = putin['fileName']
    weldBeadCode = Path(weldBeadCode)
    print(weldBeadCode, file_name)
    parent_path = os.getenv('WELD_PATH')

    # parent_path = Path('F:/weldProject/weld')
    # subfolder_path = parent_path / weldBeadCode
    # is_subfolder_exists = subfolder_path.is_dir()
    # print(is_subfolder_exists)

    # 替换为您的本地 FastAPI 服务地址和端口
    base_url = os.getenv('BASE_URL')
    # base_url = str('http://172.16.80.225:8010')
    print(base_url)
    subfolder_path = f"{base_url}/static1/{weldBeadCode}"
    print(subfolder_path)

    subfolder_path = parent_path / weldBeadCode

    # 使用 exists() 方法检查子文件夹是否存在
    if subfolder_path.is_dir():
        print("exists", True)
        site = f"{base_url}/static1/{weldBeadCode}/{file_name}"
        result = site
        return resp.ok(data=result)
    else:
        raise HTTPException(status_code=404, detail=f"The subfolder '{weldBeadCode}' does not exist.")

    # # is_subfolder_exists = subfolder_path.is_dir()
    # response = requests.get(subfolder_path)
    # print(response)
    # if response == 200:
    #     site = f"{base_url}/static1/{weldBeadCode}/{file_name}"
    #
    #     # 发送 GET 请求获取文件内容
    #     # response = requests.get(site)
    #     print("ok")
    #     result = site
    #     return resp.ok(data=result)
    # else:
    #     print("response:文件夹不存在")

    # return resp.ok(data=result)
        #
        # if weldBeadCode == Code:
        #     # 第一种滤波方式
        #     input_file = file_path
        #     time_column1 = 'weldTime'
        #
        #     voltage_column1 = 'weldVol'
        #     current_column1 = 'weldCur'
        #     threshold = 10
        #     wavelet_name = 'db4'
        #     level = 4
        #
        #     data = pd.read_excel(input_file)
        #
        #     # 获取时间和电压数据
        #     t = data[time_column1].values
        #     x_voltage = data[voltage_column1].values
        #     x_current = data[current_column1].values
        #
        #     # 进行小波包分解
        #     wavelet = pywt.Wavelet(wavelet_name)
        #     coeffs_voltage = pywt.wavedec(x_voltage, wavelet, level=level)
        #     coeffs_current = pywt.wavedec(x_current, wavelet, level=level)
        #
        #     # 对小波包系数进行滤波
        #     coeffs_voltage_filt = [pywt.threshold(c, threshold * np.sqrt(2 * np.log2(len(c))), 'soft') for c in
        #                            coeffs_voltage]
        #     coeffs_current_filt = [pywt.threshold(c, threshold * np.sqrt(2 * np.log2(len(c))), 'soft') for c in
        #                            coeffs_current]
        #
        #     # 重构滤波后的信号
        #     x_voltage_filt = pywt.waverec(coeffs_voltage_filt, wavelet)
        #     x_current_filt = pywt.waverec(coeffs_current_filt, wavelet)
        #
        #     # 将负值设置为绝对值
        #     x_voltage_filt[x_voltage_filt < 0] = np.abs(x_voltage_filt[x_voltage_filt < 0])
        #     x_current_filt[x_current_filt < 0] = np.abs(x_current_filt[x_current_filt < 0])
        #
        #     # 使用reshape将数组转换为一行
        #     x_voltage_filt = x_voltage_filt.reshape(1, -1)
        #     x_current_filt = x_current_filt.reshape(1, -1)
        #
        #     # 创建一个字典列表
        #     result_list1 = []
        #     for i, (time, vol, cur) in enumerate(zip(t, x_voltage_filt[0], x_current_filt[0])):
        #         result_dict = {
        #             "id": i + 1,
        #             "weldTime": str(time),  # 假设时间是一个日期时间对象，如果需要，将其转换为字符串
        #             "weldVol": f"{vol:.2f}",
        #             "weldCur": f"{cur:.2f}"
        #         }
        #         result_list1.append(result_dict)
        #     print(result_list1)
        #
        #     # 第二种滤波方式
        #
        #     # 电压
        #     time_column = 'weldTime'
        #     voltage_column = 'weldVol'
        #     current_column = 'weldCur'
        #     window_size = 21
        #     poly_order = 3
        #
        #     # 提取列
        #     t = data[time_column].values
        #     y_voltage = data[voltage_column].values
        #     y_current = data[current_column].values
        #
        #     # Savitzky-Golay 滤波
        #     y_voltage_sg_filter = savgol_filter(y_voltage, window_size, poly_order)
        #     y_current_sg_filter = savgol_filter(y_current, window_size, poly_order)
        #
        #     # 将滤波后的数据保留一位小数
        #     y_voltage_sg_filter_rounded = np.round(y_voltage_sg_filter, 1)
        #     y_current_sg_filter_rounded = np.round(y_current_sg_filter, 1)
        #
        #     # 创建一个字典列表
        #     result_list2 = []
        #     for i, (time, vol, cur) in enumerate(
        #             zip(t, y_voltage_sg_filter_rounded, y_current_sg_filter_rounded)):
        #         result_dict = {
        #             "id": i + 1,
        #             "weldTime": str(time),  # 假设时间是一个日期时间对象，如果需要，将其转换为字符串
        #             "weldVol": f"{vol:.2f}",
        #             "weldCur": f"{cur:.2f}"
        #         }
        #         result_list2.append(result_dict)
        #
        #     # 绘制原始和滤波后的电压数据
        #     plt.plot(t, y_voltage, label='原始电压')
        #     plt.plot(t, y_voltage_sg_filter,
        #              label=f'Savitzky-Golay 滤波后的电压 (窗口={window_size}, 阶数={poly_order})',
        #              color='green')
        #     plt.xlabel('时间')
        #     plt.ylabel('电压')
        #
        #     # 第三种滤波方式
        #
        #     window_size_1 = 5
        #     window_size_2 = 5
        #
        #     y_medfilt_11 = medfilt(data[voltage_column].values, kernel_size=window_size_1)
        #     y_medfilt_12 = medfilt(data[current_column].values, kernel_size=window_size_1)
        #
        #     # 第二次中值滤波
        #     y_medfilt_21 = medfilt(y_medfilt_11, kernel_size=window_size_2)
        #     y_medfilt_22 = medfilt(y_medfilt_12, kernel_size=window_size_2)
        #
        #     # 创建包含每个记录的字典列表
        #     records = []
        #     for i, (time, vol, cur) in enumerate(zip(data[time_column], y_medfilt_21, y_medfilt_22)):
        #         record = {
        #             "id": i + 1,
        #             "weldTime": str(time),  # 使用时间列的值
        #             "weldVol": f"{vol:.2f}",  # 保留两位小数
        #             "weldCur": f"{cur:.2f}"  # 保留两位小数
        #         }
        #         records.append(record)
        #         # print(records)
        #
        #     # print("filterData_33", records)
        #
        #     np.set_printoptions(threshold=np.inf)
        #     matplotlib.use('TkAgg')
        #
        #     df = pd.read_excel(file_path)
        #     t = [i / df.shape[0] for i in range(df.shape[0])]
        #     x = df["weldCur"].values
        #     data = x
        #
        #     sampling_rate = 50
        #     wavename = "cgau8"  # 小波函数
        #     totalscal = 256  # totalscal是对信号进行小波变换时所用尺度序列的长度(通常需要预先设定好)
        #     fc = pywt.central_frequency(wavename)  # 计算小波函数的中心频率
        #     cparam = 2 * fc * totalscal  # 常数c
        #     scales = cparam / np.arange(totalscal, 1, -1)  # 为使转换后的频率序列是一等差序列，尺度序列必须取为这一形式（也即小波尺度）
        #     [cwtmatr, frequencies] = pywt.cwt(data, scales, wavename, 1.0 / sampling_rate)  # 连续小波变换模块
        #     # 画图
        #     plt.figure(figsize=(8, 4))
        #     plt.subplot(211)  # 第一整行
        #     plt.plot(t, data)
        #     plt.xlabel(u"time(s)")
        #     plt.title(u"t to f")
        #     plt.subplot(212)  # 第二整行
        #
        #     plt.contourf(t, frequencies, abs(cwtmatr))
        #     print("length", len(abs(cwtmatr)))
        #     plt.ylabel(u"freq(Hz)")
        #     plt.xlabel(u"time(s)")
        #     plt.subplots_adjust(hspace=0.4)  # 调整边距和子图的间距 hspace为子图之间的空间保留的高度，平均轴高度的一部分
        #     # plt.show()
        #
        #     ##############################################
        #
        #     # 输出列表包字典
        #     t1 = list(range(1, len(t) + 1))
        #     formatted_data = []
        #
        #     for i in range(len(t1)):
        #         for j in range(len(frequencies)):
        #             formatted_data.append({
        #                 "time": t1[i],
        #                 "freq": np.round(frequencies[j], 3),
        #                 "cwt": np.round(abs(cwtmatr[j, i]), 3)
        #             })
        #     # print(formatted_data)
        #
        #     # 按照freq从小到大排序
        #     formatted_data_sorted = sorted(formatted_data, key=lambda x: x["freq"])
        #
        #     # 关闭工作簿
        #     workbook.close()
        #     result = {'wave_Data': result_list1, 'sa_Data_': result_list2, 'centerData': records,
        #               'formatted_str': formatted_data_sorted}
        #     print("filterData_3", result["centerData"])
        #     # print("四三种", result)

        # data = pd.read_excel(file_path)
        # time_column = 'weldTime'
        # voltage_column = 'weldVol'
        # current_column = 'weldCur'
        # t = data[time_column].values
        # x_voltage = data[voltage_column].values
        # x_current = data[current_column].values
        #
        # result_list = []
        # for i, (time, vol, cur) in enumerate(zip(t, x_voltage[0], x_current[0])):
        #     result_dict = {
        #         "id": i + 1,
        #         "weldTime": str(time),  # 假设时间是一个日期时间对象，如果需要，将其转换为字符串
        #         "weldVol": f"{vol:.2f}",
        #         "weldCur": f"{cur:.2f}"
        #     }
        #     result_list.append(result_dict)
        # result = data
        # print(data)
        #
        # total = len(result)
        # return resp.ok(data=result, total=total)