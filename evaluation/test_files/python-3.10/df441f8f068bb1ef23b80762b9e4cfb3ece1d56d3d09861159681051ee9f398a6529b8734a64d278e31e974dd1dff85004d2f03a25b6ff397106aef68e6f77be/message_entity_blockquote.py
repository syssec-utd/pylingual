from io import BytesIO
from telectron.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from telectron.raw.core import TLObject
from telectron import raw
from typing import List, Optional, Any

class MessageEntityBlockquote(TLObject):
    """This object is a constructor of the base type :obj:`~telectron.raw.base.MessageEntity`.

    Details:
        - Layer: ``145``
        - ID: ``20DF5D0``

    Parameters:
        offset: ``int`` ``32-bit``
        length: ``int`` ``32-bit``
    """
    __slots__: List[str] = ['offset', 'length']
    ID = 34469328
    QUALNAME = 'types.MessageEntityBlockquote'

    def __init__(self, *, offset: int, length: int) -> None:
        self.offset = offset
        self.length = length

    @staticmethod
    def read(b: BytesIO, *args: Any) -> 'MessageEntityBlockquote':
        offset = Int.read(b)
        length = Int.read(b)
        return MessageEntityBlockquote(offset=offset, length=length)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))
        b.write(Int(self.offset))
        b.write(Int(self.length))
        return b.getvalue()