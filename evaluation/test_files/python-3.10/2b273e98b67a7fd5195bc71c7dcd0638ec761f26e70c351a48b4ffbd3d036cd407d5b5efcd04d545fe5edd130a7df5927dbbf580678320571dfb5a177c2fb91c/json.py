from __future__ import annotations
import typing
import json
from ..base import BaseFileIterable

class JSONIterable(BaseFileIterable):

    def __init__(self, filename: str=None, stream: typing.IO=None, codec: BaseCodec=None, mode='r', tagname: str=None):
        super(JSONIterable, self).__init__(filename, stream, codec=codec, mode=mode, binary=False)
        self.tagname = tagname
        self.reset()
        pass

    def reset(self):
        super(JSONIterable, self).reset()
        self.pos = 0
        self.data = json.load(self.fobj)
        if self.tagname:
            self.data = self.data[self.tagname]
        self.total = len(self.data)

    @staticmethod
    def id() -> str:
        return 'json'

    @staticmethod
    def is_flatonly() -> bool:
        return False

    def read(self, skip_empty: bool=False) -> dict:
        """Read single JSON record"""
        if self.pos >= self.total:
            raise StopIteration
        row = self.data[self.pos]
        self.pos += 1
        return row

    def read_bulk(self, num: int=10) -> list[dict]:
        """Read bulk JSON records"""
        chunk = []
        for n in range(0, num):
            chunk.append(self.read())
        return chunk