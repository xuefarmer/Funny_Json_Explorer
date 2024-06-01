from abc import ABC, abstractmethod
import copy
from config import icon_family
from Component import *
# Show style Interface
class Showstyle(ABC):
    @abstractmethod
    def show(self, component, indent: str, is_last: bool, is_root: bool, total: int, line_length: int = 100) -> str:
        pass

# Concrete Show Strategies for JSONObject
class TreeShowstyle(Showstyle):
    def show(self, component, indent: str, is_last: bool, is_root: bool, total: int, line_length: int = 100) -> str:
        if is_root:
            result = ""
        else:
            line_prefix = "└─ " if is_last else "├─ "
            result = f"{indent}{line_prefix}{component.icon}{component.name}\n"
        for i, child in enumerate(component.children):
            label = "   " if is_last else "│  "
            if is_root:
                label = ""
            result += child.show(indent + label, i == len(component.children) - 1, False, total)
        return result


class LeafTreeShowstyle(Showstyle):
    def show(self, component, indent: str, is_last: bool, is_root: bool, total: int, line_length: int = 100) -> str:
        line_prefix = "└─ " if is_last else "├─ "
        if component.value is not None:
            return f"{indent}{line_prefix}{component.icon}{component.name}: {component.value}\n"
        else:
            return f"{indent}{line_prefix}{component.icon}{component.name}\n"



class RectangleShowstyle(Showstyle):
    def show(self, component, indent: str, is_last: bool, is_root: bool, total: int, line_length: int = 100) -> str:
        if is_root:
            result = ""
        else:
            if component.position == total:
                line_prefix = "└─"
            elif component.position == 1:
                line_prefix = "┌─ "
            else:
                line_prefix = "├─ "
            line_content = f"{indent}{line_prefix}{component.icon}{component.name}"
            padding = line_length - len(line_content) - 2  # Account for the '┐' or '┤'
            if component.position == 1:
                result = f"{line_content} {'─' * padding}┐\n"
            else:
                result = f"{line_content} {'─' * padding}┤\n"
        for i, child in enumerate(component.children):
            label = "│  "
            if is_root:
                label = ""
            if component.position + i + 1 == total:
                label = "└─ "
            result += child.show(indent + label, i == len(component.children), False, total, line_length)
        return result

# Concrete Show Strategies for JSONLeaf


class LeafRectangleShowstyle(Showstyle):
    def show(self, component, indent: str, is_last: bool, is_root: bool, total: int, line_length: int = 100) -> str:
        if component.position == total:
            line_prefix = "└─ "
        elif component.position == 1:
            line_prefix = "┌─ "
        else:
            line_prefix = "├─ "
        line_content = f"{indent}{line_prefix}{component.icon}{component.name}"
        if component.value is not None:
            line_content += f": {component.value}"
        padding = line_length - len(line_content) - 2  # Account for the '┤'
        if component.position == 1:
            result = f"{line_content} {'─' * padding}┐\n"
        elif component.position == total:
            result = f"{line_content} {'─' * padding}┘\n"
        else:
            result = f"{line_content} {'─' * padding}┤\n"
        return result
