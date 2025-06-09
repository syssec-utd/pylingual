def make_html_words(self, words):
    """ convert a series of simple words into some HTML text """
    line = ''
    if words:
        line = html_quote(words[0])
        for w in words[1:]:
            line = line + ' ' + html_quote(w)
    return line