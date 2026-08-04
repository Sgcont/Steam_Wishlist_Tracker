from dataclasses import dataclass
from datetime import datetime


@dataclass
class WishlistGame:
    appid: int
    name: str
    price_current: float
    price_original: float
    discount_percent: int
    last_updated: datetime
