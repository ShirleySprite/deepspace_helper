from collections import Counter
from typing import Dict

import numpy as np

from deepspace_helper.utils.coin import Coin, StarDice
from deepspace_helper.utils.clothing import Clothing
from deepspace_helper.utils.card import Card


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

    @property
    def record(
            self
    ):
        # coin应该合并, 其余保持不变
        result = Counter()
        for k, v in self._raw_record.items():
            if isinstance(k, Coin):
                result[k.__class__(1)] += k.value * v
            else:
                result[k] = v

        return result

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

        self.cnt += times
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


class StarCompass(SlotMachine):
    name = "星谕罗盘"

    @property
    def record(
            self
    ):
        temp_result = super().record

        result = Counter()
        for k, v in temp_result.items():
            # 衣服会转化为代币
            if isinstance(k, Clothing):
                overflow = v - 1
                result[k] = 1
                result[StarDice(1)] += overflow * 80

            # 卡满破也会转化为代币
            elif isinstance(k, Card):
                overflow = max(0, v - 4)
                result[k] = min(v, 4)
                result[StarDice(1)] += overflow * 704

            else:
                result[k] += v

        # 达到一定次数给蚊子腿
        ...

        return result
