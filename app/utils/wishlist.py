from datetime import datetime
import os
from flask import current_app


# 确保数据目录存在（修复因目录不存在导致的读写失败）
def ensure_data_dir():
    data_dir = os.path.dirname(current_app.config['WISHLIST_FILE'])
    if not os.path.exists(data_dir):
        os.makedirs(data_dir, exist_ok=True)  # 递归创建目录，避免权限问题


def init_wishlist_file():
    """初始化愿望清单文件（确保文件和目录存在）"""
    ensure_data_dir()
    if not os.path.exists(current_app.config['WISHLIST_FILE']):
        with open(current_app.config['WISHLIST_FILE'], "w", encoding="utf-8") as f:
            f.write("")  # 格式：状态|时间|IP|内容|详情文本|图片路径(逗号分隔)|备注(时间|内容;分隔)


def get_wishes():
    """获取所有愿望（修复解析错误，兼容空行和缺失字段）"""
    wishes = []
    try:
        ensure_data_dir()
        # 若文件不存在，直接返回空列表
        if not os.path.exists(current_app.config['WISHLIST_FILE']):
            return wishes

        with open(current_app.config['WISHLIST_FILE'], "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:  # 跳过空行（关键修复：避免解析空行导致的错误）
                    continue

                # 按分隔符拆分，最多7个字段（兼容旧数据）
                parts = line.split("|", 6)
                # 补全缺失的字段（确保长度为7，避免索引越界）
                while len(parts) < 7:
                    parts.append("")

                status, time, ip, content, detail_text, images, notes = parts
                wishes.append({
                    'completed': status == '1',
                    'time': time,
                    'ip': ip,
                    'content': content,
                    'detail_text': detail_text,
                    'images': images,
                    'notes': notes
                })
    except Exception as e:
        print(f"读取愿望失败：{str(e)}")  # 打印错误信息，方便调试
    return wishes


def add_wish(content, ip_addr):
    """添加新愿望（修复写入格式，确保字段完整）"""
    if not content.strip():  # 过滤空内容
        return
    try:
        ensure_data_dir()
        time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 严格按照格式写入，确保7个字段（状态|时间|IP|内容|详情|图片|备注）
        line = f"0|{time_str}|{ip_addr}|{content}||||\n"  # 后四个字段暂为空
        with open(current_app.config['WISHLIST_FILE'], "a", encoding="utf-8") as f:
            f.write(line)
    except Exception as e:
        print(f"添加愿望失败：{str(e)}")  # 打印错误信息


def toggle_wish_status(index):
    """切换愿望状态（兼容新格式）"""
    wishes = []
    try:
        with open(current_app.config['WISHLIST_FILE'], "r", encoding="utf-8") as f:
            wishes = [line.strip() for line in f if line.strip()]  # 过滤空行

        if 0 <= index < len(wishes):
            parts = wishes[index].split("|", 6)
            while len(parts) < 7:
                parts.append("")
            # 切换状态（0<->1）
            parts[0] = '1' if parts[0] == '0' else '0'
            wishes[index] = "|".join(parts)

            # 写回文件
            with open(current_app.config['WISHLIST_FILE'], "w", encoding="utf-8") as f:
                f.write("\n".join(wishes) + "\n")
    except Exception as e:
        print(f"切换愿望状态失败：{str(e)}")


def update_wish_detail(index, detail_text, image_paths):
    """更新愿望详情（文本+图片）"""
    wishes = []
    try:
        with open(current_app.config['WISHLIST_FILE'], "r", encoding="utf-8") as f:
            wishes = [line.strip() for line in f if line.strip()]

        if 0 <= index < len(wishes):
            parts = wishes[index].split("|", 6)
            while len(parts) < 7:
                parts.append("")
            parts[4] = detail_text  # 详情文本（第5个字段）
            parts[5] = ",".join(image_paths) if image_paths else parts[5]  # 图片路径（第6个字段）
            wishes[index] = "|".join(parts)

            with open(current_app.config['WISHLIST_FILE'], "w", encoding="utf-8") as f:
                f.write("\n".join(wishes) + "\n")
    except Exception as e:
        print(f"更新愿望详情失败：{str(e)}")


def get_wish_detail(index):
    """获取单个愿望详情"""
    wishes = get_wishes()
    if 0 <= index < len(wishes):
        return wishes[index]
    return {}


def add_wish_note(index, note_content):
    """添加愿望备注"""
    wishes = []
    try:
        with open(current_app.config['WISHLIST_FILE'], "r", encoding="utf-8") as f:
            wishes = [line.strip() for line in f if line.strip()]

        if 0 <= index < len(wishes):
            parts = wishes[index].split("|", 6)
            while len(parts) < 7:
                parts.append("")
            # 备注格式：时间|内容;时间|内容...
            time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_note = f"{time_str}|{note_content}"
            parts[6] = f"{parts[6]};{new_note}" if parts[6] else new_note  # 备注（第7个字段）
            wishes[index] = "|".join(parts)

            with open(current_app.config['WISHLIST_FILE'], "w", encoding="utf-8") as f:
                f.write("\n".join(wishes) + "\n")
    except Exception as e:
        print(f"添加备注失败：{str(e)}")