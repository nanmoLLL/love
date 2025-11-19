import os


class Config:
    # 项目根目录：当前文件（config.py）所在目录的父目录（即项目根目录 xiaohui）
    # 例如：若 config.py 在 xiaohui/app/config.py，则 BASE_DIR 为 xiaohui
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    # 数据存储目录（在项目根目录下创建 data 文件夹）
    DATA_DIR = os.path.join(BASE_DIR, 'data')

    # 计数相关文件路径
    TOTAL_COUNT_FILE = os.path.join(DATA_DIR, 'total_count.txt')  # 总访问次数文件
    VISIT_LOG_FILE = os.path.join(DATA_DIR, 'visit_log.txt')  # 访问日志文件

    # 其他数据文件路径（统一放在 data 目录下）
    MESSAGE_FILE = os.path.join(DATA_DIR, 'messages.txt')  # 留言文件
    WISHLIST_FILE = os.path.join(DATA_DIR, 'wishlist.txt')  # 愿望清单文件