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

    def __hash__(self):
        return hash(f"{self.name}{self.value}")

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.value == other.value

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

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        if isinstance(other, int):
            return self.__class__(
                value=self.value * other
            )
        raise TypeError(
            f"unsupported operand type(s) for +: '{self.__class__.__name__}' and '{other.__class__.__name__}'"
        )

    def __rmul__(self, other):
        return self.__mul__(other)

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(
                f"'>' not supported between instances of '{self.__class__.__name__}' and '{other.__class__.__name__}'"
            )

        return self.value < other.value

    def __gt__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(
                f"'>' not supported between instances of '{self.__class__.__name__}' and '{other.__class__.__name__}'"
            )

        return self.value > other.value


class CrystalDiamond(Coin):
    name = "晶钻"

    def evaluate_by_diamond(
            self
    ):
        return CrystalDiamond(
            value=round(self.value * 2.25)
        )


class Diamond(Coin):
    name = "钻石"

    def evaluate_by_crystal_diamond(
            self
    ):
        return CrystalDiamond(
            value=round(self.value / 2.25)
        )


class StarDice(Coin):
    store_name = "神秘屋"
    name = "星谕骰"
    activity_name = "星谕罗盘"


coin_map = {
    "StarDice": StarDice
}
