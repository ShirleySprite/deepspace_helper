import math
from collections import Counter
from typing import Dict

import pandas as pd

from deepspace_helper.sm_simulator.slot_machine import SlotMachine


class Analyzer:
    def __init__(
            self,
            slot_machine: SlotMachine
    ):
        self.slot_machine = slot_machine

    @staticmethod
    def _multi_experiment(n_repeat, func):
        def wrapper(*args, **kwargs):
            exp_result = []
            for _ in range(n_repeat):
                exp_result.append(func(*args, **kwargs))

            sample_df = pd.DataFrame(exp_result).fillna(0).astype(int)
            cols = sorted(sample_df.columns, key=lambda x: str(x))

            return sample_df.reindex(columns=cols)

        return wrapper

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

        def _roll(
                machine,
                n
        ):
            machine.initialize()
            machine(
                times=n
            )
            rec = machine.record
            rec["total_cost"] = machine.total_cost.value
            return rec

        sm = self.slot_machine

        return self._multi_experiment(
            n_repeat=n_samples,
            func=_roll
        )(
            machine=sm,
            n=n_coins // sm.per_cost.value
        )

    @staticmethod
    def _equivalent_target_list(
            target: Dict
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

        return _equivalent(Counter(target))

    def roll_by_target_naive(
            self,
            target: Dict,
            step: int = 10,
            n_samples: int = 1000
    ) -> pd.DataFrame:
        """
        Simulate rolling the slot machine until reaching the specified `target`.
        In a single experiment, results are accumulated every `step` spins.

        Parameters
        ----------
        target : Dict
            A dictionary representing the target configuration to achieve. The keys
            are the items on the slot machine, and the values are the desired counts
            for each item.
        step : int, default: 10
            The number of spins to accumulate results before checking for the target.
        n_samples : int, default 1000
            The number of simulation samples to run.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing the results of the slot machine simulations.
        """

        def _roll(
                machine,
                target_list,
                n
        ):
            machine.initialize()
            for _ in range(10000):
                machine(n)
                rec = machine.record
                for t in target_list:
                    if not (t - rec):
                        rec["total_cost"] = machine.total_cost.value
                        return rec

        sm = self.slot_machine
        options = self._equivalent_target_list(target)

        return self._multi_experiment(
            n_repeat=n_samples,
            func=_roll
        )(
            machine=sm,
            target_list=options,
            n=step
        )

    def roll_by_target_bin(
            self,
            target: Dict,
            init_value: int = 10,
            n_samples: int = 1000
    ) -> pd.DataFrame:
        """
        Simulate rolling the slot machine until reaching the specified `target`.
        In a single experiment, binary search is used. It returns the value k when
        the `target` is satisfied in the kth trial but not in the (k-1)th trial.

        Parameters
        ----------
        target : Dict
            A dictionary representing the target configuration to achieve. The keys
            are the items on the slot machine, and the values are the desired counts
            for each item.
        init_value : int, default: 10
            The initial value for binary search.
        n_samples : int, default 1000
            The number of simulation samples to run.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing the results of the slot machine simulations.
        """

        def _roll(
                machine,
                target_list,
                init
        ):
            latest_rec = machine.record
            lower = 0
            upper = math.inf
            cur_times = init
            for _ in range(100):
                machine.initialize()
                machine(cur_times)

                is_get = False
                rec = machine.record
                rec["total_cost"] = machine.total_cost.value
                for t in target_list:
                    if not (t - rec):
                        is_get = True
                        break

                if is_get:
                    upper = cur_times
                    latest_rec = rec
                else:
                    lower = cur_times

                if upper != math.inf:
                    cur_times = round((lower + upper) / 2)
                else:
                    cur_times = 2 * lower

                if upper - lower == 1:
                    return latest_rec

        sm = self.slot_machine
        options = self._equivalent_target_list(target)

        return self._multi_experiment(
            n_repeat=n_samples,
            func=_roll
        )(
            machine=sm,
            target_list=options,
            init=init_value
        )
