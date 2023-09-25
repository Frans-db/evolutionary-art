from dataclasses import dataclass, field

@dataclass
class Element:
    tag: str
    properties: list['Property'] = field(default_factory=list)
    children: list['Element'] = field(default_factory=list)

@dataclass
class Property:
    pass