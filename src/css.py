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

class Declaration:
    """
    Contains a dictionary of properties and their values
    """
    def __init__(self, name="", value=""):
        self.values={}
        if name:
            self.values[name] = value

    def add(self, name, value):
        self.values[name] = value


