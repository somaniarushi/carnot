from enum import Enum

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

    def padding_box(self):
        return self.content.expanded_by(self.padding)

    def border_box(self):
        return self.content.expanded_by(self.border)

    def margin_box(self):
        return self.content.expanded_by(self.margin)

class Rect:
    """
    Keeps track of the location of a element on the webpage.
    """
    def __init__(self, x=0, y=0, height=0, width=0):
        self.x = x
        self.y = y
        self.height = height
        self.width = width

    def expanded_by(self, edge):
        return Rect(
                self.x - edge.left,
                self.y - edge.top,
                self.width + edge.left + edge.right,
                self.height + edge.top + edge.bottom
            )

class Edge:
    """
    Stores the four-directional value of an element.
    """
    def __init__(self, right=0, left=0, top=0, bottom=0):
        self.right = right
        self.left = left
        self.top = top
        self.bottom = bottom


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
    def __init__(self, dimensions=None, style_node=None, type=BoxType.INLINE_NODE, children=[]):
        self.dimensions = dimensions if dimensions else Dimensions().set_default()
        self.style_node = style_node
        self.type = type
        self.children = children

class BlockBox(Box):
    def __init__(self, dimensions=None, style_node=None, children=[]):
        super().__init__(dimensions, style_node, BoxType.BLOCK_NODE, children)

    def get_inline_container(self):
        """
        Return a container for inline boxes.
        """
        last_box = self.children[-1] if self.children else None
        if not (last_box and last_box.type == BoxType.ANONYMOUS):
            last_box = AnonBox()
            self.children.append(last_box)
        return last_box

    def get_style_node(self):
        """
        Return the associated style_node
        """
        return self.style_node

    def layout(self, container):
        """
        Lay out a box and its descendants.
        """
        self.dimensions = self.calculate_width(container)
        self.calculate_position(container)
        self.layout_children()
        self.calculate_height()

    def calculate_position(self, container):
        """
        Calculate position of self.
        """
        style = self.get_style_node()
        d = self.dimensions

        d.margin.top = style.lookup("margin-top", "margin", 0)
        d.margin.bottom = style.lookup("margin-bottom", "margin", 0)

        d.border.top = style.lookup("border-top-width", "border-width", 0)
        d.border.bottom = style.lookup("border-bottom-width", "border-width", 0)

        d.padding.top = style.lookup("padding-top", "padding", 0)
        d.padding.bottom = style.lookup("padding-bottom", "padding", 0)

        d.content.x = container.content.x + d.margin.left + d.border.left + d.padding.left
        d.content.y = container.content.y + d.margin.top + d.border.top + d.padding.top


    def layout_children(self):
        """
        Layout the children of self.
        """
        d = self.dimensions
        for child in self.children:
            child.layout(self)
            d.content.height += child.dimensions.margin_box().height


    def calculate_height(self):
        """
        If a manual height has been specified for the box, use it.
        """
        style = self.get_style_node()
        if (style.value('height')):
            self.dimensions.content.height = style.value('height')

    def calculate_width(self, container):
        """
        Calculate the width of self.
        """

        style = self.get_style_node()
        width = style.value('width') or 'auto'

        margin_left = style.lookup('margin-right', 'margin', 0.0)
        margin_right = style.lookup('margin-left', 'margin', 0.0)

        border_left = style.lookup('border-left-width', 'border-width', 0.0)
        border_right = style.lookup('border-right-width', 'border-width', 0.0)

        padding_left = style.lookup('padding-left', 'padding', 0.0)
        padding_right = style.lookup('padding-right', 'padding', 0.0)

        total = sum(map(lambda x: x if x.isdigit() else 0, [margin_left, margin_right, border_left, border_right, padding_left, padding_right]))

        # if you're overfilling your container and the width isn't adjustable, no margins required. Set auto margin = 0
        if width != 'auto' and total > container.content.width:
            if margin_left == 'auto':
                margin_left = 0.0
            if margin_right == 'auto':
                margin_right = 0.0

        # How much space we got left over
        underflow = container.content.width - total

        if width != 'auto':
            if margin_left != 'auto' and margin_right != 'auto': # if everything constrained, right margin changes
                margin_right += underflow

            elif margin_left != 'auto' and margin_right == 'auto':
                margin_right = underflow

            elif margin_left == 'auto' and margin_right != 'auto':
                margin_left = underflow

            else:
                margin_left, margin_right = underflow/2.0, underflow/2.0

        else:
            if margin_left == 'auto':
                margin_left = 0.0

            if margin_right == 'auto':
                margin_right = 0.0

            if underflow >= 0:
                width = underflow
            else:
                width = 0.0
                margin_right += underflow

        return Dimensions(
                    Rect(width=width),
                    Edge(padding_right, padding_left),
                    Edge(border_right, border_left),
                    Edge(margin_right, margin_left)
                )

class InlineBox(Box):
    def __init__(self, style_node=None, dimensions=None, children=[]):
        super().__init__(dimensions, style_node, BoxType.INLINE_NODE, children)

    def get_inline_container(self):
        """
        Return a container for inline elements.
        """
        return self

    def get_style_node(self):
        """
        Return associated style node.
        """
        return self.style_node

    def layout(self, container):
        """
        Lay out a box and its descendants.
        """
        pass

class AnonBox(Box):
    def __init__(self, dimensions=None, children=[]):
        super().__init__(dimensions, None, BoxType.ANONYMOUS, children)

    def get_inline_container(self):
        """
        Return a container for inline boxes.
        """
        return self

    def get_style_node(self):
        """
        Return associated style node.
        """
        raise Exception('Anonymous container cannot have style node!')

    def layout(self, container):
        """
        Lay out a box and its descendants.
        """
        pass
