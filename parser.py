class Parser:
    """
    Takes a string as an input and the current position in the string.
    """
    def __init__(self, input=""):
        self.input = input
        self.pos = 0


    def eof(self):
        """
        Returns true if we are at the end of the string or beyond.
        """
        return self.pos >= len(self.input)

    def peek(self):
        """
        Peeks at the next character in the string without moving forward the pointer.

        The user needs to make sure that we are not at the end of the file.
        """
        assert(not self.eof())
        if self.pos == len(self.input) - 1:
            return ""
        else:
            return self.input[self.pos]

    def starts_with(self, str):
        """
        Returns true if the rest of the string starts with string str
        """
        return self.input[self.pos:self.pos+len(str)].__eq__(str)

    def has_next(self):
        """
        Returns true if another character can be consumed.
        """
        return not self.eof()

    def next(self):
        """
        Consume next character.
        """
        assert(self.has_next())
        self.pos += 1
        return self.input[self.pos-1]

    def next_while(self, condition):
        """
        Keep consuming characters until EOF or condition returns false.
        Returns a string of all the consumed characters.
        """
        result = ""
        while(not self.eof() and condition(self.peek())):
            result += self.next()
        return result

    def next_whitespace(self):
        """
        Keep consuming and discarding characters until EOF or first non white-space is found
        """
        self.next_while(lambda x: x.isspace())