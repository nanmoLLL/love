from datetime import datetime
import os  # 新增导入
from flask import current_app


def init_counter_files():
    """初始化计数相关文件"""
    # 总次数文件（修正文件存在判断）
    if not os.path.exists(current_app.config['TOTAL_COUNT_FILE']):
        with open(current_app.config['TOTAL_COUNT_FILE'], "w", encoding="utf-8") as f:
            f.write("0")

    # 访问日志文件（修正文件存在判断）
    if not os.path.exists(current_app.config['VISIT_LOG_FILE']):
        with open(current_app.config['VISIT_LOG_FILE'], "w", encoding="utf-8") as f:
            f.write("")


def get_count():
    """获取当前总访问次数"""
    try:
        with open(current_app.config['TOTAL_COUNT_FILE'], "r", encoding="utf-8") as f:
            content = f.read().strip()
            return int(content) if content.isdigit() else 0
    except:
        return 0


def update_count(ip_addr):
    """更新访问记录：同时更新总次数文件和详细日志文件"""
    current_count = get_count()
    new_count = current_count + 1

    # 更新总次数文件
    with open(current_app.config['TOTAL_COUNT_FILE'], "w", encoding="utf-8") as f:
        f.write(str(new_count))

    # 记录详细日志
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(current_app.config['VISIT_LOG_FILE'], "a", encoding="utf-8") as f:
        f.write(f"[{time_str}] 第{new_count}次访问，IP: {ip_addr}\n")

    return new_count