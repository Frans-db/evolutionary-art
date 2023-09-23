from dataclasses import dataclass, field


@dataclass
class Element:
    tag: str
    classes: list[str] = field(default_factory=list)
    children: list["Element"] = field(default_factory=list)

    def to_html(self) -> str:
        classes = " ".join(self.classes)
        children = '\n'.join([child.to_html() for child in self.children])
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