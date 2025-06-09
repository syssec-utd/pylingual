from io import BytesIO
from telectron.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from telectron.raw.core import TLObject
from telectron import raw
from typing import List, Optional, Any

class Game(TLObject):
    """This object is a constructor of the base type :obj:`~telectron.raw.base.Game`.

    Details:
        - Layer: ``145``
        - ID: ``BDF9653B``

    Parameters:
        id: ``int`` ``64-bit``
        access_hash: ``int`` ``64-bit``
        short_name: ``str``
        title: ``str``
        description: ``str``
        photo: :obj:`Photo <telectron.raw.base.Photo>`
        document (optional): :obj:`Document <telectron.raw.base.Document>`
    """
    __slots__: List[str] = ['id', 'access_hash', 'short_name', 'title', 'description', 'photo', 'document']
    ID = 3187238203
    QUALNAME = 'types.Game'

    def __init__(self, *, id: int, access_hash: int, short_name: str, title: str, description: str, photo: 'raw.base.Photo', document: 'raw.base.Document'=None) -> None:
        self.id = id
        self.access_hash = access_hash
        self.short_name = short_name
        self.title = title
        self.description = description
        self.photo = photo
        self.document = document

    @staticmethod
    def read(b: BytesIO, *args: Any) -> 'Game':
        flags = Int.read(b)
        id = Long.read(b)
        access_hash = Long.read(b)
        short_name = String.read(b)
        title = String.read(b)
        description = String.read(b)
        photo = TLObject.read(b)
        document = TLObject.read(b) if flags & 1 << 0 else None
        return Game(id=id, access_hash=access_hash, short_name=short_name, title=title, description=description, photo=photo, document=document)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))
        flags = 0
        flags |= 1 << 0 if self.document is not None else 0
        b.write(Int(flags))
        b.write(Long(self.id))
        b.write(Long(self.access_hash))
        b.write(String(self.short_name))
        b.write(String(self.title))
        b.write(String(self.description))
        b.write(self.photo.write())
        if self.document is not None:
            b.write(self.document.write())
        return b.getvalue()