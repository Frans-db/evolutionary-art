from dataclasses import dataclass
import random


@dataclass
class Property:
    name: str


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


# display, flex-direction
@dataclass
class DiscreteProperty(Property):
    values: list[str]
    value: str = None

    def __post_init__(self) -> None:
        self.value = random.choice(self.values)

    def to_css(self) -> str:
        return f"{self.name}: {self.value}"


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
