import datetime
from .MTDateTime import MTDateTime
from .enums import DateTimeSkips

class MTDate(MTDateTime):

    def __init__(self, value=None, pattern=None):
        """
        Constructor.

        pattern: Date-time pattern that is used when value is a string.
        value: Date value.
        """
        MTDateTime.__init__(self, value, pattern)
        self.skip |= DateTimeSkips.HOUR
        self.skip |= DateTimeSkips.MINUTE
        self.skip |= DateTimeSkips.SECOND
        self.skip |= DateTimeSkips.MILLISECOND

    def _remove(self, format_):
        format_ = MTDateTime._remove_(format_, '%H', True)
        format_ = MTDateTime._remove_(format_, '%-H', True)
        format_ = MTDateTime._remove_(format_, '%I', True)
        format_ = MTDateTime._remove_(format_, '%-I', True)
        format_ = MTDateTime._remove_(format_, '%M', True)
        format_ = MTDateTime._remove_(format_, '%-M', True)
        format_ = MTDateTime._remove_(format_, '%S', True)
        format_ = MTDateTime._remove_(format_, '%-S', True)
        str_ = datetime.datetime.now().strftime('%p')
        format_ = MTDateTime._remove_(format_, str_, True)
        return format_