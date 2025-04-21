# eudic-maimemo-sync

[![License: MPL 2.0](https://img.shields.io/badge/License-MPL%202.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0)

## 项目介绍

将[欧路词典](https://www.eudic.net/v4/en/app/eudic)生词本同步到[墨墨背单词](https://www.maimemo.com/)云词库的 Python 工具。该脚本可以将你在欧路词典查询的单词（如果你设置了查询自动添加到生词本），同步到墨墨背单词的词库中。

详细教程：https://wulu.zone/posts/eudic-maimemo-sync

## 功能特点

- 通过[欧路词典 API](https://my.eudic.net/OpenAPI/doc_api_study#-studylistapi-getwords) 获取指定生词本的单词列表
- 通过[墨墨背单词 API](https://open.maimemo.com/#/operations/maimemo.openapi.notepad.v1.NotepadService.UpdateNotepad) 添加单词到指定云词库
- 支持通过 Docker 部署（ARM64），实现定时自动同步

## 配置

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 获取欧路词典 API 密钥

获取API密钥：https://my.eudic.net/OpenAPI/Authorization

### 3. 获取墨墨背单词 API 密钥

获取API密钥：打开 墨墨背单词 App，依次进入「我的」->「更多设置」->「实验功能」->「开放 API」获取

### 4. 添加环境变量

a. 复制 `.env.example` 为 `.env`

b. 填写以下必需的环境变量：
   - `EUDIC_API_KEY`：欧路词典 API 密钥
   - `EUDIC_CATEGORY_ID`：一般为0。你也可以在填写密钥后，通过运行 **get_wordbook_id.py** 获取。
   - `MOMO_API_KEY`：墨墨背单词 API 密钥
   - `MOMO_NOTEPAD_ID`：在填写密钥后，运行 **get_notepad_id.py** 获取。

## 使用方法

### 手动同步

```bash
python sync.py
```

### 自动同步（部署到树莓派上或者其他 Linux 设备）

> [!NOTE]  
> Docker 镜像目前支持 arm64。在树莓派5上测试过。

创建一个`docker-compose.yml`配置文件, 内容如下:  
  
```
services:
  eudic-maimemo-sync:
    image: ghcr.io/emuqi/eudic-maimemo-sync:latest
    container_name: eudic-maimemo-sync
    restart: unless-stopped
    env_file:
      - .env
    # volumes:
    #   - ./words_data.txt:/app/words_data.txt # 如果想查看单词记录，取消此行和上一行的注释
    environment:
      - TZ=Asia/Shanghai
      - RUN_ON_STARTUP=true # 设置为 true 时，容器每次启动时会执行一次同步任务
      # CRON 定时任务表达式配置:
      # 示例：每小时的第 0 分钟执行（即整点执行）
      # - CRON_SCHEDULE=0 * * * *
      # 示例：每天凌晨 3:15 执行
      - CRON_SCHEDULE=15 3 * * *
      # 请确保所有必需的环境变量（如 EUDIC_API_KEY 等）已在 .env 文件中定义或在此处直接指定。
    healthcheck:
      test: ["CMD-SHELL", "pgrep supercronic || exit 1"]
      interval: 2m
      timeout: 5s
      retries: 3
      start_period: 10s
```

你可以通过`CRON_SCHEDULE`来设置任务的运行周期：

- `CRON_SCHEDULE=0 * * * *`:  每小时的第 0 分钟执行（即整点执行）
- `CRON_SCHEDULE=15 3 * * *`: 每天凌晨 3:15 执行

在相同目录下创建一个`words_data.txt`文件，用于记录同步的单词列表，方便调试或查看。如果不需要，可以跳过此步。    

```
touch words_data.txt
```

运行程序

```
docker compose up -d
```

## 许可证

本项目采用 [Mozilla Public License Version 2.0](https://www.mozilla.org/en-US/MPL/2.0/) 许可证。