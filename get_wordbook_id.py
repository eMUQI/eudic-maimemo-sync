import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("EUDIC_API_KEY")

# 配置项
BASE_URL = "https://api.frdic.com/api/open/v1/studylist/category"
LANGUAGE = "en"  #'en', 'fr', 'de', 'es'

# 请求头
headers = {
    "Authorization": f"{API_KEY}",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
}

# 请求参数
params = {
    "language": LANGUAGE,
}

# 发起请求
response = requests.get(BASE_URL, headers=headers, params=params)

# 处理响应
if response.status_code == 200:
    data = response.json()
    if data and 'data' in data and isinstance(data['data'], list):
        vocabulary_lists = data['data']
        if vocabulary_lists:
            print("您的词汇列表:")
            for vocab_list in vocabulary_lists:
                print(f"- 列表名称: {vocab_list['name']}")
                print(f"  列表ID  : {vocab_list['id']}")
                print(f"  创建时间: {vocab_list['add_time']}")
                print("-" * 20)
        else:
            print("没有找到任何词汇列表。")
    else:
        print("请求成功，但返回的数据格式不正确。")
        print("返回的原始数据：", data)
else:
    print(f"请求失败，状态码：{response.status_code}")
    print(f"错误信息：{response.text}")