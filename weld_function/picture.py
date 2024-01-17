import base64

import requests

class Method:
    def image_to_base64(cls, url):
        print('here')
        response = requests.get(url)
        print('here2')
        # 检查响应状态码
        if response.status_code == 200:
            # 获取图片内容
            image_content = response.content

            # 将图片内容进行 Base64 编码
            image_base64 = base64.b64encode(image_content)

            # 转换为字符串格式
            image_base64_str = image_base64.decode('utf-8')
            imageBase64Dict = {"imageBase64": image_base64_str}
            return imageBase64Dict
        else:
            # 下载失败，返回空字符串或抛出异常
            return "图片转码失败"