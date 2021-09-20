from parsers.parser import Parser
from defs.css import StyleSheet, Rule, Declaration, Selector, Color

class CSSParser(Parser):
    def parse_rules(self):
        """
        Parse through a series of rules
        """
        rules = []
        while self.has_next():
            self.next_whitespace()
            rules.append(self.parse_rule())
            self.next()
            self.next_whitespace()
        return rules

    def parse_rule(self):
        """
        Parse a selector/declarations pair of rule.
        """
        selectors = self.parse_selectors()
        declarations = self.parse_decalarations()
        return Rule(selectors, declarations)

    def parse_selectors(self):
        """
        Parse a comma separated list of selectors.
        """
        selectors = []
        while self.has_next() and self.peek() != '{':
            selectors.append(self.parse_selector())
            if self.peek() == ',':
                self.next(); self.next_whitespace()
            self.next_whitespace()
        selectors.sort(key=lambda x: x.specificity())
        return selectors

    def parse_selector(self):
        """
        Parses one selector. eg: type#id.class1.class2
        """
        tag, id, classes = None, None, []
        while self.has_next():
            c = self.peek()
            if c == '#':
                self.next()
                id = self.parse_identifier()
            elif c == '.':
                self.next()
                classes.append(self.parse_identifier())
            elif c == '*':
                self.next()
                continue
            elif is_valid_identifier(c):
                tag = self.parse_identifier()
            else:
                break

        return Selector(tag, id, classes)

    def parse_identifier(self):
        """
        Return a single valid identifier
        """
        return self.next_while(is_valid_identifier)

    def parse_decalarations(self):
        """
        Parse a list of declarations enclosed within { ... }
        """
        declarations = []
        assert(self.next() == '{')
        while self.has_next() and self.peek() != '}':
            self.next_whitespace()
            declarations.append(self.parse_declaration())
            self.next_whitespace()
        assert(self.next() == '}')
        return declarations

    def parse_declaration(self):
        """
        Parse and return one property:value declaration.
        """
        name = self.parse_identifier()
        self.next_whitespace()
        assert(self.next() == ':')

        self.next_whitespace()
        value = self.parse_value()
        self.next_whitespace()

        assert(self.next() == ';')
        return Declaration(name, value)

    def parse_value(self):
        """
        Parse and return the value for a property value pair.
        """
        c = self.peek()
        if c.isnumeric():
            return self.next_while(lambda x: x.isnumeric())
        elif c == '#':
            return self.parse_color()
        else:
            return self.next_while(lambda x: x != ';')

    def parse_color(self):
        """
        Parse and return a color object
        """
        def parse_hex(self):
            """
            Parse through a hexcode, wrap it base 256, and return the value
            """
            s = self.input[self.pos:self.pos+2]
            self.pos+=2
            return int(s) % 256
        assert(self.next() == '#')
        return Color(self.parse_hex(), self.parse_hex(), self.parse_hex(), self.parse_hex())

def is_valid_identifier(c):
    """
    Returns true if identifier is valid.
    """
    return c.isalnum() or c == '-' or c == '_'

def parse_css(source):
    """
    Accepts an CSS document as a string, parses it, and returns the populated rules structure.
    """
    rules = CSSParser(source).parse_rules()
    return StyleSheet(rules)