from flask import Flask
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(config_class)

    # 注册路由蓝图
    from app.routes import main_bp, love_notes_bp, wishlist_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(love_notes_bp)
    app.register_blueprint(wishlist_bp)

    # 激活应用上下文后初始化数据文件（修复核心）
    with app.app_context():
        # 初始化数据文件
        from app.utils.counter import init_counter_files
        from app.utils.messages import init_message_file
        from app.utils.wishlist import init_wishlist_file

        init_counter_files()
        init_message_file()
        init_wishlist_file()

    return app