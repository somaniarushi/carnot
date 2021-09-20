from enum import Enum

class BoxType(Enum):
    """
    Enumerates all possible types of boxes
    """
    BLOCK_NODE = 1
    INLINE_NODE = 2
    ANONYMOUS = 3

class Box:
    """
    Models a node on the screen.
    """
    def __init__(self, dimensions=None, type=BoxType.INLINE_NODE, children=[]):
        self.dimensions = dimensions if dimensions else Dimensions().set_default()
        self.type = type
        self.children = children


class InlineBox(Box):
    def __init__(self, dimensions=None, children=[]):
        super().__init__(dimensions, BoxType.INLINE_NODE, children)

    def get_inline_container(self):
        return self


class BlockBox(Box):
    def __init__(self, dimensions=None, children=[]):
        super().__init__(dimensions, BoxType.BLOCK_NODE, children)

    def get_inline_container(self):
        last_box = self.children[-1] if self.children else None
        if not (last_box and last_box.box_type == BoxType.ANONYMOUS):
            last_box = AnonBox()
            self.children.append(last_box)
        return last_box



class AnonBox(Box):
    def __init__(self, dimensions=None, children=[]):
        super().__init__(dimensions, BoxType.ANONYMOUS, children)

    def get_inline_container(self):
        return self


class Dimensions:
    """
    Models a box display for an element on the webpage.
    """
    def __init__(self, content=None, padding=None, border=None, margin=None):
        self.content = content
        self.padding = padding
        self.border = border
        self.margin = margin

    def set_default(self):
        self.content = Rect()
        self.padding, self.border, self.margin = Edge(), Edge(), Edge()

class Rect:
    """
    Keeps track of the location of a element on the webpage.
    """
    def __init__(self, x=0, y=0, height=0, weight=0):
        self.x = x
        self.y = y
        self.height = height
        self.weight = weight

class Edge:
    """
    Stores the four-directional value of an element.
    """
    def __init__(self, right=0, left=0, top=0, bottom=0):
        self.right = right
        self.left = left
        self.top = top
        self.bottom = bottom
