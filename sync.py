import os
import requests
import json
from collections import defaultdict
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta

def fetch_word_list():
    """获取欧路词典生词本"""
    load_dotenv()
    
    headers = {
        "Authorization": os.getenv("EUDIC_API_KEY"),
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    }
    
    url = "https://api.frdic.com/api/open/v1/studylist/words/{id}".format(id=os.getenv("EUDIC_CATEGORY_ID"))

    try:
        response = requests.get(url, headers=headers, params={"language": "en"})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"[ERROR] 获取单词列表失败: {e}")
        return None

def generate_word_output(word_data):
    """生成按日期分组的单词字符串，并将UTC时间转换为中国时间"""
    if not word_data or 'data' not in word_data:
        return ""

    # 中国时区 (UTC+8)
    china_tz = timezone(timedelta(hours=8))
    
    grouped_words = defaultdict(list)
    for item in word_data['data']:
        # 解析UTC时间
        utc_time = datetime.fromisoformat(item["add_time"].replace('Z', '+00:00'))
        # 转换为中国时间
        china_time = utc_time.astimezone(china_tz)
        # 获取中国时区的日期
        date = china_time.strftime("%Y-%m-%d")
        
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
        print(f"[ERROR] 更新墨墨生词本失败: {e}")
        return None

def save_words_to_file(word_data, filename="words_data.txt"):
    """将单词列表保存到文件中"""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(generate_word_output(word_data))
        return True
    except Exception as e:
        print(f"[ERROR] 保存单词列表到文件失败: {e}")
        return False

def main():
    start_time = datetime.now()
    print(f"[INFO] 开始同步 - {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 获取欧路单词
    print("[INFO] 正在获取欧路词典单词...")
    word_data = fetch_word_list()
    
    if word_data:
        # 保存单词列表到文件
        word_count = len(word_data.get('data', []))
        print(f"[INFO] 获取到 {word_count} 个单词，正在保存到本地文件...")
        save_words_to_file(word_data)
        
        # 生成输出并同步到墨墨
        output_string = generate_word_output(word_data)
        print("[INFO] 正在同步到墨墨背单词...")
        response = update_maimemo_notepad(output_string)
        
        if response and response.get('success'):
            print("[SUCCESS] 同步完成!")
        else:
            print("[ERROR] 同步失败!")
    else:
        print("[ERROR] 未获取到欧路词典单词，同步终止")
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    print(f"[INFO] 同步结束 - {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[INFO] 总耗时: {duration:.2f} 秒")

if __name__ == "__main__":
    main()