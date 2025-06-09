from abc import abstractmethod, ABC
from typing import Dict, Any, Callable, Tuple
from torch.nn import Module
from .util import F

class NekoModule(ABC, Module, F):
    """
    The module base of tensorneko. This NekoModule is inherited from :class:`~torch.nn.Module`
    and also support the ``tensorneko.util.fp`` pipe operation.

    Examples::

        # A three-layer-mlp with layer 16 -> 128 -> 1
        class ThreeLayerMLP(NekoModule):

            def __init__(self):
                super().__init__()
                self.linear0 = Linear(16, 128, build_activation=ReLU)
                self.linear1 = Linear(128, 1)

            def forward(self, x):
                f = self.linear0 >> self.linear1
                return f(x)

    """

    def __init__(self):
        super().__init__()
        self.f: Callable[[Tuple[Any, ...], Dict[str, Any]], Any] = self._call_impl

    @abstractmethod
    def forward(self, *args, **kwargs):
        ...

    @classmethod
    def __compose(cls, f, g):
        return F(lambda *args, **kwargs: f(g(*args, **kwargs)))

    def __ensure_callable(self, f):
        return F(*f) if isinstance(f, tuple) else f

    def __rshift__(self, g):
        """Overload << operator for F instances"""
        return self.__class__.__compose(self.__ensure_callable(g), self.f)

    def __lshift__(self, g):
        """Overload >> operator for F instances"""
        return self.__class__.__compose(self.f, self.__ensure_callable(g))