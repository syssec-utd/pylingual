from rift.ast.types import Expr
from rift.core import Entity
from rift.core.factory import Factory
from rift.core.utils import init_abstract_type
from rift.func.types.builder_base import _BuilderBase
from rift.func.types.cell_base import _CellBase
from rift.func.types.cont_base import _ContBase
from rift.func.types.dict_base import _DictBase
from rift.func.types.idict_base import _IDictBase
from rift.func.types.int_base import _IntBase
from rift.func.types.pfxdict_base import _PfxDictBase
from rift.func.types.slice_base import _SliceBase
from rift.func.types.string_base import _StringBase
from rift.func.types.udict_base import _UDictBase
from rift.util import type_id

class Int(_IntBase):
    __type_id__ = type_id('Int')

    def __init__(self, value, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.value = value
        if 'data' not in kwargs:
            self.data = Expr.const(value)

    @classmethod
    def abstract_init(cls, *args, **kwargs) -> 'Int':
        return cls(0, *args, **kwargs)

    @classmethod
    def type_name(cls) -> str:
        return 'int'

class HexInt(_IntBase):
    __type_id__ = type_id('HexInt')

    def __init__(self, value, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.value = value
        if 'data' not in kwargs:
            self.data = Expr.const(value)

    @classmethod
    def abstract_init(cls, *args, **kwargs) -> 'Int':
        return cls(0, *args, **kwargs)

    def _repr_(self):
        return hex(self.value)

    @classmethod
    def type_name(cls) -> str:
        return 'int'

class Slice(_SliceBase):
    __type_id__ = type_id('Slice')

    @classmethod
    def type_name(cls) -> str:
        return 'slice'

    def __mod__(self, other):
        assert isinstance(other, type)
        return other(self)

    def __rshift__(self, other):
        return other.__deserialize__(self)

class Cont(_ContBase):
    __type_id__ = type_id('Cont')

    @classmethod
    def type_name(cls) -> str:
        return 'cont'

class String(_StringBase):
    __type_id__ = type_id('String')

    @classmethod
    def type_name(cls) -> str:
        return 'string'

class Cell(_CellBase):
    __type_id__ = type_id('Cell')

    @classmethod
    def type_name(cls) -> str:
        return 'cell'

    def as_ref(self):
        from rift.types.ref import Ref
        return Ref[Cell](self)

class Dict(_DictBase):
    __type_id__ = type_id('Dict')

    @classmethod
    def type_name(cls) -> str:
        return 'cell'

class UDict(_UDictBase):
    __type_id__ = type_id('UDict')
    pass

class IDict(_IDictBase):
    __type_id__ = type_id('IDict')
    pass

class PfxDict(_PfxDictBase, Cell):
    __type_id__ = type_id('PfxDict')

    @classmethod
    def type_name(cls) -> str:
        return 'cell'

class Builder(_BuilderBase):
    __type_id__ = type_id('Builder')

    @classmethod
    def type_name(cls) -> str:
        return 'builder'

class Tensor(Entity, tuple):
    __type_id__ = type_id('Tensor')

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args)

    def __init__(self, *args, **kwargs):
        name = kwargs.pop('name', None)
        data = kwargs.pop('data', None)
        self.type_ = kwargs.pop('type_', None)
        super().__init__(data=data, name=name)

    def __iter__(self):
        if not self.type_:
            return super().__iter__()
        if hasattr(self, '__unpackable') and self.__unpackable:
            for _, tp in zip(range(self._unpack_len), self.type_.__args__):
                yield init_abstract_type(tp)

class Tuple(Entity):
    __type_id__ = type_id('Tuple')

    @classmethod
    def type_name(cls) -> str:
        return 'tuple'
Factory.register('Tensor', Tensor)
Factory.register('Tuple', Tuple)
Factory.register('Builder', Builder)
Factory.register('Dict', Dict)
Factory.register('UDict', UDict)
Factory.register('IDict', IDict)
Factory.register('PfxDict', PfxDict)
Factory.register('Slice', Slice)
Factory.register('Cell', Cell)
Factory.register('String', String)
Factory.register('Cont', Cont)
Factory.register('Int', Int)
Factory.register('HexInt', HexInt)