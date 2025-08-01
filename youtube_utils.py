"""
YouTube DATA APIを用いて検索を行うモジュール。
"""
import os

from googleapiclient.discovery import build


YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")

def search_youtube(keyword, max_results=50):
    """
    YouTube Data APIを用いて動画を検索する関数。

    Args:
        keyword (str): 検索キーワード。
        max_results (int): 一回の検索で取得する動画数。最大値は50。
    Returns:
        list of dict: 取得した動画情報のリスト。各辞書はidとタイトルを含む。
    """
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    response = youtube.search().list(  # pylint: disable=no-member
        q=keyword,
        part="snippet",
        type="video",
        videoDuration="short",
        maxResults=max_results
    ).execute()

    videos = []
    for item in response.get("items", []):
        videos.append({
            "id": item["id"]["videoId"],
            "title": item["snippet"]["title"]
        })
    return videos
