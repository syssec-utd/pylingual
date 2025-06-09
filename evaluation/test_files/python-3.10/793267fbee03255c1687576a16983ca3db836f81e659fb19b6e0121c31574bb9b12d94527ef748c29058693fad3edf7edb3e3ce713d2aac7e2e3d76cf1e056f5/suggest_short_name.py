from io import BytesIO
from telectron.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from telectron.raw.core import TLObject
from telectron import raw
from typing import List, Optional, Any

class SuggestShortName(TLObject):
    """Telegram API method.

    Details:
        - Layer: ``145``
        - ID: ``4DAFC503``

    Parameters:
        title: ``str``

    Returns:
        :obj:`stickers.SuggestedShortName <telectron.raw.base.stickers.SuggestedShortName>`
    """
    __slots__: List[str] = ['title']
    ID = 1303364867
    QUALNAME = 'functions.stickers.SuggestShortName'

    def __init__(self, *, title: str) -> None:
        self.title = title

    @staticmethod
    def read(b: BytesIO, *args: Any) -> 'SuggestShortName':
        title = String.read(b)
        return SuggestShortName(title=title)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))
        b.write(String(self.title))
        return b.getvalue()