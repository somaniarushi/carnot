from enum import Enum

class NodeType(Enum):
    """
    Enumerated list of all the types of nodes implemented.
    """
    ELEMENT = 1
    TEXT = 2


class Node:
    """
    A class that defines a node of the DOM. Contains a list of
    other nodes and the type of the node.
    """
    def __init__(self, children = [], node_type=NodeType.TEXT):
        self.children = children
        self.node_type = node_type

class ElementNode(Node):
    """
    A class that creates an element node of the DOM.
    """
    def __init__(self, children=[], tag_name=None, attr={}):
        super().__init__(children, NodeType.ELEMENT)
        self.tag_name = tag_name
        self.attr = attr

    def id(self):
        if 'id' in self.attr:
            return self.attr['id']
        else:
            return None

    def classes(self):
        if 'class' not in self.attr:
            return []
        return self.attr['class'].split(' ')

class TextNode(Node):
    """
    A class that creates a text node of the DOM.
    """
    def __init__(self, text="", attr={}):
        super().__init__(None, NodeType.TEXT)
        self.text = text
        self.attr = attr



