import time
from datetime import datetime
from typing import List, Optional

import requests

from models import WishlistGame


class SteamAPI:
    BASE_URL = "https://store.steampowered.com/api/appdetails"

    def fetch_game_details(self, appid: int) -> Optional[WishlistGame]:
        try:
            response = requests.get(
                self.BASE_URL,
                params={"appids": appid, "cc": "br", "l": "portuguese"},
                timeout=15,
            )
            response.raise_for_status()
            data = response.json()

            app_data = data.get(str(appid), {})
            if not app_data.get("success"):
                return None

            details = app_data.get("data", {})
            name = details.get("name")
            price_overview = details.get("price_overview")

            if not name or not price_overview:
                return None

            current = price_overview.get("final", 0) / 100
            original = price_overview.get("initial", 0) / 100
            discount = price_overview.get("discount_percent", 0)

            return WishlistGame(
                appid=appid,
                name=name,
                price_current=float(current),
                price_original=float(original),
                discount_percent=int(discount),
                last_updated=datetime.now(),
            )
        except requests.RequestException:
            return None

    def update_wishlist_games(self, appids: List[int]) -> List[WishlistGame]:
        games: List[WishlistGame] = []

        for appid in appids:
            game = self.fetch_game_details(appid)
            if game:
                games.append(game)
            time.sleep(1.0)

        return games
