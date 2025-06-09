from __future__ import absolute_import
from .base import Type

class Woff(Type):
    """
    Implements the WOFF font type matcher.
    """
    MIME = 'application/font-woff'
    EXTENSION = 'woff'

    def __init__(self):
        super(Woff, self).__init__(mime=Woff.MIME, extension=Woff.EXTENSION)

    def match(self, buf):
        return len(buf) > 7 and buf[0] == 119 and (buf[1] == 79) and (buf[2] == 70) and (buf[3] == 70) and (buf[4] == 0 and buf[5] == 1 and (buf[6] == 0) and (buf[7] == 0) or (buf[4] == 79 and buf[5] == 84 and (buf[6] == 84) and (buf[7] == 79)) or (buf[4] == 116 and buf[5] == 114 and (buf[6] == 117) and (buf[7] == 101)))

class Woff2(Type):
    """
    Implements the WOFF2 font type matcher.
    """
    MIME = 'application/font-woff'
    EXTENSION = 'woff2'

    def __init__(self):
        super(Woff2, self).__init__(mime=Woff2.MIME, extension=Woff2.EXTENSION)

    def match(self, buf):
        return len(buf) > 7 and buf[0] == 119 and (buf[1] == 79) and (buf[2] == 70) and (buf[3] == 50) and (buf[4] == 0 and buf[5] == 1 and (buf[6] == 0) and (buf[7] == 0) or (buf[4] == 79 and buf[5] == 84 and (buf[6] == 84) and (buf[7] == 79)) or (buf[4] == 116 and buf[5] == 114 and (buf[6] == 117) and (buf[7] == 101)))

class Ttf(Type):
    """
    Implements the TTF font type matcher.
    """
    MIME = 'application/font-sfnt'
    EXTENSION = 'ttf'

    def __init__(self):
        super(Ttf, self).__init__(mime=Ttf.MIME, extension=Ttf.EXTENSION)

    def match(self, buf):
        return len(buf) > 4 and buf[0] == 0 and (buf[1] == 1) and (buf[2] == 0) and (buf[3] == 0) and (buf[4] == 0)

class Otf(Type):
    """
    Implements the OTF font type matcher.
    """
    MIME = 'application/font-sfnt'
    EXTENSION = 'otf'

    def __init__(self):
        super(Otf, self).__init__(mime=Otf.MIME, extension=Otf.EXTENSION)

    def match(self, buf):
        return len(buf) > 4 and buf[0] == 79 and (buf[1] == 84) and (buf[2] == 84) and (buf[3] == 79) and (buf[4] == 0)