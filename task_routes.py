"""
ToDoアプリケーションにおけるタスク関連のルーティング処理を定義するモジュール。
以下の機能を提供します：

- タスク一覧ページ（トップページ）の表示
- タスクの作成、削除、完了状態の切り替え
- タスクの並び順変更(ドラッグ＆ドロップ)
- カテゴリに基づいたご褒美動画の表示と履歴保存
"""

from datetime import datetime

from flask import Blueprint, render_template, request, redirect, jsonify
from flask_login import login_required,current_user
import pytz

from models import Task,WatchHistory,RewardVideo
from extensions import db


task_bp = Blueprint('tasks', __name__)


@task_bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    """
    ログイン中のユーザーに対応したタスク一覧ページを表示または新しいタスクを追加します。

    GET: タスクの一覧を表示。動画のカテゴリをDBから取得する処理も行う。
    POST: フォームから送信されたタスクをデータベースに追加。

    Returns:
        str: HTMLテンプレートのレンダリング結果。
    """
    user_id = current_user.id
    if request.method == 'POST':
        content = request.form.get("content")
        if content:
            task = Task(content=content, user_id=user_id)
            db.session.add(task)
            db.session.commit()
        return redirect("/")
    categories = db.session.query(RewardVideo.category).distinct().all()
    categories = [c[0] for c in categories if c[0]]
    incomplete_tasks = (
        Task.query
        .filter_by(user_id=user_id, completed=False)
        .order_by(Task.sort_order.asc())
        .all()
    )
    complete_tasks = (
        Task.query
        .filter_by(user_id=user_id, completed=True)
        .order_by(Task.created_at.desc())
        .all()
    )
    return render_template(
        "index.html",
        incomplete_tasks=incomplete_tasks,
        complete_tasks=complete_tasks,
        categories=categories
    )

@task_bp.route("/delete/<int:task_id>", methods=["DELETE"])
@login_required
def delete(task_id):
    """
    指定されたタスクを削除します。

    Args:
        task_id (int): 削除対象のタスクID。

    Returns:
        JSON形式のレスポンス(success=True)
    """
    task = Task.query.get(task_id)
    if task and task.user_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False}), 403

@task_bp.route("/toggle/<int:task_id>", methods=["POST"])
@login_required
def toggle(task_id):
    """
    指定されたタスクの完了状態を切り替えます。

    Args:
        task_id (int): 状態を変更するタスクID。

    Returns:
        Response:  JSON形式のレスポンス(success=True, task.completed)
    """
    task = Task.query.get(task_id)
    if task:
        task.completed = not task.completed
        db.session.commit()
        return jsonify({"success": True, "completed": task.completed})
    return jsonify({"success": False}), 404

@task_bp.route("/reward", methods=["POST"])
def show_reward():
    """
    選択されたカテゴリの中から、まだ視聴していないご褒美動画をランダムに1つ取得して表示します。
    POSTデータからカテゴリ名を取得してフィルタリングを行います。
    視聴履歴の更新を行います。

    Returns:
        str: HTMLテンプレートのレンダリング結果（reward.html）未視聴動画が無い場合はメッセージ。
    """
    user_id = current_user.id

    # そのユーザーがまだ見ていない動画IDを抽出
    seen_ids = db.session.query(WatchHistory.video_id).filter_by(user_id=user_id).subquery()
    selected_category = request.form.get("category")
    # 未視聴動画の中からランダムに取得
    video = (
        RewardVideo.query
        .filter(
            ~RewardVideo.id.in_(seen_ids),
            RewardVideo.category == selected_category
        )
        .order_by(db.func.random())
        .first()
    )
    if not video:
        return "すべての動画を視聴済みです。新しい動画を追加してください。"

    # 視聴履歴を保存
    tokyo = pytz.timezone("Asia/Tokyo")
    history = WatchHistory(
        user_id=user_id,
        video_id=video.id,
        watched_at=datetime.now(tokyo)
    )
    db.session.add(history)
    db.session.commit()

    return render_template("reward.html", video=video)

@task_bp.route("/reorder",methods=["POST"])
@login_required
def reorder():
    """
    フロントエンドから受け取ったタスクIDの順番に従って、タスクの並び順(sort_order)を更新します。

    Returns:
        Response: JSON形式の成功レスポンス（success=True）。
    """
    data=request.get_json()
    ordered_ids=data.get("ordered_ids",[])
    for i, task_id in enumerate(ordered_ids):
        task = Task.query.get(int(task_id))
        if task and task.user_id == current_user.id:
            task.sort_order = i
    db.session.commit()
    return jsonify(success=True)
