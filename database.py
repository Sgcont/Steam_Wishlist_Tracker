import sqlite3
from datetime import datetime
from typing import List

from models import WishlistGame


class Database:
    def __init__(self, db_path: str = "database.db") -> None:
        self.db_path = db_path
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS wishlist_games (
                    appid INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    price_current REAL NOT NULL,
                    price_original REAL NOT NULL,
                    discount_percent INTEGER NOT NULL,
                    last_updated TEXT NOT NULL
                )
                """
            )

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tracked_appids (
                    appid INTEGER PRIMARY KEY,
                    created_at TEXT NOT NULL
                )
                """
            )

    def save_tracked_appids(self, appids: List[int]) -> None:
        now = datetime.now().isoformat()

        with self._connect() as conn:
            conn.execute("DELETE FROM tracked_appids")
            conn.executemany(
                "INSERT INTO tracked_appids (appid, created_at) VALUES (?, ?)",
                [(appid, now) for appid in appids],
            )

    def get_tracked_appids(self) -> List[int]:
        with self._connect() as conn:
            cursor = conn.execute(
                "SELECT appid FROM tracked_appids ORDER BY appid"
            )
            return [row[0] for row in cursor.fetchall()]

    def upsert_games(self, games: List[WishlistGame]) -> None:
        with self._connect() as conn:
            conn.executemany(
                """
                INSERT INTO wishlist_games (appid, name, price_current, price_original, discount_percent, last_updated)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(appid) DO UPDATE SET
                    name = excluded.name,
                    price_current = excluded.price_current,
                    price_original = excluded.price_original,
                    discount_percent = excluded.discount_percent,
                    last_updated = excluded.last_updated
                """,
                [
                    (
                        game.appid,
                        game.name,
                        game.price_current,
                        game.price_original,
                        game.discount_percent,
                        game.last_updated.isoformat(),
                    )
                    for game in games
                ],
            )

    def get_discounted_games(self) -> List[WishlistGame]:
        with self._connect() as conn:
            cursor = conn.execute(
                """
                SELECT appid, name, price_current, price_original, discount_percent, last_updated
                FROM wishlist_games
                WHERE discount_percent > 0
                ORDER BY discount_percent DESC, name ASC
                """
            )

            rows = cursor.fetchall()

        return [
            WishlistGame(
                appid=row[0],
                name=row[1],
                price_current=row[2],
                price_original=row[3],
                discount_percent=row[4],
                last_updated=datetime.fromisoformat(row[5]),
            )
            for row in rows
        ]
