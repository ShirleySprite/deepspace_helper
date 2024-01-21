from abc import ABC


class Coin(ABC):
    name = "抽象Coin"

    def __init__(
            self,
            value: int = 1
    ):
        self.value = value

    def __repr__(self):
        return f"{self.__class__.__name__}(value={self.value})"

    def __str__(self):
        return f"{self.name}*{self.value}"

    def __add__(self, other):
        if isinstance(other, int):
            return self.__class__(
                value=self.value + other
            )

        if not isinstance(other, self.__class__):
            raise TypeError(
                f"unsupported operand type(s) for +: '{self.__class__.__name__}' and '{other.__class__.__name__}'"
            )

        return self.__class__(
            value=self.value + other.value
        )

    def __mul__(self, other):
        if isinstance(other, int):
            return self.__class__(
                value=self.value * other
            )
        raise TypeError(
            f"unsupported operand type(s) for +: '{self.__class__.__name__}' and '{other.__class__.__name__}'"
        )


class CrystalDiamond(Coin):
    name = "晶钻"


class Diamond(Coin):
    name = "钻石"


class StarDice(Coin):
    store_name = "神秘屋"
    name = "星谕骰"
    activity_name = "星谕罗盘"


coin_map = {
    "StarDice": StarDice
}
