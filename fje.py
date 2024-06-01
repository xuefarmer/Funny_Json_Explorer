import json
import argparse
from abc import ABC, abstractmethod
import copy
from config import icon_family
from Component import  *
from style import *
from Factory import *
# Abstract Component Class


# Abstract Factory Interface


# Abstract Builder Interface
class Builder(ABC):
    @abstractmethod
    def get_result(self):
        pass

    @abstractmethod
    def add_object(self, name, parent=None, style="tree"):
        pass

    @abstractmethod
    def add_leaf(self, name, value=None, parent=None, style="tree"):
        pass

# Concrete Builder Class
class JsonBuilder(Builder):
    def __init__(self, factory: JSONshowFactory, icon: int):
        self.factory = factory
        self.icon = icon
        self.root = self.factory.create_object("root", 'tree', icon, 0)
        self.total_nodes = 0
        self.position = 0

    def add_object(self, name, parent=None, style="tree"):
        self.position += 1
        obj = self.factory.create_object(name, style, self.icon, self.position)
        if parent:
            parent.add(obj)
        else:
            self.root.add(obj)
        self.total_nodes += 1
        return obj

    def add_leaf(self, name, value=None, parent=None, style="tree"):
        self.position += 1
        leaf = self.factory.create_leaf(name, value, style, self.icon, self.position)
        if parent:
            parent.add(leaf)
        else:
            self.root.add(leaf)
        self.total_nodes += 1
        return leaf

    def get_result(self):
        return self.root

# Director Class
class Director:
    def __init__(self, builder: Builder):
        self.builder = builder

    def construct(self, data, parent=None, style="tree"):
        count = 0
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    obj = self.builder.add_object(key, parent, style=style)
                    count += self.construct(value, obj, style)
                else:
                    self.builder.add_leaf(key, value=value, parent=parent, style=style)
                count += 1
        elif isinstance(data, list):
            for index, item in enumerate(data):
                if isinstance(item, (dict, list)):
                    obj = self.builder.add_object(f"[{index}]", parent, style=style)
                    count += self.construct(item, obj, style)
                else:
                    self.builder.add_leaf(f"[{index}]", value=item, parent=parent, style=style)
                count += 1
        else:
            self.builder.add_leaf(str(data), value=data, parent=parent, style=style)
            count += 1
        return count

# Main Function
def main():
    print("21307296 薛锦俊")
    parser = argparse.ArgumentParser(description='Funny JSON Explorer (FJE)')
    parser.add_argument('-f', '--file', required=True, help='JSON file to visualize')
    parser.add_argument('-s', '--style', choices=['tree', 'rectangle'], required=True, help='Visualization style')
    parser.add_argument('-i', '--icon', choices=list(map(str, range(len(icon_family)))), required=True, help='Icon set to use')
    args = parser.parse_args()

    with open(args.file, 'r') as f:
        json_data = json.load(f)

    if args.style == 'tree':
        factory = TreeshowFactory()
    elif args.style == 'rectangle':
        factory = RectangleshowFactory()

    icon = int(args.icon)  # Convert icon argument to integer
    builder = JsonBuilder(factory, icon)
    director = Director(builder)
    total = director.construct(json_data, style=args.style)

    result = builder.get_result()
    # Define the desired line length
    line_length = 100
    # Pass is_root=True to skip showing the root node's name
    print(result.show(is_root=True, total=total, line_length=line_length))

if __name__ == "__main__":
    main()
