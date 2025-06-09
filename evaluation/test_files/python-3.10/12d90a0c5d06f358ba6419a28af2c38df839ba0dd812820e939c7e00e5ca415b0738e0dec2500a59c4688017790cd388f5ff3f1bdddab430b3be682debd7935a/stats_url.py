from io import BytesIO
from telectron.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from telectron.raw.core import TLObject
from telectron import raw
from typing import List, Optional, Any

class StatsURL(TLObject):
    """This object is a constructor of the base type :obj:`~telectron.raw.base.StatsURL`.

    Details:
        - Layer: ``145``
        - ID: ``47A971E0``

    Parameters:
        url: ``str``
    """
    __slots__: List[str] = ['url']
    ID = 1202287072
    QUALNAME = 'types.StatsURL'

    def __init__(self, *, url: str) -> None:
        self.url = url

    @staticmethod
    def read(b: BytesIO, *args: Any) -> 'StatsURL':
        url = String.read(b)
        return StatsURL(url=url)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))
        b.write(String(self.url))
        return b.getvalue()