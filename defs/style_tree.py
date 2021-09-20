class StyledNode:
    """
    Consists of the node, along with associated dictionary of styles.
    """
    def __init__(self, node=None, style={}, children=[]):
        self.node = node
        self.style = style
        self.children = children

    def value(self, name):
        """
        Return the value of a property of the associated stylesheet.
        """
        if name not in self.style:
            return None
        return self.style[name]

