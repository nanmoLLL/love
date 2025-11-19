# app/__init__.py
from flask import Flask
from config import Config
import os
from app.utils.wishlist import init_wishlist_file

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 初始化数据目录和文件
    with app.app_context():
        from app.utils.wishlist import init_wishlist_file
        from app.utils.common import ensure_data_dir

        ensure_data_dir()  # 确保数据目录存在
        init_wishlist_file()  # 初始化愿望清单文件

    # 注册蓝图
    from app.routes import main_bp, love_notes_bp, wishlist_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(love_notes_bp)
    app.register_blueprint(wishlist_bp)

    return app