import os
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, current_app, jsonify
from werkzeug.utils import secure_filename
from app.utils.wishlist import get_wishes, add_wish, toggle_wish_status, save_wish_details
from app.utils.common import get_client_ip

wishlist_bp = Blueprint('wishlist', __name__)

# 允许上传的图片扩展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@wishlist_bp.route('/wishlist', methods=['GET', 'POST'])
def wishlist_page():
    if request.method == 'POST':
        content = request.form.get('wish', '').strip()
        if content:
            ip = get_client_ip(request)
            add_wish(content, ip)
        return redirect(url_for('wishlist.wishlist_page'))

    wishes = get_wishes()
    return render_template('wishlist.html', wishes=wishes)


@wishlist_bp.route('/wishlist/toggle/<int:index>', methods=['POST'])
def toggle_wish(index):
    checked = request.form.get('checked', 'false') == 'true'
    toggle_wish_status(index, checked)
    return '', 204


@wishlist_bp.route('/wishlist/save/<int:index>', methods=['POST'])
def save_wish(index):
    try:
        # 获取表单数据
        title = request.form.get('title', '')
        description = request.form.get('description', '')
        wish_id = request.form.get('id', '')

        # 处理图片上传
        uploaded_images = []
        if 'images' in request.files:
            files = request.files.getlist('images')

            # 创建上传目录
            upload_dir = os.path.join(current_app.root_path, 'static', 'uploads')
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)

            for i, file in enumerate(files):
                if file and allowed_file(file.filename):
                    # 生成安全的文件名
                    filename = f"{wish_id}_{i + 1}_{secure_filename(file.filename)}"
                    filepath = os.path.join(upload_dir, filename)
                    file.save(filepath)
                    uploaded_images.append(filename)

        # 处理删除的图片
        deleted_images = []
        if 'deleted_images' in request.form:
            try:
                import json
                deleted_images = json.loads(request.form.get('deleted_images'))
                # 删除文件
                for img in deleted_images:
                    img_path = os.path.join(upload_dir, img)
                    if os.path.exists(img_path):
                        os.remove(img_path)
            except:
                pass

        # 保存愿望详情
        save_wish_details(index, title, description, uploaded_images, deleted_images)

        return jsonify({'success': True}), 200
    except Exception as e:
        print(f"保存愿望详情出错：{str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500