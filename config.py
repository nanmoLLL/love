import os

class Config:
    # 项目根目录
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # 适配多级目录
    # 数据存储目录（确保在项目根目录下的data文件夹）
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    # 愿望清单文件路径
    WISHLIST_FILE = os.path.join(DATA_DIR, 'wishlist.txt')
    # 其他配置（如果有）
    TOTAL_COUNT_FILE = os.path.join(DATA_DIR, 'total_count.txt')
    VISIT_LOG_FILE = os.path.join(DATA_DIR, 'visit_log.txt')
    MESSAGE_FILE = os.path.join(DATA_DIR, 'messages.txt')