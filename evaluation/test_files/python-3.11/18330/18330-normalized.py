def number(self, text):
    """number = digit - "0" . {digit} ;"""
    self._attempting(text)
    return concatenation([exclusion(self.digit, '0'), zero_or_more(self.digit, ignore_whitespace=False)], ignore_whitespace=False)(text).compressed(TokenType.number)