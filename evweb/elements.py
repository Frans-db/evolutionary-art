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

    def remove(self, target: "Element") -> bool:
        for child in self.children:
            if child is target:
                self.children.remove(child)
                return True
            if child.remove(target):
                return True

        return False

    def replace(self, target: "Element", element: "Element") -> bool:
        try:
            index = self.children.index(target)
            self.children[index] = element
            return True
        except ValueError:
            for child in self.children:
                if child.replace(target, element):
                    return True
        return False
                