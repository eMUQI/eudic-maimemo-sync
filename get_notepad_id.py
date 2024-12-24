import requests
import os
from dotenv import load_dotenv

load_dotenv()
authorization_token = os.getenv("MOMO_API_KEY")

limits = 10
offset = 0

# 定义URL和Authorization令牌
url = "https://open.maimemo.com/open/api/v1/notepads/"

# 设置请求头
headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {authorization_token}"
}

params = {
    "limits": limits,
    "offset": offset,
}

# 发送GET请求
response = requests.get(url, headers=headers, params=params)

# 输出返回结果
if response.status_code == 200:
    data = response.json()
    if data.get('success'):
        notepads = data.get('data', {}).get('notepads', [])
        if not notepads:
            print("没有找到任何词库。")
        else:
            print("您的词库列表:")
            for notepad in notepads:
                print(f"  词库名称: {notepad['title']}")
                print(f"  词库ID  : {notepad['id']}")
                print(f"  描述    : {notepad.get('brief', '暂无描述')}")  # 使用get方法并提供默认值
                print(f"  创建时间: {notepad['created_time']}")
                print("-" * 20) # 添加分隔符
    else:
        print("获取词库列表失败。")
        if data.get('errors'):
            for error in data['errors']:
                print(f"错误信息: {error}")
else:
    print(f"请求失败，状态码: {response.status_code}")
    print(f"错误详情: {response.text}")