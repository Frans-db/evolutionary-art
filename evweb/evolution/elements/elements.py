from dataclasses import dataclass, field
from html2image import Html2Image
import os

from .properties import Property, RealProperty, DiscreteProperty, RGBProperty, StaticProperty


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
        # Currently using default properties. This could be changed to use a config
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

    def render(self, directory: str, filename: str) -> str:
        html = self.to_html()
        image_filename = f"{filename}.png"
        # Html2Image creates the output directory here including parent directories
        renderer = Html2Image(output_path=directory)
        renderer.screenshot(html_str=html, save_as=image_filename)
        with open(os.path.join(directory, f"{filename}.html"), "w+") as f:
            f.write(html)

        return os.path.join(directory, image_filename)

    # tree operations

    def flatten(self) -> list["Element"]:
        flat = [self]
        for child in self.children:
            flat.extend(child.flatten())
        return flat

    def remove(self, target: "Element") -> bool:
        for child in self.children:
            # Child is target. Remove from list and return
            if child is target:
                self.children.remove(child)
                return True
            # Child contained target one if its (grand)children.
            elif child.remove(target):
                return True
        # Target was not found
        return False

    def replace(self, target: "Element", element: "Element") -> bool:
        try:
            # Target is in children
            index = self.children.index(target)
            # Replace child with target
            self.children[index] = target
            return True
        except ValueError:
            # Target is not in children, search for it in children's children
            for child in self.children:
                if child.replace(target, element):
                    return True
        # Target was not found
        return False


def get_default_element() -> Element:
    root = Element("body")
    root.properties = [StaticProperty('background-color', 'rgb(255, 255, 255)')]
    for _ in range(5):
        child = Element("div")
        child.children.append(Element("div"))
        root.children.append(child)

    return root
