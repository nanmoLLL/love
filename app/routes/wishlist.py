from flask import Blueprint, render_template, request, jsonify
from app.utils.wishlist import get_wishes, add_wish, toggle_wish_status

wishlist_bp = Blueprint('wishlist', __name__)


@wishlist_bp.route("/wishlist", methods=["GET", "POST"])
def wishlist():
    if request.method == "POST":
        action = request.form.get('action')

        if action == 'add':
            content = request.form.get('content', '').strip()
            if content:
                add_wish(content, request.remote_addr)
                return jsonify({"status": "success"})

        elif action == 'toggle':
            index = request.form.get('index')
            if index is not None:
                toggle_wish_status(int(index))
                return jsonify({"status": "success"})

        return jsonify({"status": "error"})

    # GET请求，展示愿望清单
    wishes = get_wishes()
    return render_template('wishlist.html', wishes=wishes)