from dataclasses import dataclass

@dataclass(frozen=True)
class Colors:
    BLACK = '\x1b[0;30m'
    RED = '\x1b[0;31m'
    GREEN = '\x1b[0;32m'
    BROWN = '\x1b[0;33m'
    BLUE = '\x1b[0;34m'
    PURPLE = '\x1b[0;35m'
    CYAN = '\x1b[0;36m'
    GREY = '\x1b[0;37m'
    DARK_GREY = '\x1b[1;30m'
    LIGHT_RED = '\x1b[1;31m'
    LIGHT_GREEN = '\x1b[1;32m'
    YELLOW = '\x1b[1;33m'
    LIGHT_BLUE = '\x1b[1;34m'
    LIGHT_PURPLE = '\x1b[1;35m'
    LIGHT_CYAN = '\x1b[1;36m'
    WHITE = '\x1b[1;37m'
    RESET = '\x1b[0m'
colors = Colors()