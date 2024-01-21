from dataclasses import dataclass
from typing import Optional

from deepspace_helper.sm_simulator.coin import Coin, StarDice


@dataclass
class Clothing:
    position: str
    name: str
    price: Optional[Coin] = None

    def __str__(self):
        return f"{self.position}·{self.name}"

    def __hash__(self):
        return hash(str(self))


# 一月星谕罗盘
sd_100 = StarDice(100)

duck_clo = Clothing(
    position="头饰",
    name="童趣小鸭",
    price=sd_100
)
bamboo_clo = Clothing(
    position="头饰",
    name="竹蜻蜓",
    price=sd_100
)
horn_clo = Clothing(
    position="头饰",
    name="黄金尖角",
    price=sd_100
)
