from parser import Parser
from css import Declaration, Selector

class CSSParser(Parser):
    def parse_selector(self):
        """
        Parses one selector. eg: type#id.class1.class2
        """
        tag, id, classes = "", "", []
        while self.has_next():
            c = self.next()
            if c == '#':
                id = self.parse_identifier()
            elif c == '.':
                classes.append(self.parse_identifier())
            elif c == '*':
                continue
            elif self.is_valid_identifier(c):
                tag = self.parse_identifier()
            else:
                raise EOFError('Found unidentified character')

        return Selector(tag, id, classes)

    def parse_identifier(self):
        """
        Return a single valid identifier
        """
        return self.next_while(is_valid_identifier)

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


def is_valid_identifier(c):
    """
    Returns true if identifier is valid.
    """
    return c.isalnum() or c == '-' or c == '_'