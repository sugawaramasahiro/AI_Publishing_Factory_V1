"""出版チェックリスト  v0.1"""
from __future__ import annotations
from typing import List, Dict
from tinydb import TinyDB, Query
import pathlib

DB_PATH = pathlib.Path(".data/checklist.json")
DB_PATH.parent.mkdir(exist_ok=True)
db = TinyDB(DB_PATH)

DEFAULT_ITEMS = [
    "①前準課題（事前にやっておく）",
    "②出版予定日を決める",
    "③コンセプトを決める",
    "④本の構成を考える",
    "⑤目次を考える",
    "⑥章立てに沿って本文を書く",
    "⑦後書きを書く",
    "⑧著者プロフィールを書く",
    "⑨参考文献一覧を付ける",
    "⑩奥付を付ける",
    "⑪はじめに（前付け）を書く",
    "⑫本文＆スタイルをリライト",
    "⑬目次を最終調整する",
    "⑭表紙を作成する",
    "⑮Kindle プレビューアーで原稿確認"
]

def init_checklist() -> None:
    """初期化（1 回だけ呼ぶ）"""
    if len(db) == 0:
        db.insert_multiple({"title": t, "done": False} for t in DEFAULT_ITEMS)

def get_items() -> List[Dict]:
    return db.all()

def set_done(title: str, value: bool) -> None:
    db.update({"done": value}, Query().title == title)
