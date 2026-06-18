from __future__ import annotations

from collections import defaultdict

from .segment import Recovery, Segment, INDENT


_strategies: dict[int, list] = defaultdict(list)


def register_recovery_strategy(priority: int):
    def decorator(func):
        _strategies[priority].append(func)
        return func
    return decorator


def get_strategies() -> list:
    result = []
    for priority in sorted(_strategies.keys()):
        result.extend(_strategies[priority])
    return result


def recover(seg: Segment, indent: int = 0) -> Recovery:
    for strategy in get_strategies():
        result = strategy(seg, indent)
        if result is not None:
            return result
    return Recovery("", False)


from . import strategies  # noqa: E402,F401  — trigger strategy registration