import re
from flask import Flask, jsonify, request, render_template, make_response, session
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from flask_cors import CORS
import os

import pprint

from blog_control.user_mgmt import User
from blog_view import blog

# https 만을 지원하는 기능을 http 에서 테스트할 때 필요한 설정
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# 앱 팩토리 구성
def create_app():
    # html 모여있는 static 폴더 알려주기
    app = Flask(__name__, static_url_path="/static")
    CORS(app)
    app.secret_key = "dave_server3"

    # 블루프린트
    app.register_blueprint(blog.bp)

    return app


app = create_app()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return make_response(jsonify(success=False), 401)


@app.before_request
def app_before_request():
    session["client_id"] = request.environ.get("HTTP_X_REAL_IP", request.remote_addr)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080", debug=True)
