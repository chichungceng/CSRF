import base64
import os
from flask import Flask, render_template, request, redirect, url_for, make_response

app=Flask(__name__,static_folder="static",template_folder="templates")

def generate_csrf_token():
    return bytes.decode(base64.b64encode(os.urandom(48)))

@app.route("/",methods=["POST","GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "chichung" and password == "480916":
            response = redirect(url_for("transfer"))
            response.set_cookie("username","password")
            return response
        else:
            print("用户名或密码错误")
    return render_template("000正规途径的登录界面.html")

@app.route("/transfer",methods=["POST","GET"])
def transfer():
    username = request.cookies.get("username")
    if not username:
        return redirect(url_for("login"))
    if request.method == "POST":
        towho = request.form.get("towho")
        money = request.form.get("money")
        csrf_token = request.cookies.get("token")
        if csrf_token != request.form.get("csrf_token"):
            return redirect(url_for("login"))
        return "转账给%s 转账的金额%s 成功！"%(towho,money)

    csrf_token = generate_csrf_token()
    response = make_response(render_template("000正规途径的转账界面.html",token=csrf_token))
    response.set_cookie("token",csrf_token)

    return response


if __name__ == '__main__':
    app.run(debug=True)

