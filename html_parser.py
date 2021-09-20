from dom import TextNode, ElementNode
from parser import Parser

"""
The parser is supposed to take an HTML file as an input,
read it and return the DOM structure using our classes.
"""

class HTMLParser(Parser):
    def parse_tag(self):
        """
        Goes through a tag or attribute and returns its value.
        """
        return self.next_while(lambda x: x.isalnum())

    def parse_node(self):
        """
        Goes through a node and parses it
        """
        if self.peek() == '<':
            return self.parse_element()
        else:
            return self.parse_text()

    def parse_text(self):
        """
        Parses through text until a tag opening is found, and returns the value as a text node.
        """
        text = self.next_while(lambda x: not x.__eq__('<'))
        return TextNode(text)


    def parse_element(self):
        """
        Parses through an element tag until a closing tag is found, and returns the value as an element node.
        """
        # Opening Tag
        assert(self.next() == '<')
        tag_name = self.parse_tag()
        attr = self.parse_attributes()
        assert(self.next() == '>')

        # Children
        children = self.parse_nodes()

        # Closing Tag Validation
        assert(self.next() == '<')
        assert(self.next() == '/')
        assert(self.parse_tag() == tag_name)
        assert(self.next() == '>')

        return ElementNode(children, tag_name, attr)

    def parse_nodes(self):
        """
        Parse a sequence of sibling nodes.
        """
        nodes = []
        while not self.eof() and not self.starts_with("</"):
            self.next_whitespace()
            nodes.append(self.parse_node())
            self.next_whitespace()
        return nodes

    def parse_attributes(self):
        """
        Parse a list of name="value" pairs, separated by whitespace, returning a dictionary
        """
        def parse_attribute(self):
            """
            Return a single name="value" pair as a tuple
            """
            def parse_attribute_value(self):
                assert(self.next() == '"')
                value = self.next_while(lambda x: not x.__eq__('"'))
                assert(self.next() == '"')
                return value
            name = self.parse_tag()
            assert(self.next() == '=')
            value = self.parse_attribute_value()
            return (name, value)

        attr = {}
        while (not self.peek().__eq__('>')):
            self.next_whitespace()
            name, value = self.parse_attribute()
            attr[name] = value

        return attr


def parse(source):
    """
    Accepts an HTML document as a string, parses it, and returns the populated DOM tree structure.
    """
    nodes = HTMLParser(source).parse_nodes()
    if len(nodes) == 1: # root element exists
        return nodes[0]
    else: # no root node
        return ElementNode(nodes, 'html')


