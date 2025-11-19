from datetime import datetime
import os  # 用于处理目录和文件路径
from flask import current_app


def init_counter_files():
    """初始化计数相关文件（确保目录存在，避免文件未找到错误）"""
    # 关键：先创建数据目录（如果不存在）
    data_dir = os.path.dirname(current_app.config['TOTAL_COUNT_FILE'])
    if not os.path.exists(data_dir):
        os.makedirs(data_dir, exist_ok=True)  # 自动创建多级目录，exist_ok=True 避免重复创建报错

    # 初始化总访问次数文件（如果不存在）
    if not os.path.exists(current_app.config['TOTAL_COUNT_FILE']):
        with open(current_app.config['TOTAL_COUNT_FILE'], "w", encoding="utf-8") as f:
            f.write("0")  # 初始值为 0

    # 初始化访问日志文件（如果不存在）
    if not os.path.exists(current_app.config['VISIT_LOG_FILE']):
        with open(current_app.config['VISIT_LOG_FILE'], "w", encoding="utf-8") as f:
            f.write("")  # 空文件初始化


def get_count():
    """获取当前总访问次数"""
    try:
        # 读取文件内容，若文件不存在则返回 0
        with open(current_app.config['TOTAL_COUNT_FILE'], "r", encoding="utf-8") as f:
            content = f.read().strip()
            return int(content) if content.isdigit() else 0
    except (FileNotFoundError, ValueError):
        return 0  # 异常情况返回默认值 0


def update_count(ip_addr):
    """更新访问记录：同时更新总次数和详细日志"""
    current_count = get_count()
    new_count = current_count + 1  # 累加次数

    # 更新总次数文件
    try:
        with open(current_app.config['TOTAL_COUNT_FILE'], "w", encoding="utf-8") as f:
            f.write(str(new_count))
    except Exception as e:
        print(f"更新总次数失败：{e}")  # 调试用：打印错误信息

    # 记录详细访问日志（时间、次数、IP）
    try:
        time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 格式化时间
        log_entry = f"[{time_str}] 第{new_count}次访问，IP: {ip_addr}\n"
        with open(current_app.config['VISIT_LOG_FILE'], "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as e:
        print(f"记录访问日志失败：{e}")  # 调试用：打印错误信息

    return new_count  # 返回更新后的次数