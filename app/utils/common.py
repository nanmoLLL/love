# app/utils/common.py
import os
from flask import request, current_app


def ensure_data_dir():
    """确保数据目录存在（如果不存在则创建）"""
    data_dir = current_app.config.get('DATA_DIR', os.path.join(current_app.root_path, 'data'))
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"数据目录已创建：{data_dir}")


def get_client_ip(request_obj=None):
    """
    获取客户端真实IP地址
    :param request_obj: Flask的request对象（可选，默认从上下文获取）
    """
    # 如果没有传入request，从Flask上下文获取
    req = request_obj or request

    if req.headers.get('X-Forwarded-For'):
        return req.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif req.headers.get('X-Real-IP'):
        return req.headers.get('X-Real-IP')
    else:
        return req.remote_addr or 'unknown'


def get_total_visits():
    """获取总访问量"""
    count_file = current_app.config.get('TOTAL_COUNT_FILE',
                                        os.path.join(current_app.root_path, 'data', 'total_count.txt'))
    ensure_data_dir()
    if os.path.exists(count_file):
        with open(count_file, 'r', encoding='utf-8') as f:
            return int(f.read().strip() or 0)
    return 0


def update_visit_count():
    """更新访问量计数"""
    count_file = current_app.config.get('TOTAL_COUNT_FILE',
                                        os.path.join(current_app.root_path, 'data', 'total_count.txt'))
    ensure_data_dir()
    current_count = get_total_visits()
    with open(count_file, 'w', encoding='utf-8') as f:
        f.write(str(current_count + 1))