from refinery.units.pattern import Arg, RegexUnit
from refinery.units.meta import ConditionalUnit

class iffx(RegexUnit, ConditionalUnit):
    """
    Filter incoming chunks by discarding those that do not match the given
    regular expression.
    """

    def __init__(self, regex, multiline=False, ignorecase=False, negate=False, temporary=False, match: Arg.Switch('-m', help='Perform a full match rather than matching anywhere in the chunk.')=False):
        super().__init__(regex=regex, negate=negate, temporary=temporary, multiline=multiline, ignorecase=ignorecase, match=match)

    def match(self, chunk):
        return bool(self._matcher(chunk))

    def filter(self, chunks):
        self._matcher = self.regex.fullmatch if self.args.match else self.regex.search
        yield from super().filter(chunks)