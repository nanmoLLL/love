from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from app.utils.wishlist import get_wishes, add_wish, toggle_wish_status, update_wish_detail, get_wish_detail, \
    add_wish_note
import os

wishlist_bp = Blueprint('wishlist', __name__)


# 愿望清单页面
@wishlist_bp.route('/wishlist')
def wishlist():
    wishes = get_wishes()  # 获取所有愿望（已修复解析逻辑）
    pending_wishes = [w for w in wishes if not w['completed']]
    completed_wishes = [w for w in wishes if w['completed']]
    return render_template('wishlist.html',
                           pending_wishes=pending_wishes,
                           completed_wishes=completed_wishes,
                           pending_count=len(pending_wishes))


# 添加愿望（修复重定向问题）
@wishlist_bp.route('/wishlist', methods=['POST'])
def add_wish_route():
    wish_content = request.form.get('wish', '').strip()
    if wish_content:
        add_wish(wish_content, request.remote_addr)  # 调用修复后的add_wish函数
    # 用绝对路径重定向，避免路由跳转错误
    return redirect(url_for('wishlist.wishlist', _external=True))


# 切换愿望状态
@wishlist_bp.route('/wishlist/toggle', methods=['POST'])
def toggle_wish():
    index = int(request.form.get('index', -1))
    if index != -1:
        toggle_wish_status(index)
    return redirect(url_for('wishlist.wishlist', _external=True))


# 更新愿望详情（文本+图片）
@wishlist_bp.route('/wishlist/update-detail', methods=['POST'])
def update_detail():
    index = int(request.form.get('index', -1))
    detail_text = request.form.get('detail_text', '').strip()

    # 处理图片上传
    image_paths = []
    if 'images' in request.files:
        upload_dir = os.path.join(os.path.dirname(__file__), '../static/uploads')
        os.makedirs(upload_dir, exist_ok=True)

        for image in request.files.getlist('images'):
            if image.filename:
                filename = f"{os.urandom(16).hex()}_{image.filename}"
                filepath = os.path.join(upload_dir, filename)
                image.save(filepath)
                image_paths.append(f'/static/uploads/{filename}')

    if index != -1:
        update_wish_detail(index, detail_text, image_paths)
    return jsonify({'status': 'success'})


# 获取愿望详情
@wishlist_bp.route('/wishlist/get-detail')
def get_detail():
    index = int(request.args.get('index', -1))
    if index != -1:
        wish = get_wish_detail(index)
        return jsonify(wish)
    return jsonify({})


# 添加愿望备注
@wishlist_bp.route('/wishlist/add-note', methods=['POST'])
def add_note():
    index = int(request.form.get('index', -1))
    note = request.form.get('note', '').strip()
    if index != -1 and note:
        add_wish_note(index, note)
    return jsonify({'status': 'success'})