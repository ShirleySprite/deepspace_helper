from collections import Counter
from typing import Dict, Union, Tuple, List

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
        self._raw_record = np.array([Counter()])

    @property
    def total_cost(
            self
    ):
        return self.per_cost * self.cnt

    @property
    def record(
            self
    ) -> List:
        # coin应该合并, 其余保持不变
        result = []
        for cnt in self._raw_record:
            single_result = Counter()
            for k, v in cnt.items():
                if isinstance(k, Coin):
                    single_result[k.__class__(1)] += k.value * v
                else:
                    single_result[k] = v
            result.append(single_result)

        return result

    def __repr__(
            self
    ):
        return f"{self.__class__.__name__}(chance_table={self.chance_table})"

    def __call__(
            self,
            size: Union[int, Tuple[int, int]] = 1
    ):
        if isinstance(size, int):
            size = (1, size)

        result = self.rng.choice(
            self._items,
            size=size,
            p=self._weights
        )
        result_cnt = np.array([Counter(x) for x in result])

        self.cnt += size[1]
        self._raw_record = self._raw_record + result_cnt

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
        self._raw_record = np.array([Counter()])


class StarCompass(SlotMachine):
    name = "星谕罗盘"

    @property
    def record(
            self
    ) -> List:
        temp_result = super().record
        new_result = []
        for single_result in temp_result:
            new_single = Counter()
            for k, v in single_result.items():
                # 衣服会转化为代币
                if isinstance(k, Clothing):
                    overflow = v - 1
                    new_single[k] = 1
                    new_single[StarDice(1)] += overflow * 80

                # 卡满破也会转化为代币
                elif isinstance(k, Card):
                    overflow = max(0, v - 4)
                    new_single[k] = min(v, 4)
                    new_single[StarDice(1)] += overflow * 704
                else:
                    new_single[k] += v
            new_result.append(new_single)

        # 达到一定次数给蚊子腿
        ...

        return new_result
