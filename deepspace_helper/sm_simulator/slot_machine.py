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
        # 单次花费
        self.per_cost = per_cost

        # 概率表
        self.chance_table = chance_table
        self._items = tuple(self.chance_table.keys())
        self._weights = tuple(self.chance_table.values())

        # 随机生成器
        self.rng = np.random.default_rng()

        # 记录次数和获得物品
        self.cnt = 0
        self._raw_record = Counter()

    @property
    def total_cost(
            self
    ):
        return self.per_cost * self.cnt

    def __repr__(
            self
    ):
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

        self.cnt += 1
        self._raw_record += Counter(result)

    def initialize(
            self
    ) -> None:
        """
        Initialize this machine.

        Returns
        -------
        None
        """
        self.cnt = 0
        self._raw_record = Counter()
