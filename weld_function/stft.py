import scipy.signal as signal
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# fs=1024 #采样频率
# dt=pd.read_excel('burnthrough.xlsx')
# # 一维数据
# data=dt['ECurrent'].values
#
# # 使用 signal.stft 进行短时傅里叶变换
# # f: 频率数组
# # t: 时间数组
# # nd: 短时傅里叶变换的结果（复数数组，表示幅度和相位）
# f, t, nd = signal.stft(data,fs=fs,window='hann',nperseg=256,noverlap=None,nfft=None,
#                        detrend=False,return_onesided=True,boundary='zeros',padded=True,axis=-1)
# # 绘制时频图，x轴为t，y轴为f，绘制np.abs(nd)的绝对值，设置最小值为0，最大值为4
# plt.pcolormesh(t, f, np.abs(nd), vmin = 0, vmax = 4)
# plt.title('STFT')
# plt.ylabel('frequency')
# plt.xlabel('time')
# plt.show()

# async def stft(cls,route):
#     fs = 1024  # 采样频率
#     route = route
#     dt = pd.read_excel(route)
#     # 一维数据
#     data = dt['ECurrent'].values
#
#     # 使用 signal.stft 进行短时傅里叶变换
#     # f: 频率数组
#     # t: 时间数组
#     # nd: 短时傅里叶变换的结果（复数数组，表示幅度和相位）
#     f, t, nd = signal.stft(data, fs=fs, window='hann', nperseg=256, noverlap=None, nfft=None,
#                            detrend=False, return_onesided=True, boundary='zeros', padded=True, axis=-1)
#     # 绘制时频图，x轴为t，y轴为f，绘制np.abs(nd)的绝对值，设置最小值为0，最大值为4
#     plt.pcolormesh(t, f, np.abs(nd), vmin=0, vmax=4)
#     plt.title('STFT')
#     plt.ylabel('frequency')
#     plt.xlabel('time')
#     plt.show()
#
import numpy as np
import matplotlib.pyplot as plt
import pywt
import pandas as pd
from scipy.signal import savgol_filter
from scipy.signal import medfilt
import json
import pandas as pd
from scipy.stats import kurtosis
import numpy as np
from scipy.stats import entropy

from schemas.response import resp


class DataAnalyzer:
    def __init__(self, excel_file_path, column_to_split, num_splits=10):
        self.excel_file_path = excel_file_path
        self.column_to_split = column_to_split
        self.num_splits = num_splits
        self.df = pd.read_excel(excel_file_path)
        self.column_data = self.df[column_to_split]
        self.split_data = self.split_data()

    def split_data(self):
        split_data = np.array_split(self.column_data, self.num_splits)
        remainder = len(self.column_data) % self.num_splits
        if remainder > 0:
            split_data[-1] = split_data[-1].append(self.column_data.tail(remainder))
        return split_data

    def calculate_kurtosis(self):
        print(f"计算: 峭度")
        for i, subset in enumerate(self.split_data):
            kurtosis_value = kurtosis(subset)
            print(f"区间{i+1}: '{kurtosis_value:.2f}',")

    def calculate_rms(self):
        print(f"计算: 均方根")
        for i, subset in enumerate(self.split_data):
            rms_value = np.sqrt(np.mean(subset**2))
            print(f"区间{i+1}: '{rms_value:.2f}',")

    def calculate_mean_abs_diff(self):
        print(f"计算: 差分绝对值均值")
        for i, subset in enumerate(self.split_data):
            abs_diff_values = np.abs(subset.diff()).dropna()
            mean_abs_diff = np.mean(abs_diff_values)
            print(f"区间{i+1}: '{mean_abs_diff:.2f}',")

    def calculate_median_abs_diff(self):
        print(f"计算: 差分绝对值的中位数")
        for i, subset in enumerate(self.split_data):
            abs_diff_values = np.abs(subset.diff()).dropna()
            median_abs_diff = np.median(abs_diff_values)
            print(f"区间{i+1}: '{median_abs_diff:.2f}',")

    def calculate_entropy(self):
        print(f"计算: 熵")
        for i, subset in enumerate(self.split_data):
            subset_entropy = entropy(subset.value_counts(normalize=True), base=2)
            print(f"区间{i+1}: '{subset_entropy:.2f}',")


# 打印全部数据
    def analyze_data(self):
        self.calculate_kurtosis()
        self.calculate_rms()
        self.calculate_mean_abs_diff()
        self.calculate_median_abs_diff()
        self.calculate_entropy()

# # 示例用法，修改文件名和数据列名
# analyzer = DataAnalyzer(excel_file_path='normal.xlsx', column_to_split='weldCur')
# analyzer.calculate_entropy()


class FilterMethod:

    def process_wavelet_filtering(input_file, output_file, time_column, voltage_column, current_column, threshold, wavelet_name='db4', level=4):
        # 从Excel文件读取数据
        data = pd.read_excel(input_file)

        # 获取时间和电压数据
        t = data[time_column].values
        x_voltage = data[voltage_column].values
        x_current = data[current_column].values

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
        result_list = []
        for i, (time, voltage, current) in enumerate(zip(t, x_voltage_filt[0], x_current_filt[0])):
            result_dict = {
                "id": i + 1,
                "weldTime": str(time),  # 假设时间是一个日期时间对象，如果需要，将其转换为字符串
                "weldVol": voltage,
                "weldCur": current
            }
            result_list.append(result_dict)

        # 创建一个字典列表
        # result_list = []
        # for i, (time, voltage) in enumerate(zip(t, x_filt[0])):
        #     result_dict = {
        #         "id": i + 1,
        #         "weldTime": str(time),  # 假设时间是一个日期时间对象，如果需要，将其转换为字符串
        #         "weldVol": voltage
        #     }
        #     result_list.append(result_dict)

        # result_list = {}
        # for item in re_list:
        #     id_value = item['id']
        #     result_list[id_value] = item
        # json_data = json.dumps(result_list, indent=2)

        # # 将结果列表保存到 JSON 文件中
        # with open(output_file, 'w') as f:
        #     json.dump(result_list, f, indent=2)
        # result = re_list
        # return resp.ok(data=result)

    # 示例用法
    # input_file = 'shaochuan.xlsx'
    # output_file = '小波包电压.json'
    # time_column = 'SendDate'
    # column_name = 'EVoltage'
    # threshold = 10

    #
    # process_wavelet_filtering(input_file, output_file, time_column, column_name, threshold)




    def process_savgol_filter(input_file, output_file, time_column, voltage_column, current_column, window_size=21, poly_order=3):
        # 读取数据
        data = pd.read_excel(input_file)

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
        result_list = []
        for i, (time, voltage, current) in enumerate(zip(t, y_voltage_sg_filter_rounded, y_current_sg_filter_rounded)):
            result_dict = {
                "id": i + 1,
                "weldTime": str(time),  # 假设时间是一个日期时间对象，如果需要，将其转换为字符串
                "weldVol": voltage,
                "weldCur": current
            }
            result_list.append(result_dict)

        # 将结果列表保存到 JSON 文件中
        with open(output_file, 'w') as f:
            json.dump(result_list, f, indent=2)

        # 绘制原始和滤波后的电压数据
        plt.plot(t, y_voltage, label='原始电压')
        plt.plot(t, y_voltage_sg_filter, label=f'Savitzky-Golay 滤波后的电压 (窗口={window_size}, 阶数={poly_order})', color='green')
        plt.xlabel('时间')
        plt.ylabel('电压')
        plt.legend()
        plt.show()

    # # 示例用法
    # input_file = 'shaochuan.xlsx'
    # output_file = 'SG滤波后的数据.json'
    # time_column = 'SendDate'
    # voltage_column = 'EVoltage'
    # current_column = 'ECurrent'
    # window_size = 21
    # poly_order = 3

    # process_savgol_filter(input_file, output_file, time_column, voltage_column, current_column, window_size, poly_order)


    def process_median_filtering(input_file, output_file, time_column, column_name, window_size_1=5, window_size_2=5):
        # 读取数据
        data = pd.read_excel(input_file)

        # 第一次中值滤波
        y_medfilt_1 = medfilt(data[column_name].values, kernel_size=window_size_1)

        # 第二次中值滤波
        y_medfilt_2 = medfilt(y_medfilt_1, kernel_size=window_size_2)

        # 创建包含每个记录的字典列表
        records = []
        for i, (time, vol, cur) in enumerate(zip(data[time_column], y_medfilt_2, y_medfilt_2)):
            record = {
                "id": i + 1,
                "weldTime": str(time),  # 使用时间列的值
                "weldVol": f"{vol:.2f}",  # 保留两位小数
                "weldCur": f"{cur:.2f}"  # 保留两位小数
            }
            records.append(record)

        # 保存JSON格式的数据到txt文件
        with open(output_file, 'w') as f:
            json.dump(records, f, indent=2)

    # # 示例用法
    # input_file = 'shaochuan.xlsx'
    # output_file = '中值滤波后的数据.json'
    # time_column = 'SendDate'
    # column_name = 'EVoltage'
    # window_size_1 = 5
    # window_size_2 = 5

    # process_median_filtering(input_file, output_file, time_column, column_name, window_size_1, window_size_2)
