from collections import Counter
from typing import Dict, Union, List, Tuple

import numpy as np
import pandas as pd

from deepspace_helper.sm_simulator.slot_machine import SlotMachine


class Analyzer:
    def __init__(
            self,
            slot_machine: SlotMachine
    ):
        self.slot_machine = slot_machine

    @staticmethod
    def _to_dataframe(
            counter_list
    ):
        sample_df = pd.DataFrame(counter_list).fillna(0).astype(int)
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
        sm.initialize()

        n = n_coins // sm.per_cost.value

        sm(
            size=(n_samples, n)
        )
        rec = sm.record

        return self._to_dataframe(rec)

    @staticmethod
    def _equivalent_target_list(
            target: Union[Dict, List[Dict]]
    ):
        def _equivalent(
                tar
        ):
            result = [tar]
            for k, v in tar.items():
                if hasattr(k, "price"):
                    pri = k.price
                    equ_target = Counter(tar)
                    equ_target -= Counter([k])
                    equ_target[pri.__class__(1)] += pri.value

                    if equ_target in rec:
                        continue
                    rec.append(equ_target)

                    result.extend(_equivalent(equ_target))

            return result

        rec = []
        if isinstance(target, Dict):
            target = [target]

        return [
            cnt
            for t in target
            for cnt in _equivalent(Counter(t))
        ]

    def roll_by_target_naive(
            self,
            target: Union[Dict, List[Dict]],
            step: int = 10,
            n_samples: int = 1000
    ) -> pd.DataFrame:
        """
        Simulate rolling the slot machine until reaching the specified `target`.
        In a single experiment, results are accumulated every `step` spins.

        Parameters
        ----------
        target : Union[Dict, List[Dict]]
            If `target` is a dictionary, it indicates that all targets specified in the dictionary
            must be achieved simultaneously.
            The keys of the dictionary represent the items on the slot machine,
            and the values represent the desired counts for each item.
            If `target` is a list, it means that any of the targets represented by dictionaries in the list
            can be achieved.
        step : int, default: 10
            The number of spins to accumulate results before checking for the target.
        n_samples : int, default 1000
            The number of simulation samples to run.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing the results of the slot machine simulations.
        """
        sm = self.slot_machine
        sm.initialize()

        # 将所有达成目标的情景拼在一起
        options = self._equivalent_target_list(target)
        total_keys = list({k for x in options for k in x.keys()})

        # 记录达成、未达成和开销的变量
        reach = []
        not_reach = np.broadcast_to(np.array([Counter()]), shape=(n_samples,))
        cost = 0

        while n_not_reach := len(not_reach):
            sm.initialize()
            sm(
                size=(n_not_reach, step)
            )
            cost += sm.total_cost.value

            # 当前(余下的人)的抽卡记录
            rec = not_reach + np.array(sm.record)
            rec_df = pd.DataFrame(rec.tolist(), columns=total_keys).fillna(0)

            # 根据目标构建mask，True代表完成，False代表未完成
            mask = np.any([
                np.all(
                    [rec_df[k] >= v for k, v in x.items()],
                    axis=0
                )
                for x in options
            ], axis=0)

            # 记录达成目标的人
            new_reach = rec[mask]
            for x in new_reach:
                x["total_cost"] = cost
            reach.append(new_reach)

            # 更新余下的人
            not_reach = rec[~mask]

        return self._to_dataframe(np.concatenate(reach).tolist())

    def roll_by_target_iter(
            self,
            target: Union[Dict, List[Dict]],
            n_times=300,
            n_samples: int = 1000,
            percentile: float = 0.5,
            lr: Union[int, float] = 10,
            max_iter: int = 500,
            verbose=True
    ) -> pd.DataFrame:
        sm = self.slot_machine
        sm.initialize()

        # 将所有达成目标的情景拼在一起
        options = self._equivalent_target_list(target)
        total_keys = list({k for x in options for k in x.keys()})

        last_10_times = list(range(10))
        rec_df = pd.DataFrame([], columns=total_keys)
        for _ in range(max_iter):
            sm.initialize()
            sm(
                size=(n_samples, n_times)
            )
            rec_df = pd.DataFrame(sm.record, columns=total_keys).fillna(0)

            # 根据目标构建mask，True代表完成，False代表未完成
            reach = np.any([
                np.all(
                    [rec_df[k] >= v for k, v in x.items()],
                    axis=0
                )
                for x in options
            ], axis=0).sum()

            # 根据当前达成目标百分比，更新n_times
            ratio = reach / n_samples
            diff = ratio - percentile
            change = lr * diff
            n_times -= change
            n_times = round(n_times)

            if verbose:
                print(n_times, diff)

            # 使用后10次的极差来作为停止迭代条件
            if np.array(last_10_times).ptp() <= 1:
                break

            last_10_times.pop(0)
            last_10_times.append(n_times)

        return rec_df.astype(int)

    # def roll_by_target_bin(
    #         self,
    #         target: Dict,
    #         init_value: int = 10,
    #         n_samples: int = 1000
    # ) -> pd.DataFrame:
    #     """
    #     Simulate rolling the slot machine until reaching the specified `target`.
    #     In a single experiment, binary search is used. It returns the value k when
    #     the `target` is satisfied in the kth trial but not in the (k-1)th trial.
    #
    #     Parameters
    #     ----------
    #     target : Dict
    #         A dictionary representing the target configuration to achieve. The keys
    #         are the items on the slot machine, and the values are the desired counts
    #         for each item.
    #     init_value : int, default: 10
    #         The initial value for binary search.
    #     n_samples : int, default 1000
    #         The number of simulation samples to run.
    #
    #     Returns
    #     -------
    #     pd.DataFrame
    #         A DataFrame containing the results of the slot machine simulations.
    #     """
    #
    #     def _roll(
    #             machine,
    #             target_list,
    #             init
    #     ):
    #         latest_rec = machine.record
    #         lower = 0
    #         upper = math.inf
    #         cur_times = init
    #         for _ in range(100):
    #             machine.initialize()
    #             machine(cur_times)
    #
    #             is_get = False
    #             rec = machine.record
    #             rec["total_cost"] = machine.total_cost.value
    #             for t in target_list:
    #                 if not (t - rec):
    #                     is_get = True
    #                     break
    #
    #             if is_get:
    #                 upper = cur_times
    #                 latest_rec = rec
    #             else:
    #                 lower = cur_times
    #
    #             if upper != math.inf:
    #                 cur_times = round((lower + upper) / 2)
    #             else:
    #                 cur_times = 2 * lower
    #
    #             if upper - lower == 1:
    #                 return latest_rec
    #
    #     sm = self.slot_machine
    #     options = self._equivalent_target_list(target)
    #
    #     return self._multi_experiment(
    #         n_repeat=n_samples,
    #         func=_roll
    #     )(
    #         machine=sm,
    #         target_list=options,
    #         init=init_value
    #     )
