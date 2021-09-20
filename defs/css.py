class StyleSheet:
    """
    Maintains a list of rules in a stylesheet.
    """
    def __init__(self, rules=[]):
        self.rules = rules

class Rule:
    """
    Contains a list of selectors and a dictionary of related declarations.
    """
    def __init__(self, selectors = [], declarations = []):
        self.selectors = selectors
        self.declarations = declarations

class Selector:
    """
    Contains a selector for a tag, with the tag name, id and class name.
    """
    def __init__(self, tag_name="", id="", classes=[]):
        self.tag_name = tag_name
        self.id = id
        self.classes = classes

    def specificity(self):
        """
        Return a numeric value for the specificity of the selector
        """
        #TODO: add support for multiple id and multiplpe tag names
        return 2 + len(self.classes)

class Declaration:
    """
    Contains a dictionary of properties and their values
    """
    def __init__(self, name="", value=""):
        self.values={}
        self.name = name
        if name:
            self.values[name] = value

    def add(self, name, value):
        self.values[name] = value

    def value(self, name):
        return self.values[name]

class Color:
    """
    Defines a color in a stylesheet.
    """
    def __init__(self, r=0, g=0, b=0, a=0):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

