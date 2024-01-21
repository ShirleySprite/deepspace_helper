import os
import json
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Union, List, Dict

from deepspace_helper.utils.coin import Coin, coin_map


@dataclass
class Clothing:
    position: str
    name: str
    price: Optional[Coin] = None

    def __str__(self):
        return f"{self.position}·{self.name}"

    def __hash__(self):
        return hash(str(self))


def clothing_parser(
        clothing: Union[List, Dict]
):
    if isinstance(clothing, Dict):
        clothing = [clothing]

    result = []
    for c in clothing:
        if "price" in c:
            p = c["price"]
            price = coin_map[p["name"]](p["count"])
            c["price"] = price
        result.append(Clothing(**c))

    return result


_clothing_root = Path(f"{os.path.dirname(__file__)}/game_data/clothing")
all_clothing = {
    clo_file.stem: clothing_parser(
        json.loads(clo_file.read_text(encoding="utf-8"))
    )
    for clo_file in _clothing_root.rglob("*.json")
}
