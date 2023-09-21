from dataclasses import dataclass, field


@dataclass
class Element:
    tag: str
    classes: list[str] = field(default_factory=list)
    children: list["Element"] = field(default_factory=list)

    def to_html(self) -> str:
        classes = " ".join(self.classes)
        children = "\n".join(map(lambda x: x.to_html(), self.children))
        return f'<{self.tag} class="{classes}">{children}</{self.tag}>'
