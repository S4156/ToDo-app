"""
Flask拡張機能の初期化用モジュール。
app.pyなどで import して初期化に使用します。
以下の拡張機能を定義します：

- SQLAlchemy: データベース操作用
- LoginManager: ユーザー認証用
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

login_manager.login_view = "auth.login"
login_manager.login_message_category = "error"
