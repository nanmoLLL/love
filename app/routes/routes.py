from flask import Blueprint, render_template, request, redirect, url_for, current_app
from app.utils.wishlist import get_wishlist, add_wish, toggle_wish_check, reply_wish, delete_wish
from app.utils.common import get_client_ip

# 创建蓝图
wishlist_bp = Blueprint('wishlist', __name__)


@wishlist_bp.route('/wishlist')
def wishlist():
    """愿望清单页面"""
    wishes = get_wishlist()
    return render_template('wishlist.html', wishes=wishes)


@wishlist_bp.route('/wishlist', methods=['POST'])
def add_wish_route():
    """添加愿望的接口"""
    # 获取表单中的愿望内容
    wish_content = request.form.get('wish', '').strip()
    client_ip = get_client_ip(request)

    if wish_content:
        print(f"收到新愿望：{wish_content}（IP：{client_ip}）")
        add_wish(wish_content, client_ip)
    else:
        print("未收到愿望内容")

    # 重定向回愿望清单页面
    return redirect(url_for('wishlist.wishlist'))


@wishlist_bp.route('/wishlist/toggle/<int:index>', methods=['POST'])
def toggle_wish(index):
    """切换愿望完成状态"""
    checked = request.form.get('checked', 'false') == 'true'
    toggle_wish_check(index, checked)
    return '', 204


@wishlist_bp.route('/wishlist/reply/<int:index>', methods=['POST'])
def reply_wish_route(index):
    """回复愿望"""
    reply_content = request.form.get('reply', '').strip()
    admin_ip = get_client_ip(request)

    if reply_content:
        reply_wish(index, reply_content, admin_ip)

    return redirect(url_for('wishlist.wishlist'))


@wishlist_bp.route('/wishlist/delete/<int:index>', methods=['POST'])
def delete_wish_route(index):
    """删除愿望"""
    delete_wish(index)
    return redirect(url_for('wishlist.wishlist'))