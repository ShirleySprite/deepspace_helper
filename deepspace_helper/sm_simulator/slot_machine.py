from collections import Counter
from typing import Dict

import numpy as np

from deepspace_helper.utils.coin import Coin


class SlotMachine:
    def __init__(
            self,
            per_cost: Coin,
            chance_table: Dict
    ):
        self.per_cost = per_cost
        self.chance_table = chance_table
        self._items = tuple(self.chance_table.keys())
        self._weights = tuple(self.chance_table.values())
        self.rng = np.random.default_rng()
        self.record = Counter()
        self.total_cost = 0

    def __repr__(self):
        return f"{self.__class__.__name__}(chance_table={self.chance_table})"

    def __call__(
            self,
            times: int = 1
    ):
        result = self.rng.choice(
            self._items,
            size=times,
            p=self._weights
        )

        self.total_cost = self.per_cost * times + self.total_cost
        self.record += Counter(result)
