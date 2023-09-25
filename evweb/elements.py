from dataclasses import dataclass, field
from functools import reduce
from html2image import Html2Image
import os

input_html ='''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Evolutionary Webdesign</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-white">
    INNER
</body>
</html>'''

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

    def render(self, save_dir: str, filename: str) -> None:
        os.makedirs(save_dir, exist_ok=True)
        html = self.to_html()
        html = input_html.replace('INNER', self.to_html())
        hti = Html2Image(output_path=save_dir)
        hti.screenshot(html_str=html, save_as=filename)


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
                
    def __repr__(self) -> str:
        representation = '.'.join([self.tag] + self.classes)
        child_representations = ['\t' + repr(child) for child in self.children]

        return '\n'.join([representation] + child_representations)