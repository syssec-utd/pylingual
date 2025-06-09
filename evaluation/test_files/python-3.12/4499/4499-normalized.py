def __truncate(self, line_arr, max_width):
    """  Cut tuple of line chunks according to it's wisible lenght  """

    def is_space(chunk):
        return all([True if i == ' ' else False for i in chunk])

    def is_empty(chunks, markups):
        result = []
        for chunk in chunks:
            if chunk in markups:
                result.append(True)
            elif is_space(chunk):
                result.append(True)
            else:
                result.append(False)
        return all(result)
    left = max_width
    result = ''
    markups = self.markup.get_markup_vars()
    for num, chunk in enumerate(line_arr):
        if chunk in markups:
            result += chunk
        elif left > 0:
            if len(chunk) <= left:
                result += chunk
                left -= len(chunk)
            else:
                leftover = (chunk[left:],) + line_arr[num + 1:]
                was_cut = not is_empty(leftover, markups)
                if was_cut:
                    result += chunk[:left - 1] + self.markup.RESET + u'…'
                else:
                    result += chunk[:left]
                left = 0
    return result