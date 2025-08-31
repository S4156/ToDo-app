"""  
アプリケーションの本体。  
アプリの初期化、DBへの接続、Blueprintの登録を行う。
"""
import os
from dotenv import load_dotenv

from flask import Flask
from flask_migrate import Migrate


from extensions import db, login_manager
from auth_routes import auth_bp
from task_routes import task_bp
from admin_tools import bp as admin_bp

# from models import *

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or os.urandom(24)


# DB接続設定
raw_db_url = os.environ.get("DATABASE_URL")
if raw_db_url.startswith("postgresql://"):
    db_url = raw_db_url.replace("postgresql://", "postgresql+psycopg://", 1)
else:
    db_url = raw_db_url
app.config["SQLALCHEMY_DATABASE_URI"] = db_url

db.init_app(app)
login_manager.init_app(app)
migrate = Migrate(app, db)


# ルーティング登録
app.register_blueprint(auth_bp)
app.register_blueprint(task_bp)
app.register_blueprint(admin_bp)

if __name__ == "__main__":
    app.run(debug=True)

if __name__ != "__main__":
    with app.app_context():
        db.create_all()