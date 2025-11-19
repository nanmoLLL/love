from datetime import datetime
import os  # 新增导入
from flask import current_app

def init_message_file():
    """初始化留言文件（修正文件存在判断）"""
    if not os.path.exists(current_app.config['MESSAGE_FILE']):
        with open(current_app.config['MESSAGE_FILE'], "w", encoding="utf-8") as f:
            f.write("")

def save_message(content, ip_addr):
    """保存留言，记录IP地址、时间和内容"""
    if not content.strip():
        return
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(current_app.config['MESSAGE_FILE'], "a", encoding="utf-8") as f:
        f.write(f"[{time_str}] IP: {ip_addr}: {content}\n")