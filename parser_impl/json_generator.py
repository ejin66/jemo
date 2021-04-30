from typing import List

from igenerator import IGenerator
from model import Node, RootNode, MutiNode, ValueType, DataLeafNode, DataObjectNode, ImportNode
from parser_impl.json_template import jsonTemplate

import re


_clsNumber = 0


# 若部分node无name无cls, 可创建一个cls
def geneClassName() -> str:
    global _clsNumber
    _clsNumber += 1
    return "SubItem" + str(_clsNumber)


# 是否是基础类型
def isBasicType(node: Node) -> bool:
    return node.type == ValueType.Double or \
           node.type == ValueType.String or \
           node.type == ValueType.Int or \
           node.type == ValueType.Bool


# 将蛇形转成驼峰形
def formatName(name: str):
    if name == '':
        return name

    name = re.sub("[^a-zA-Z0-9_]", "", name)

    formatName = ''
    items = name.split("_")
    for item in items:
        formatName += item[0].upper() + item[1:]
    formatName = formatName[0].lower() + formatName[1:]
    return formatName


# 获取node对应的变量名称
def nodeName(node: Node) -> str:
    if isinstance(node, DataLeafNode) or isinstance(node, DataObjectNode):
        return node.alias if node.alias != '' else formatName(node.name)
    return ''


# 获取node对应的变量类型
def nodeToClass(node: Node) -> str:
    if node.type == ValueType.Double:
        return "double"

    if node.type == ValueType.Int:
        return "int"

    if node.type == ValueType.String:
        return "String"

    if node.type == ValueType.Bool:
        return "bool"

    if isinstance(node, RootNode):
        return node.cls

    if isinstance(node, DataObjectNode):
        if node.type == ValueType.Object:
            if node.cls != '':
                cls = node.cls
            elif node.name != '':
                name = nodeName(node)
                cls = name[0].upper() + name[1:]
            else:
                node.cls = geneClassName()
                cls = node.cls
            return cls

        # 获取数组中的元素类型
        if node.type == ValueType.Array:
            if len(node.children) == 0:
                cls = "dynamic"
            else:
                cls = nodeToClass(node.children[0])

            return "List<{}>".format(cls)

    raise AttributeError("node to class failed, at line: " + node.source)


def nodeToClsArg(node: Node) -> str:
    if isinstance(node, DataLeafNode):
        name = nodeName(node)
        cls = nodeToClass(node)
        if node.nullable:
            cls += "?"
        return cls + " " + name + ";"

    if isinstance(node, DataObjectNode):
        name = nodeName(node)
        cls = nodeToClass(node)
        if node.nullable:
            cls += "?"
        return cls + " " + name + ";"

    raise AttributeError("node to class arguments failed, at line: " + node.source)


def mapToTypeList(nodeArray: DataObjectNode) -> str:
    node = nodeArray.children[0]
    if node.type == ValueType.Double:
        return "e.toDouble()"

    if node.type == ValueType.Int:
        return "e"

    if node.type == ValueType.String:
        return "e"

    if node.type == ValueType.Bool:
        return "e"

    return nodeToClass(node) + ".fromJson(e)"


def typeListToMap(nodeArray: DataObjectNode) -> str:
    node = nodeArray.children[0]
    if node.type == ValueType.Double:
        return "e"

    if node.type == ValueType.Int:
        return "e"

    if node.type == ValueType.String:
        return "e"

    if node.type == ValueType.Bool:
        return "e"

    return "e.toJson()"


def nodeToFromJson(node: Node) -> str:
    if isinstance(node, DataLeafNode):
        text = "{}: json['{}']".format(nodeName(node), node.name)
        if node.type == ValueType.Double and node.nullable:
            text += "?.toDouble()"
        text += ","
        return text

    if isinstance(node, DataObjectNode):
        json = "json['{}']".format(node.name)

        if node.type == ValueType.Object:
            text = "{0}.fromJson({1})".format(nodeToClass(node), json)
            if node.nullable:
                text = "{} != null ? {} : null".format(json, text)
            text = "{}: {},".format(nodeName(node), text)
            return text

        if node.type == ValueType.Array:
            text = "{}.from({}.map((e) => {}))".format(nodeToClass(node), json, mapToTypeList(node))
            if node.nullable:
                text = "{} != null ? {} : null".format(json, text)
            text = "{}: {},".format(nodeName(node), text)
            return text
    raise AttributeError("node to from json failed, at line: " + node.source)


def nodeToToJson(node: Node) -> str:
    if isinstance(node, DataLeafNode):
        text = r'"{}": {},'.format(node.name, nodeName(node))
        return text

    if isinstance(node, DataObjectNode):
        if node.type == ValueType.Object:
            text = "{}{}.toJson()".format(nodeName(node), "?" if node.nullable else "")
            text = r'"{}": {},'.format(node.name, text)
            return text

        if node.type == ValueType.Array:
            text = "List<dynamic>.from({}{}.map((e) => {}))".format(nodeName(node), "!" if node.nullable else "", typeListToMap(node))
            if node.nullable:
                text = "{} != null ? {} : null".format(nodeName(node), text)
            text = r'"{}": {},'.format(node.name, text)
            return text
    raise AttributeError("node to from json failed, at line: " + node.source)


generatorCodeHeader = """/*
  Don't edit.
  Code generated by jemo.py.
*/

import 'dart:convert';
"""

space = "    "


class JsonGenerator(IGenerator):
    _lineFeed = ''
    _createdClass = []
    _code = ''

    def __init__(self, linefeed: str):
        self._lineFeed = linefeed

    def generate(self, nodes: List[Node]) -> str:
        self._code = generatorCodeHeader
        for node in nodes:
            if isinstance(node, ImportNode):
                self._code += self._generateImportNode(node)
                continue
            self._code += self._generateNode(node)
        return self._code

    def _generateImportNode(self, node: ImportNode) -> str:
        importLibraries = "import '{}';{}".format(node.library, self._lineFeed)

        if node.child is not None:
            importLibraries += self._generateImportNode(node.child)

        return importLibraries

    def _nodeRequired(self, node: Node) -> str:
        if isinstance(node, DataLeafNode) and not node.nullable:
            return 'required '

        if isinstance(node, DataObjectNode) and not node.nullable:
            return 'required '

        return ''

    def _generateNode(self, node: Node) -> str:
        if not isinstance(node, MutiNode):
            return ''

        cls = nodeToClass(node)

        if self._createdClass.__contains__(cls):
            return ''

        self._createdClass.append(cls)

        clsArgs = ''
        clsConstructionArgs = ''
        fromJson = ''
        toJson = ''
        superCls = "extends " + node.super + " " if isinstance(node, RootNode) and node.super != "" else ""

        subNodes: List[DataObjectNode] = []

        for child in node.children:
            clsArgs += space + nodeToClsArg(child) + self._lineFeed
            clsConstructionArgs += "{}{}this.{},{}".format(space + space, self._nodeRequired(child), nodeName(child), self._lineFeed)
            fromJson += "{}{}{}{}".format(space, space, nodeToFromJson(child), self._lineFeed)
            toJson += "{}{}{}{}".format(space, space, nodeToToJson(child), self._lineFeed)

            tmpNode = child
            while True:
                if not isinstance(tmpNode, DataObjectNode):
                    break

                if len(tmpNode.children) == 0:
                    break

                if tmpNode.type == ValueType.Object:
                    subNodes.append(tmpNode)
                    break

                if tmpNode.type == ValueType.Array:
                    tmpNode = tmpNode.children[0]
                    continue

                break

        result = jsonTemplate.format(cls, clsArgs.rstrip(),
                                     clsConstructionArgs.rstrip(), fromJson.rstrip(),
                                     toJson.rstrip(), superCls)

        for child in subNodes:
            result += self._generateNode(child)

        return result
