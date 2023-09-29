from dataclasses import dataclass, field
from abc import ABC
import random


@dataclass
class Property(ABC):
    name: str

    def mutate(self) -> None:
        raise NotImplementedError

    @staticmethod
    def nudge(value: float, max_nudge: float) -> float:
        nudge = (random.random() - 0.5) * max_nudge
        value += value * nudge
        return value

    @staticmethod
    def clamp(value: float, min_value: float, max_value: float) -> float:
        return max(min(value, max_value), min_value)


# padding, marging, width, height
@dataclass
class RealProperty(Property):
    min_value: float
    max_value: float
    unit: str
    value: float = None

    def __post_init__(self) -> None:
        delta = self.max_value - self.min_value
        self.value = self.min_value + random.random() * delta

    def to_css(self) -> str:
        return f"{self.name}: {self.value}{self.unit}"

    def mutate(self, max_nudge: float = 0.1) -> None:
        self.value = self.nudge(self.value, max_nudge)
        self.value = self.clamp(self.value, self.min_value, self.max_value)

    def __str__(self) -> str:
        return self.to_css()


# display, flex-direction
@dataclass
class DiscreteProperty(Property):
    values: list[str]
    value: str = None

    def __post_init__(self) -> None:
        self.value = random.choice(self.values)

    def to_css(self) -> str:
        return f"{self.name}: {self.value}"

    def mutate(self, switch_chance: float = 0.1) -> None:
        if random.random() > switch_chance:
            return
        self.value = random.choice(self.values)

    def __str__(self) -> str:
        return self.to_css()


# color, background-color
@dataclass
class RGBProperty(Property):
    r: RealProperty = None
    g: RealProperty = None
    b: RealProperty = None

    def __post_init__(self) -> None:
        self.r = RealProperty("red", 0, 255, "")
        self.g = RealProperty("green", 0, 255, "")
        self.b = RealProperty("blue", 0, 255, "")

    def to_css(self) -> str:
        r = round(self.r.value)
        g = round(self.g.value)
        b = round(self.b.value)
        return f"{self.name}: rgb({r}, {g}, {b})"

    def mutate(self, max_nudge: float = 0.1) -> None:
        self.r.mutate(max_nudge=max_nudge)
        self.g.mutate(max_nudge=max_nudge)
        self.b.mutate(max_nudge=max_nudge)

    def __str__(self) -> str:
        return self.to_css()


@dataclass
class StaticProperty(Property):
    value: str

    def to_css(self) -> str:
        return f"{self.name}: {self.value}"

    def mutate(self) -> None:
        pass

    def __str__(self) -> str:
        return self.to_css()