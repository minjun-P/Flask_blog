from flask import Flask, Blueprint, request, render_template, redirect, url_for, session
from flask_login import login_user, current_user, logout_user

import datetime

from blog_control.user_mgmt import User
from blog_control.session_mgmt import BlogSession

bp = Blueprint("blog", __name__, url_prefix="/blog")


@bp.route("/set_email", methods=["GET", "POST"])
def set_email():
    if request.method == "GET":
        return redirect(url_for("blog.test_blog"))
    else:
        # content-type이 application/json인 경우만 가능
        user = User.create(request.form["user_email"], request.form["blog_id"])
        login_user(user, remember=True, duration=datetime.timedelta(days=365))

        return redirect(url_for("blog.test_blog"))


@bp.route("/test_blog")
def test_blog():
    if current_user.is_authenticated:
        # current_user는 현재 User.get으로 불러온 USER 객체
        webpage_name = BlogSession.get_blog_page(current_user.blog_id)
        BlogSession.save_session_info(
            session["client_id"], current_user.user_email, webpage_name
        )

        return render_template(webpage_name, user_email=current_user.user_email)
    else:
        # 현재 구독 정보가 없을 때
        webpage_name = BlogSession.get_blog_page()
        BlogSession.save_session_info(session["client_id"], "anonymus", webpage_name)
        return render_template(webpage_name)


@bp.route("/logout")
def logout():
    User.delete(current_user.id)
    logout_user()
    return redirect(url_for("blog.test_blog"))
