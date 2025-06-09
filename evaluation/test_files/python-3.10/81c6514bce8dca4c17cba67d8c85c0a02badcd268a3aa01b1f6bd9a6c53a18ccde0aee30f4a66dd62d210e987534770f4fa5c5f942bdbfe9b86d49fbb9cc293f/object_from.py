from .base import BaseSource
__all__ = ['BuildObjectFrom']

class BuildObjectFrom(BaseSource):
    """
    A source that outputs a single key with given name, and as it's contents the contents
    of it's child.
    """
    __slots__ = ('key', 'child')

    def __init__(self, key: str, child: BaseSource):
        self.key = key
        self.child = child

    def provide(self) -> dict:
        """
        Return your configuration, as a dict

        :raise ConfigurationError: on invalid configuration
        """
        return {self.key: self.child.provide()}

    def __repr__(self) -> str:
        return '<%s>' % (self.__class__.__qualname__,)