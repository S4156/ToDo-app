"""
管理者用のYouTube動画検索・登録モジュール。

Flaskアプリの管理者のみが利用可能な以下の機能を提供します：

- YouTube Data API を使って動画をキーワードで検索
- 検索結果とカテゴリをデータベースへ追加
- 管理者チェック付きのルート制御
"""
from functools import wraps

from flask import Blueprint, request, render_template, redirect, url_for, flash,abort
from flask_login import current_user,login_required

from extensions import db
from models import RewardVideo
from youtube_utils import search_youtube  # APIで動画を取得する関数



bp = Blueprint('admin_tools', __name__, url_prefix='/admin')

def admin_required(f):
    """
    管理者（is_admin=True）のみにルートアクセスを許可するデコレーター。

    Flask-Login の current_user を使用して、ログイン済みかつ管理者であるかを確認。
    条件を満たさない場合は 403 Forbidden を返す。

    Args:
        f (function): デコレートされる関数。

    Returns:
        function: 管理者チェックを挟んだ新しい関数。
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

#Youtube動画追加用の管理ページ
@bp.route('/search', methods=['GET', 'POST'])
@login_required
@admin_required
def search():
    """
    管理者用：YouTube動画の検索とカテゴリ指定による一括登録を行う画面。

    GET:
        admin/search.html を表示し、フォームを提供。

    POST:
        - 入力されたキーワードをもとに YouTube 動画を検索。
        - すでに登録されていない動画のみ、指定カテゴリと共にデータベースに保存。
        - 成功・スキップ件数を flash メッセージで通知。

    Returns:
        str | Response: GET 時はテンプレートをレンダリング、POST 時はリダイレクト。
    """
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        if not keyword:
            flash("キーワードを入力してください")
            return redirect(url_for('admin_tools.search'))

        videos = search_youtube(keyword, max_results=50)
        added_count = 0
        skipped_count = 0

        for video in videos:
            # 重複チェック：同じ youtube_id が既にDBへ登録されていないか確認
            exists = RewardVideo.query.filter_by(youtube_id=video['id']).first()
            if exists:
                skipped_count += 1
                continue

            new_video = RewardVideo(
                youtube_id=video['id'],
                title=video['title'],
                category=keyword  # キーワードをカテゴリとして使う
            )
            db.session.add(new_video)
            added_count += 1

        db.session.commit()

        flash(f"{added_count}件の動画を登録しました。{skipped_count}件は既に登録済みでした。","success")
        return redirect(url_for('admin_tools.search'))

    return render_template('admin/search.html')
