from flask import Flask, request, render_template
import random

app = Flask(__name__)

messages = ["클컴컴", "아이티", "사보", "메카", "공전", "화이팅.."]

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""

    if request.method == "POST":
        text = request.form.get("user_input")

        if text == "":
            result = "입력 값이 없습니다! 문장을 입력해주세요."
        else:
            random_text = random.choice(messages)
            result = f'입력하신 문장: "{text}" 랜덤 메시지: "{random_text}"'

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run()
