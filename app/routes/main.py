from flask import Blueprint, render_template, request, jsonify
import random
from app.utils.counter import get_count, update_count
from app.utils.messages import save_message

main_bp = Blueprint('main', __name__)


@main_bp.route("/", methods=["GET", "POST"])
def love_page():
    if request.method == "POST":
        # 处理AJAX提交的留言
        message = request.form.get("message", "")
        visitor_ip = request.remote_addr
        save_message(message, visitor_ip)
        return jsonify({"status": "success"})

    # 获取访问者IP地址并更新计数
    visitor_ip = request.remote_addr
    current_count = update_count(visitor_ip)
    surprise_text = ""
    target_counts = [2, 4, 7, 99, 520, 1314, 9999]

    if current_count in target_counts:
        texts = {
            2: "你又来看我啦～ 其实每次你点开，我都很开心",
            99: "九十九，只是一个开始。但我已经看到，那条名为“永远”的路的轮廓",
            520: "520次访问！这可不是巧合，这是你在我心里留下的脚印",
            1314: "谢谢你，用1314次点击，陪我走过这段心路。接下来的路，我也想陪你一起走",
            9999: "你过的还好吗，能不能嫁给我"
        }
        surprise_text = texts.get(current_count, "")

    message = '''
    我曾以为自己是一座孤岛，直到你的出现像一艘船<br>
    不是为了靠岸，而是让我明白：孤独的意义，是为了遇见打破孤独的人<br>
    我们谈论的每句话，都是在彼此的世界里种下的树<br>
    慢慢长出的枝叶，让两个独立的宇宙有了重叠的阴影<br>
    或许喜欢，就是允许另一个人参与你的存在
    '''

    return render_template(
        'index.html',
        surprise_text=surprise_text,
        random=random,
        message=message
    )