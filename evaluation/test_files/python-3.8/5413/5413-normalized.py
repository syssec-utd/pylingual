def compose(chosung, joongsung, jongsung=u''):
    """This function returns a Hangul letter by composing the specified chosung, joongsung, and jongsung.
    @param chosung
    @param joongsung
    @param jongsung the terminal Hangul letter. This is optional if you do not need a jongsung."""
    if jongsung is None:
        jongsung = u''
    try:
        chosung_index = CHO.index(chosung)
        joongsung_index = JOONG.index(joongsung)
        jongsung_index = JONG.index(jongsung)
    except Exception:
        raise NotHangulException('No valid Hangul character index')
    return unichr(44032 + chosung_index * NUM_JOONG * NUM_JONG + joongsung_index * NUM_JONG + jongsung_index)