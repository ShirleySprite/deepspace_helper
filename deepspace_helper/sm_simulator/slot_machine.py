from collections import Counter
from typing import Dict

import numpy as np


class SlotMachine:
    def __init__(
            self,
            chance_table: Dict
    ):
        self.chance_table = chance_table
        self._items = tuple(self.chance_table.keys())
        self._weights = tuple(self.chance_table.values())
        self.rng = np.random.default_rng()
        self.record = Counter()

    def __call__(
            self,
            times: int = 1
    ):
        result = self.rng.choice(
            self._items,
            size=times,
            p=self._weights
        )

        self.record += Counter(result)
