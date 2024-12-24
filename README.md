# eudic-maimemo-sync

## 项目介绍

将[欧路词典](https://www.eudic.net/v4/en/app/eudic)生词本同步到[墨墨背单词](https://www.maimemo.com/)云词库的 Python 工具。该脚本可以将你在欧路词典查询的单词（如果你设置了查询自动添加到生词本），同步到墨墨背单词的词库中。

## 功能特点

- 从[欧路词典 API](https://my.eudic.net/OpenAPI/doc_api_study#-studylistapi-getwords) 获取生词列表
- 通过[墨墨背单词 API](https://open.maimemo.com/#/operations/maimemo.openapi.notepad.v1.NotepadService.UpdateNotepad) 将单词同步到云词库

## 配置

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 获取欧路词典 API 密钥

获取API密钥：https://my.eudic.net/OpenAPI/Authorization


### 3. 获取墨墨背单词 API 密钥

获取API密钥：墨墨背单词APP 我的 - 更多设置 - 实验功能 - 开放API

### 4. 添加环境变量

a. 复制 `.env.example` 为 `.env`

b. 填写以下必需的环境变量：
   - `EUDIC_API_KEY`：欧路词典 API 密钥
   - `EUDIC_CATEFORY_ID`：一般为0。你也可以在填写密钥后，通过运行 **get_wordbook_id.py** 获取。
   - `MOMO_API_KEY`：墨墨背单词 API 密钥
   - `MOMO_NOTEPAD_ID`：在填写密钥后，运行 **get_notepad_id.py** 获取。

## 使用方法

```bash
python sync.py
```


## 路线图

- [x] 更详细的教程
- [ ] 完善异常处理
- [ ] 支持 docker
