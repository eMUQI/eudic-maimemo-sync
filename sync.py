import os
import requests
from collections import defaultdict
from dotenv import load_dotenv

def fetch_word_list():
    """获取欧路词典生词本"""
    load_dotenv()
    
    headers = {
        "Authorization": os.getenv("EUDIC_API_KEY"),
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    }
    
    url = "https://api.frdic.com/api/open/v1/studylist/words/{id}".format(id=os.getenv("EUDIC_CATEFORY_ID"))

    try:
        response = requests.get(url, headers=headers, params={"language": "en"})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"获取单词列表失败: {e}")
        return None

def generate_word_output(word_data):
    """生成按日期分组的单词字符串"""
    if not word_data or 'data' not in word_data:
        return ""

    grouped_words = defaultdict(list)
    for item in word_data['data']:
        date = item["add_time"].split("T")[0]
        grouped_words[date].append(item["word"])

    output_string = ""
    for date in sorted(grouped_words.keys()):
        output_string += f"#{date}\n"
        output_string += "\n".join(grouped_words[date])
        output_string += "\n"

    return output_string

def update_maimemo_notepad(content):
    """同步到墨墨背单词"""
    # 加载环境变量
    load_dotenv()
    
    # 获取 API 密钥和笔记本 ID
    api_key = os.getenv("MOMO_API_KEY")
    notepad_id = os.getenv("MOMO_NOTEPAD_ID")
    
    # 请求 URL
    url = f"https://open.maimemo.com/open/api/v1/notepads/{notepad_id}"
    
    # 请求头
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    # 请求数据
    payload = {
        "notepad": {
            "status": "UNPUBLISHED",
            "content": content,
            "title": "欧路生词",
            "brief": "欧路词典上查询过的单词",
            "tags": ["自用"]
        }
    }
    
    try:
        # 发送 POST 请求
        response = requests.post(url, json=payload, headers=headers)
        
        # 检查响应
        response.raise_for_status()
        
        return response.json()
    except requests.RequestException as e:
        print(f"更新墨墨生词本失败: {e}")
        return None

def main():
    word_data = fetch_word_list()
    if word_data:
        output_string = generate_word_output(word_data)
        update_maimemo_notepad(output_string)
        print(output_string)

if __name__ == "__main__":
    main()