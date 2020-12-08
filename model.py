from enum import Enum
from typing import List


class ValueType(Enum):
    Unknown = -1
    Root = 0,
    Int = 1
    Double = 2
    Bool = 3
    String = 4
    Object = 5
    Array = 6


class Node:
    name = ''
    type = ValueType.Unknown
    parent = None
    source = ''

    def attach(self, node):
        pass


class LeafNode(Node):

    def attach(self, node):
        pass


class ImportNode(Node):
    library = ''
    child = None

    def attach(self, node):
        self.child = node

class MutiNode(Node):
    children: List[Node]

    def attach(self, node):
        node.parent = self
        self.children.append(node)


class RootNode(MutiNode):
    cls = ""
    super = ""

    def __init__(self):
        self.children = []


class DataLeafNode(LeafNode):
    alias = ''
    nullable = False


class DataObjectNode(MutiNode):
    cls = ''
    alias = ''
    nullable = False

    def __init__(self, array: bool):
        self.children = []
        self.type = ValueType.Array if array else ValueType.Object