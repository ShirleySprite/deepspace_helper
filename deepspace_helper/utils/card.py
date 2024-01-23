import os
import json
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Union, List, Dict

from deepspace_helper.utils.coin import Coin, coin_map


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

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return str(self) == str(other)


def card_parser(
        cards: Union[List, Dict]
) -> List[Card]:
    """
    Instantiate a `Card` object from either a `List` or `Dict`.

    Parameters
    ----------
    cards: Union[List, Dict]
        Raw data of the card in either `List` or `Dict` format.

    Returns
    -------
    List[Card]
        A list containing the instantiated `Card` objects.
    """
    if isinstance(cards, Dict):
        cards = [cards]

    result = []
    for c in cards:
        if "price" in c:
            p = c["price"]
            price = coin_map[p["name"]](p["value"])
            c["price"] = price
        result.append(Card(**c))

    return result


# 自动从卡牌文件夹里加载所有卡牌
_card_root = Path(f"{os.path.dirname(__file__)}/game_data/card")
all_cards = {
    clo_file.stem: card_parser(
        json.loads(clo_file.read_text(encoding="utf-8"))
    )
    for clo_file in _card_root.rglob("*.json")
}
