from typing import List

from iparser import IParser
from model import Node, RootNode, ValueType, DataLeafNode, DataObjectNode, ImportNode
from parser_impl.mark import RootMark, LeafMark, ObjectMark, ImportMark
import re


def _readKey(line: str) -> str:
    result = re.match(r'"(.*)":', line)
    return "" if result is None else result.group(1)


def _readValue(line: str) -> str:
    result = re.match(r'.*:(.*)', line)

    if result is None:
        value = line.strip()
    else:
        value = result.group(1).strip()
    if value.endswith(","):
        return value[:-1]
    return value


def _inferType(value) -> ValueType:
    if value.startswith(r'"'):
        return ValueType.String

    if value == "true" or value == "false":
        return ValueType.Bool

    if value.__contains__("."):
        return ValueType.Double

    int(value)
    return ValueType.Int


class JsonParser(IParser):
    _currentNode = None
    _cachedMark = ''
    _lineFeed = ''
    _segments = []
    _nodes = []

    def __init__(self, lineFeed: str):
        self._lineFeed = lineFeed

    def parse(self, data: bytes) -> List[Node]:
        s = bytes.decode(data)
        lines = s.split(self._lineFeed)
        self._segment(lines)
        self._segmentToNode()
        return self._nodes

    def _segment(self, lines: List[str]):
        segment = []
        for line in lines:
            if line == "":
                if len(segment) != 0:
                    self._segments.append(segment)
                segment = []
            else:
                segment.append(line)
        if len(segment) != 0:
            self._segments.append(segment)

    def _segmentToNode(self):
        if len(self._segments) == 0:
            return

        for segment in self._segments:
            self._currentNode = None
            self._nodes.append(self._parseNode(segment))

    def _parseNode(self, segment: List[str]) -> Node:
        root = None

        lineNumber = 0

        for line in segment:
            lineNumber += 1
            node = self._parseLine(line.strip(), lineNumber)
            if root is None and node is not None:
                root = node
                continue

        return root

    def _parseLine(self, line: str, lineNumber: int):
        if line.__contains__("}"):
            self._currentNode = self._currentNode.parent
            return

        if line.__contains__("{"):
            # 开始对象)
            if self._currentNode is None:
                node = self._parseHeader()
                self._currentNode = node
            else:
                node = self._parseObject(line, lineNumber, False)
                self._currentNode.attach(node)
                self._currentNode = node
            return node

        if line.__contains__("["):
            # 开始数组
            node = self._parseObject(line, lineNumber, True)
            self._currentNode.attach(node)
            self._currentNode = node
            return node

        if line.startswith("]"):
            # 数组结束
            self._currentNode = self._currentNode.parent
            return

        if line.startswith("//import"):
            node = self._parseImport(line)
            if self._currentNode is None:
                self._currentNode = node
                return node
            else:
                self._currentNode.attach(node)
                return

        if line.startswith("//"):
            self._cachedMark = line
            return

        # 叶子节点
        node = self._parseLeaf(line, lineNumber)
        self._currentNode.attach(node)

    def _parseImport(self, line: str) -> Node:
        node = ImportNode()
        mark = ImportMark()
        mark.read(line[2:])
        node.library = mark.library
        return node

    def _parseHeader(self) -> Node:
        if len(self._cachedMark) == 0:
            raise Exception("json header is absent")

        mark = RootMark()
        mark.read(self._cachedMark[2:])
        self._cachedMark = ""

        root = RootNode()
        root.cls = mark.cls
        root.super = mark.super
        return root

    def _parseLeaf(self, line: str, lineNumer: int) -> Node:
        node = DataLeafNode()
        node.source = "{}, line number: {}".format(line, lineNumer)

        if len(self._cachedMark) != 0:
            mark = LeafMark()
            mark.read(self._cachedMark[2:])
            self._cachedMark = ""

            node.alias = mark.alias
            node.nullable = mark.nullable

        node.name = _readKey(line)
        node.value = _readValue(line)
        node.type = _inferType(node.value)
        return node

    def _parseObject(self, line: str, lineNumer: int, array: bool) -> Node:
        node = DataObjectNode(array)
        node.source = "{}, line number: {}".format(line, lineNumer)

        if len(self._cachedMark) != 0:
            mark = ObjectMark()
            mark.read(self._cachedMark[2:])
            self._cachedMark = ""

            node.cls = mark.cls
            node.alias = mark.alias
            node.nullable = mark.nullable

        node.name = _readKey(line)
        return node
