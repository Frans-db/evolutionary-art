from dataclasses import dataclass, field
from functools import reduce


@dataclass
class Element:
    tag: str
    classes: list[str] = field(default_factory=list)
    children: list["Element"] = field(default_factory=list)

    @property
    def size(self) -> int:
        return 1 + sum([child.size for child in self.children])

    def to_html(self) -> str:
        classes = " ".join(self.classes)
        children = "\n".join([child.to_html() for child in self.children])
        return f'<{self.tag} class="{classes}">{children}</{self.tag}>'

    def flatten(self) -> list["Element"]:
        l = [self]
        for child in self.children:
            l.extend(child.flatten())
        return l

    def remove(self, element: "Element") -> bool:
        for child in self.children:
            if child is element:
                self.children.remove(child)
                break
            child.remove(element)
