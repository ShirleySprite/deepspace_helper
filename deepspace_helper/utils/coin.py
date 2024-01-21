from abc import ABC


class Coin(ABC):
    name = "抽象Coin"

    def __init__(
            self,
            count: int = 1
    ):
        self.count = count

    def __repr__(self):
        return f"{self.__class__.__name__}(count={self.count})"

    def __str__(self):
        return f"{self.name}*{self.count}"

    def __add__(self, coin):
        if not isinstance(coin, self.__class__):
            raise TypeError(
                f"unsupported operand type(s) for +: '{self.__class__.__name__}' and '{coin.__class__.__name__}'"
            )

        return self.__class__(
            count=self.count + coin.count
        )


class StarDice(Coin):
    store_name = "神秘屋"
    name = "星谕骰"
    activity_name = "星谕罗盘"

    def __init__(
            self,
            count: int = 1
    ):
        super().__init__(
            count=count
        )
