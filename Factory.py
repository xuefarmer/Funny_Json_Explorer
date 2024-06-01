import json
import argparse
from abc import ABC, abstractmethod
import copy
from config import icon_family
from Component import *
class JSONshowFactory(ABC):
    @abstractmethod
    def create_object(self, name, style, icon, position) -> JSONComponent:
        pass

    @abstractmethod
    def create_leaf(self, name, value, style, icon, position) -> JSONComponent:
        pass

# Concrete Factory Classes
class TreeshowFactory(JSONshowFactory):
    def create_object(self, name, style, icon, position) -> JSONComponent:
        return JSONObject(name, style, icon, position)

    def create_leaf(self, name, value, style, icon, position) -> JSONComponent:
        return JSONLeaf(name, value, style, icon, position)

class RectangleshowFactory(JSONshowFactory):
    def create_object(self, name, style, icon, position) -> JSONComponent:
        return JSONObject(name, style, icon, position)

    def create_leaf(self, name, value, style, icon, position) -> JSONComponent:
        return JSONLeaf(name, value, style, icon, position)