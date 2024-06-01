import argparse
from abc import ABC, abstractmethod
import copy
from config import icon_family
from style import  *
class JSONComponent(ABC):
    def __init__(self):
        self.position = 0
    @abstractmethod
    def show(self, indent: str = "", is_last: bool = False, is_root: bool = False, total: int = 1, line_length: int = 80) -> str:
        pass

    def add(self, component):
        pass

    @abstractmethod
    def clone(self):
        pass


class JSONObject(JSONComponent):
    def __init__(self, name, style, icon=0, position=0):
        self.name = name
        self.children = []
        self.icon = icon_family[icon][0]
        self.position = position
        if style == 'rectangle':
            self.show_style = RectangleShowstyle()
        elif style == 'tree':
            self.show_style = TreeShowstyle()

    def add(self, component: JSONComponent):
        self.children.append(component)

    def show(self, indent: str = "", is_last: bool = False, is_root: bool = False, total: int = 1, line_length: int = 100) -> str:
        return self.show_style.show(self, indent, is_last, is_root, total, line_length)

    def clone(self):
        return copy.deepcopy(self)

class JSONLeaf(JSONComponent):
    def __init__(self, name, value=None, style="tree", icon=0, position=0):
        self.name = name
        self.value = value
        self.icon = icon_family[icon][1]
        self.position = position
        if style == 'rectangle':
            self.show_style = LeafRectangleShowstyle()
        elif style == 'tree':
            self.show_style = LeafTreeShowstyle()

    def show(self, indent: str = "", is_last: bool = False, is_root: bool = False, total: int = 1, line_length: int = 80) -> str:
        return self.show_style.show(self, indent, is_last, is_root, total, line_length)

    def clone(self):
        return copy.deepcopy(self)