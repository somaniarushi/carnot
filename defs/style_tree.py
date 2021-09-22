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
        If it doesn't exist, return None
        """
        if name not in self.style:
            return None
        return self.style[name]

    def display(self):
        """
        Returns the type of display category in the node,
        defaulting to inline.
        """
        #TODO: Sanitization?
        val = self.value('display')
        if not val:
            return 'inline'
        else:
            return val

    def lookup(self, name, fallback_name, default):
        """
        Return the specified value of property name, or property
        fallback_name if it doesn't exist, or default if
        neither exists.
        """
        if name in self.style:
            return self.style[name]
        elif fallback_name in self.style:
            return self.style[fallback_name]
        else:
            return default
