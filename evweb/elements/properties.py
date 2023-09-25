from dataclasses import dataclass
from abc import ABC, NotImplementedError
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

    def mutate(self, max_nudge: float) -> None:
        self.value = self.nudge(self.value, self.max_value)
        self.value = self.clamp(self.value, self.min_value, self.max_value)


# display, flex-direction
@dataclass
class DiscreteProperty(Property):
    values: list[str]
    value: str = None

    def __post_init__(self) -> None:
        self.value = random.choice(self.values)

    def to_css(self) -> str:
        return f"{self.name}: {self.value}"

    def mutate(self, switch_chance: float) -> None:
        if random.random() > switch_chance:
            return
        self.value = random.choice(self.values)


# color, background-color
@dataclass
class RGBProperty(Property):
    r: float = None
    g: float = None
    b: float = None

    def __post_init__(self) -> None:
        self.r = random.random() * 255
        self.g = random.random() * 255
        self.b = random.random() * 255

    def to_css(self) -> str:
        return f"{self.name}: rgb({self.r}, {self.g}, {self.b})"

    def mutate(self, max_nudge: float) -> None:
        self.r = self.nudge(self.r, max_nudge)
        self.r = self.clamp(self.r, 0, 255)
        self.g = self.nudge(self.g, max_nudge)
        self.g = self.clamp(self.g, 0, 255)
        self.b = self.nudge(self.b, max_nudge)
        self.b = self.clamp(self.b, 0, 255)
