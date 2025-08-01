"""
ユーザー認証モジュール。

以下の機能を提供します：

- ユーザーのログイン
- アカウントの新規登録
- ユーザーのログアウト
"""

from flask import Blueprint, render_template, request, redirect,flash,url_for
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import User
from extensions import db, login_manager

auth_bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    """
    Flask-Loginが現在のユーザーを取得するために使用する関数。
    """
    return User.query.get(int(user_id))

@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    """
    ユーザーログインのためのルート。
    認証失敗時はエラーメッセージを表示してリダイレクト。

    GET: ログインフォームを表示。
    POST: 入力されたユーザー名とパスワードを検証し、正しければログイン状態にする。ログイン後はタスクページへリダイレクト

    Returns:
        Response: テンプレートまたはリダイレクトレスポンス
    """
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect("/")
        flash("ユーザー名、パスワードが違います","warning")
        return redirect(url_for("auth.login"))
    return render_template("login.html")

@auth_bp.route("/signup", methods=['GET', 'POST'])
def signup():
    """
    新規アカウント登録のためのルート。

    GET: ユーザー登録フォームを表示。
    POST: 入力情報を元にユーザーを作成し、データベースに保存。登録後はログインページにリダイレクト。

    Returns:
        Response: テンプレートまたはリダイレクトレスポンス
    """
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        hashed_pass = generate_password_hash(password)
        user = User(username=username, password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    return render_template("signup.html")

@auth_bp.route("/logout")
def logout():
    """
    ユーザーをログアウトするルート。

    現在のセッションを終了し、ログインページへリダイレクトする。

    Returns:
        Response: ログインページへのリダイレクトレスポンス
    """
    logout_user()
    return redirect("/login")
