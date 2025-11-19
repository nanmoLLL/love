import os
from datetime import datetime
from flask import current_app
from app.utils.common import ensure_data_dir


def init_wishlist_file():
    """初始化愿望清单文件（如果不存在则创建）"""
    try:
        ensure_data_dir()
        wish_file = current_app.config.get('WISHLIST_FILE', os.path.join(current_app.root_path, 'data', 'wishlist.txt'))

        if not os.path.exists(wish_file):
            with open(wish_file, 'w', encoding='utf-8') as f:
                f.write('')
            print(f"愿望清单文件已初始化：{wish_file}")
    except Exception as e:
        print(f"初始化愿望清单文件失败：{str(e)}")


def get_wishes():
    """获取所有愿望列表（添加ID+按时间排序）"""
    wishlist = []
    wish_file = current_app.config.get('WISHLIST_FILE', os.path.join(current_app.root_path, 'data', 'wishlist.txt'))

    if not os.path.exists(wish_file):
        return wishlist

    try:
        with open(wish_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # 为每个愿望添加ID并按时间排序
        for idx, line in enumerate(lines):
            line = line.strip()
            if line:
                parts = line.split('|', 7)  # 增加到8个字段以支持描述
                if len(parts) >= 4:  # 确保有基本字段
                    # 解析图片列表
                    images = parts[6].split(',') if len(parts) > 6 and parts[6] else []
                    images = [img for img in images if img.strip()]  # 过滤空值

                    wish = {
                        'id': idx + 1,  # 添加自增ID
                        'index': idx,  # 保留原索引用于操作
                        'checked': parts[0] == '1',
                        'time': parts[1],
                        'ip': parts[2],
                        'content': parts[3],
                        'reply': parts[4] if len(parts) > 4 else '',
                        'reply_time': parts[5] if len(parts) > 5 else '',
                        'images': images,  # 图片列表
                        'description': parts[7] if len(parts) > 7 else ''  # 详细描述
                    }
                    wishlist.append(wish)

        # 按时间倒序排列（最新的在前面）
        wishlist.sort(key=lambda x: x['time'], reverse=True)

    except Exception as e:
        print(f"读取愿望列表失败：{str(e)}")

    return wishlist


def add_wish(content, ip_addr):
    """添加新愿望"""
    if not content.strip():
        print("愿望内容为空，跳过写入")
        return

    try:
        ensure_data_dir()
        wish_file = current_app.config.get('WISHLIST_FILE', os.path.join(current_app.root_path, 'data', 'wishlist.txt'))
        time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"0|{time_str}|{ip_addr}|{content}|||||\n"  # 增加一个空字段用于描述

        with open(wish_file, "a", encoding="utf-8") as f:
            f.write(line)
        print(f"愿望写入成功：{wish_file}")

    except Exception as e:
        print(f"添加愿望失败：{str(e)}")


def toggle_wish_status(index, checked):
    """切换愿望完成状态"""
    wish_file = current_app.config.get('WISHLIST_FILE', os.path.join(current_app.root_path, 'data', 'wishlist.txt'))

    if not os.path.exists(wish_file):
        return False

    try:
        with open(wish_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if 0 <= index < len(lines):
            parts = lines[index].strip().split('|', 7)  # 支持8个字段
            if len(parts) >= 1:
                parts[0] = '1' if checked else '0'
                # 确保字段数量足够
                while len(parts) < 8:
                    parts.append('')
                lines[index] = '|'.join(parts) + '\n'

                with open(wish_file, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                return True
    except Exception as e:
        print(f"切换愿望状态失败：{str(e)}")

    return False


def reply_wish(index, reply_content, admin_ip):
    """回复愿望"""
    wish_file = current_app.config.get('WISHLIST_FILE', os.path.join(current_app.root_path, 'data', 'wishlist.txt'))

    if not os.path.exists(wish_file):
        return False

    try:
        with open(wish_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if 0 <= index < len(lines):
            parts = lines[index].strip().split('|', 7)
            while len(parts) < 8:
                parts.append('')

            parts[4] = reply_content
            parts[5] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            parts[6] = admin_ip  # 这里改为存储图片，回复功能需要调整

            lines[index] = '|'.join(parts) + '\n'

            with open(wish_file, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            return True
    except Exception as e:
        print(f"回复愿望失败：{str(e)}")

    return False


def delete_wish(index):
    """删除愿望"""
    wish_file = current_app.config.get('WISHLIST_FILE', os.path.join(current_app.root_path, 'data', 'wishlist.txt'))

    if not os.path.exists(wish_file):
        return False

    try:
        with open(wish_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if 0 <= index < len(lines):
            del lines[index]

            with open(wish_file, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            return True
    except Exception as e:
        print(f"删除愿望失败：{str(e)}")

    return False


def save_wish_details(index, title, description, new_images=None, deleted_images=None):
    """保存愿望详情（标题、描述、图片）"""
    wish_file = current_app.config.get('WISHLIST_FILE', os.path.join(current_app.root_path, 'data', 'wishlist.txt'))

    if not os.path.exists(wish_file):
        return False

    try:
        with open(wish_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if 0 <= index < len(lines):
            parts = lines[index].strip().split('|', 7)
            # 确保字段数量足够
            while len(parts) < 8:
                parts.append('')

            # 更新标题（content字段）
            parts[3] = title

            # 更新描述（第8个字段）
            parts[7] = description

            # 处理图片
            current_images = parts[6].split(',') if parts[6] else []
            current_images = [img for img in current_images if img.strip()]

            # 删除图片
            if deleted_images:
                current_images = [img for img in current_images if img not in deleted_images]

            # 添加新图片
            if new_images:
                current_images.extend(new_images)

            # 更新图片字段
            parts[6] = ','.join(current_images)

            lines[index] = '|'.join(parts) + '\n'

            with open(wish_file, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            return True
    except Exception as e:
        print(f"保存愿望详情失败：{str(e)}")

    return False