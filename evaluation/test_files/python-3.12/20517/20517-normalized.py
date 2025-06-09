def highlight_text(needles, haystack, cls_name='highlighted', words=False, case=False):
    """ Applies cls_name to all needles found in haystack. """
    if not needles:
        return haystack
    if not haystack:
        return ''
    if words:
        pattern = '(%s)' % '|'.join(['\\b{}\\b'.format(re.escape(n)) for n in needles])
    else:
        pattern = '(%s)' % '|'.join([re.escape(n) for n in needles])
    if case:
        regex = re.compile(pattern)
    else:
        regex = re.compile(pattern, re.I)
    i, out = (0, '')
    for m in regex.finditer(haystack):
        out += ''.join([haystack[i:m.start()], '<span class="%s">' % cls_name, haystack[m.start():m.end()], '</span>'])
        i = m.end()
    return mark_safe(out + haystack[i:])