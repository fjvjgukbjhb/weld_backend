import json
from pathlib import Path
from typing import Any, List, Optional
from datetime import datetime, timedelta

import matplotlib
import numpy as np
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

from core import security
from models import user_test

from models.user_test import UserTest
from models.user_test import TestPost

from common import deps, logger
from models.usermenu import Usermenu
from models.userrole import RoleMenuRelp, Userrole
from models.weld import WeldGene
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

@router.post("/weld/getData/", summary="新增表格", name="添加表格")
async def query_by(params: dict):
    # print("shuju", params)
    try:
        data = params.get("data")
        # name = params.get("name")
        # print(data)
        df = pd.DataFrame(data)
        df.to_excel('weld_function/get_data/normal.xlsx', index=False)

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
        print(formatted_data)

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
        print("filterData_3", result["centerData"])
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



@router.post("/weld/test/", summary="测试表格", name="测试表格")
async def create_upload_file(file: UploadFile = File(...)):
    # 检查文件类型，确保是表格文件
    if file.content_type != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        return {"error": "只接受Excel表格文件 (.xlsx)"}

    # 保存文件到本地
    #
    # with open(f'weld_function/get_data/normal.xlsx', "wb") as f:
    #     f.write(file.file.read())
    try:
        # # 指定文件夹名称
        # folder_name = "get_data/normal.xlsx"
        # # 获取当前项目的根目录
        # base_path = Path(__file__).resolve().parent
        # # 拼接文件夹的完整路径
        # save_path = base_path / folder_name
        save_path = 'weld_function/get_data/normal.xlsx'

        with open(f'{save_path}', "wb") as f:
            f.write(file.file.read())
        # return {"get_data": file.filename}
        input_file = 'weld_function/get_data/normal.xlsx'
        output_file = '小波包电压.json'
        time_column = 'SendDate'
        column_name = 'EVoltage'
        threshold = 10

        FilterMethod.process_wavelet_filtering(input_file, output_file, time_column,  column_name, threshold)
        result = output_file
        # df = pd.read_excel('normal.xlsx')
        # # 在这里添加清除数据的逻辑，例如清除所有数据：
        # df = pd.DataFrame(columns=df.columns)
        # # 保存清除后的数据到文件
        # df.to_excel(save_path, index=False)
        # print(result)
        return resp.ok(data=result)
    except Exception as e:
        return resp.fail(resp.DataNotFound, detail=str(e))

@router.get("/get/{id}", summary="根据id查看用户详细信息", name="获取信息")
async def query_user_id(id: int):
    result = await WeldGene.select_by_weld_id(id)
    if result:
        return resp.ok(data=result)
    else:
        raise HTTPException(
            status_code=404, detail="data not found")