from collections import Counter
from typing import Any, Dict

import pandas as pd

from deepspace_helper.sm_simulator.slot_machine import SlotMachine


class Analyzer:
    def __init__(
            self,
            slot_machine: SlotMachine
    ):
        self.slot_machine = slot_machine

    @staticmethod
    def sample_df(
            sample_list
    ):
        sample_df = pd.DataFrame(sample_list).fillna(0).astype(int)
        cols = sorted(sample_df.columns, key=lambda x: str(x))

        return sample_df.reindex(columns=cols)

    def roll_by_coins(
            self,
            n_coins: int,
            n_samples: int = 1000
    ) -> pd.DataFrame:
        """
        Simulate rolling the slot machine using a specified number of coins.

        Parameters
        ----------
        n_coins : int
            The total number of coins to be used for rolling the slot machine.
        n_samples : int, default 1000
            The number of simulation samples to run.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing the results of the slot machine simulations.
        """
        sm = self.slot_machine
        times = n_coins // sm.per_cost.value
        exp_result = []
        for _ in range(n_samples):
            sm(
                times=times
            )
            exp_result.append(sm.record)
            sm.initialize()

        sample_df = self.sample_df(exp_result)
        sample_df["total_cost"] = sm.per_cost.value * times

        return sample_df
    #
    # @staticmethod
    # def is_get(
    #         target_item: Any,
    #         target_cnt: int,
    #         record: Counter
    # ):
    #     left = target_cnt - record[target_item]
    #     if left <= 0:
    #         return True
    #
    #     if hasattr(target_item, "price"):
    #         pri = target_item.price
    #         coins = record[pri.__class__(1)]
    #         coins_left = coins - pri.value * target_cnt
    #         if coins_left >= 0:
    #             return True
    #
    #     return False
    #
    # def roll_by_target(
    #         self,
    #         target: Dict,
    #         step: int = 10,
    #         n_samples: int = 1000
    # ) -> pd.DataFrame:
    #     target = Counter(target)
    #
    #     is_get = False
    #     sm = self.slot_machine
    #     while not is_get:
    #         sm(
    #             times=step
    #         )
    #         rec = sm.record
    #
    #         for k, v in target.items():
    #             if
