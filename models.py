"""  
データベースの情報を集約したモジュール。
以下のデータベースを定義します:

- User: ユーザー情報（認証用）
- Task: ユーザーのToDoタスク
- RewardVideo: ご褒美として再生するYouTube動画情報
- WatchHistory: 動画の視聴履歴
"""
# from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from flask_login import UserMixin
import pytz

from extensions import db
tokyo_timezone = pytz.timezone('Asia/Tokyo')

def get_tokyo_time():
    """
    東京の時刻を返す
    """
    return datetime.now(tokyo_timezone)

class User(UserMixin, db.Model):
    """
    ユーザー情報を保持するモデル

    Attributes
        id (int): ユーザーID,(主キー)
        username (str): ユーザー名
        password (str): パスワード
        tasks (list[Task]): このユーザーが所有するタスク一覧
        is_admin(bool): 管理者かどうか
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)
    is_admin=db.Column(db.Boolean, default=False)

class Task(db.Model):
    """
    登録されたToDoタスクの情報を保持するモデル

    Attributes
        id (int): タスクID,(主キー)
        content (str): タスクの内容
        created_at (DateTime): タスクを登録した日時
        user_id (int): タスクを作成したユーザーのID (外部キー)
        completed (bool): 完了済みかどうか
        sort_order (int): 並び替えに使用する数値
    """
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=get_tokyo_time)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    sort_order = db.Column(db.Integer, default=0)

class RewardVideo(db.Model):
    """
    ご褒美として使用されるYouTube動画の情報を保持するモデル。

    Attributes:
        id (int): 動画ID (主キー)
        category (str): 動画のカテゴリ (例: 動物、癒し)
        youtube_id (str): YouTubeの動画ID
        title (str): 動画のタイトル
    """
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String)
    youtube_id = db.Column(db.String, nullable=False)
    title = db.Column(db.String)

class WatchHistory(db.Model):
    """
    ユーザーが視聴した動画の履歴を記録するモデル。

    Attributes:
        id (int): 履歴ID(主キー)
        user_id (int): 視聴したユーザーのID(外部キー)
        video_id (int): 視聴された動画のID(外部キー)
        watched_at (datetime): 視聴日時
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('reward_video.id'))
    watched_at = db.Column(db.DateTime(timezone=True), nullable=False, default=get_tokyo_time)
