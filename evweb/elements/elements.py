from dataclasses import dataclass, field
from html2image import Html2Image
import os

from .properties import Property, RealProperty, DiscreteProperty, RGBProperty


@dataclass
class Element:
    tag: str
    children: list["Element"] = field(default_factory=list)
    properties: list[Property] = field(default_factory=list)
    contents: str = ""
    # Fitness is only used on the root element.
    # Another way to do this would be to create an Individual object
    # which stores an element and its fitness. This would be the only
    # purpose for the individual though, so I prefer this.
    fitness: int = -1

    def __post_init__(self) -> None:
        displays = ["block", "inline", "flex"]
        flex_directions = ["row", "row-reverse", "column", "column-reverse"]
        properties = [
            RealProperty(name="width", min_value=0, max_value=100, unit="rem"),
            RealProperty(name="height", min_value=0, max_value=100, unit="rem"),
            RealProperty(name="padding", min_value=0, max_value=100, unit="rem"),
            RealProperty(name="margin", min_value=0, max_value=100, unit="rem"),
            RGBProperty(name="background-color"),
            DiscreteProperty("display", values=displays),
            DiscreteProperty("flex-direction", values=flex_directions),
        ]
        self.properties.extend(properties)

    def to_html(self) -> str:
        style = "; ".join([prop.to_css() for prop in self.properties])
        children_html = [child.to_html() for child in self.children]
        inner = "\n".join([self.contents] + children_html)
        return f'<{self.tag} style="{style}">{inner}</{self.tag}>'

    def render(self, directory: str, filename: str) -> None:
        html = self.to_html()
        renderer = Html2Image(output_path=directory)
        renderer.screenshot(html=html, save_as=f"{filename}.png")
        with open(os.path.join(directory, f"{filename}.html"), "w+") as f:
            f.write(html)


def get_default_element() -> Element:
    root = Element("div")
    for _ in range(5):
        child = Element("div")
        child.children.append(Element("div"))
        root.children.append(child)

    return root
