from dataclasses import dataclass, field
import random


@dataclass
class Element:
    tag: str
    properties: list["Property"] = field(default_factory=list)
    children: list["Element"] = field(default_factory=list)

    def to_html(self) -> str:
        style = '; '.join([prop.to_css() for prop in self.properties])
        children = '\n'.join([child.to_html() for child in self.children])
        return f'<{self.tag} style="{style}">{children}</{self.tag}>'

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

    def __post_init__(self):
        delta = self.max_value - self.min_value
        self.value = self.min_value + random.random() * delta

    def to_css(self) -> str:
        return f"{self.name}: {self.value}{self.unit}"


# flex, flex-direction
@dataclass
class DiscreteProperty(Property):
    values: list[str]
    value: str = None

    def __post_init__(self):
        self.value = random.choice(self.values)

    def to_css(self) -> str:
        return f"{self.name}: {self.value}"


# color, background-color
@dataclass
class RGBProperty(Property):
    r: float = None
    g: float = None
    b: float = None

    def __post_init__(self):
        self.r = random.random() * 255
        self.g = random.random() * 255
        self.b = random.random() * 255

    def to_css(self) -> str:
        return f"{self.name}: rgb({self.r}, {self.g}, {self.b})"