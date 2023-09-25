from dataclasses import dataclass, field

from .properties import Property, RealProperty, DiscreteProperty, RGBProperty


@dataclass
class Element:
    tag: str
    properties: list[Property] = None
    children: list["Element"] = field(default_factory=list)

    def __post_init__(self) -> None:
        displays = ["block", "inline", "flex"]
        flex_directions = ["row", "row-reverse", "column", "column-reverse"]
        self.properties = [
            RealProperty(name="width", min_value=0, max_value=100, unit="rem"),
            RealProperty(name="height", min_value=0, max_value=100, unit="rem"),
            RealProperty(name="padding", min_value=0, max_value=100, unit="rem"),
            RealProperty(name="margin", min_value=0, max_value=100, unit="rem"),
            RGBProperty(name="background-color"),
            DiscreteProperty("display", values=displays),
            DiscreteProperty("flex-direction", values=flex_directions),
        ]

    def to_html(self) -> str:
        style = "; ".join([prop.to_css() for prop in self.properties])
        children = "\n".join([child.to_html() for child in self.children])
        return f'<{self.tag} style="{style}">{children}</{self.tag}>'
