from typing import Union
from telectron import raw
from telectron.raw.core import TLObject
CodeSettings = Union[raw.types.CodeSettings]

class CodeSettings:
    """This base type has 1 constructor available.

    Constructors:
        .. hlist::
            :columns: 2

            - :obj:`CodeSettings <telectron.raw.types.CodeSettings>`
    """
    QUALNAME = 'telectron.raw.base.CodeSettings'

    def __init__(self):
        raise TypeError('Base types can only be used for type checking purposes: you tried to use a base type instance as argument, but you need to instantiate one of its constructors instead. More info: https://docs.telectron.org/telegram/base/code-settings')