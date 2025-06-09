import sys
import ast as _ast
from typing import Any
PY38: bool = sys.version_info >= (3, 8)
PY310: bool = sys.version_info >= (3, 10)

class _AST:

    def __getattr__(self, name: str) -> Any:
        return getattr(_ast, name)
    if PY38:
        arguments = _ast.arguments
    else:

        @staticmethod
        def arguments(_, args, vararg, kwonlyargs, kw_defaults, kwarg, defaults):
            return _ast.arguments(args, vararg, kwonlyargs, kw_defaults, kwarg, defaults)
ast = _AST()
if sys.version_info >= (3, 10):
    from typing import Concatenate, ParamSpec, TypeAlias
else:
    from typing_extensions import Concatenate, ParamSpec, TypeAlias
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol
__all__ = ['PY38', 'PY310', 'ast', 'Protocol', 'Concatenate', 'ParamSpec', 'TypeAlias']