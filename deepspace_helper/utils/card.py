from dataclasses import dataclass
from typing import Optional

from deepspace_helper.utils.coin import Coin, StarDice


@dataclass
class Card:
    rarity: int
    character: str
    name: str
    price: Optional[Coin] = None

    def __str__(self):
        return f"{self.character}·{self.name}"

    def __hash__(self):
        return hash(str(self))


# 一月星谕罗盘
sd_880 = StarDice(880)

sxh_shower_card = Card(
    rarity=4,
    character="沈星回",
    name="漉漉温言",
    price=sd_880
)
ls_shower_card = Card(
    rarity=4,
    character="黎深",
    name="余冽",
    price=sd_880
)
qy_shower_card = Card(
    rarity=4,
    character="祁煜",
    name="潮夜陷落",
    price=sd_880
)
