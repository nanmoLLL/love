import os


class Config:
    # 修复BASE_DIR：当前文件所在目录即为项目根目录（love）
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # 数据存储目录（项目根目录下的data文件夹）
    DATA_DIR = os.path.join(BASE_DIR, 'data')

    # 计数相关文件路径
    TOTAL_COUNT_FILE = os.path.join(DATA_DIR, 'total_count.txt')
    VISIT_LOG_FILE = os.path.join(DATA_DIR, 'visit_log.txt')

    # 消息和愿望清单文件路径（统一放在data下）
    MESSAGE_FILE = os.path.join(DATA_DIR, 'messages.txt')
    WISHLIST_FILE = os.path.join(DATA_DIR, 'wishlist.txt')

    # 其他配置（保持原有内容）
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'