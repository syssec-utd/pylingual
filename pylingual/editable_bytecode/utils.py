import re
from datetime import datetime
from struct import pack

from xdis.cross_types import LongTypeForPython3, UnicodeForPython3
import xdis.marsh as marshal
from xdis import iscode
from xdis.codetype import to_portable

from pylingual.utils.version import PythonVersion


def unwrap(x):
    """
    Turns xdis-specific types back into Python types
    """
    if isinstance(x, UnicodeForPython3):
        return str(x)
    if isinstance(x, LongTypeForPython3):
        return int(x)
    if isinstance(x, tuple):
        return tuple(unwrap(e) for e in x)
    if isinstance(x, list):
        return [unwrap(e) for e in x]
    return x


# every code attribute except filename and line info
SAME_CODE_ATTRS = ("co_argcount", "co_posonlyargcount", "co_kwonlyargcount", "co_nlocals", "co_stacksize", "co_flags", "co_code", "co_names", "co_varnames", "co_freevars", "co_cellvars", "co_name", "co_qualname", "co_exceptiontable")


def same_const(a, b) -> bool:
    if iscode(a) or iscode(b):
        return iscode(a) and iscode(b) and same_code(a, b)
    if type(a) is not type(b):
        return False
    if isinstance(a, tuple):
        return len(a) == len(b) and all(same_const(x, y) for x, y in zip(a, b))
    if isinstance(a, frozenset):
        return sorted(map(repr, a)) == sorted(map(repr, b))
    if isinstance(a, (float, complex)):
        # nan never compares equal and -0.0 should stay distinct
        return a == b and repr(a) == repr(b)
    return a == b


def same_code(a, b) -> bool:
    """
    Checks if two code objects are identical, ignoring filenames and line info
    """
    if a is b:
        return True
    if any(getattr(a, attr, None) != getattr(b, attr, None) for attr in SAME_CODE_ATTRS):
        return False
    return len(a.co_consts) == len(b.co_consts) and all(same_const(x, y) for x, y in zip(a.co_consts, b.co_consts))


def line_shift(a, b) -> int | None:
    """
    Gets how far every line moved between two code objects that are the same apart from line info, or None if the lines changed otherwise
    """
    delta = b.co_firstlineno - a.co_firstlineno
    stack = [(a, b)]
    while stack:
        x, y = stack.pop()
        # co_linetable replaced co_lnotab in 3.10
        table = "co_linetable" if hasattr(x, "co_linetable") else "co_lnotab"
        if y.co_firstlineno - x.co_firstlineno != delta or getattr(x, table, None) != getattr(y, table, None):
            return None
        stack.extend((c, d) for c, d in zip(x.co_consts, y.co_consts) if iscode(c))
    return delta


def codeobj_replace(codeobj, **kwargs):
    if hasattr(codeobj, "replace"):
        return codeobj.replace(**kwargs)
    else:
        all_kwargs = {key: getattr(codeobj, key) for key in dir(codeobj) if key.startswith("co_")}
        all_kwargs.update(kwargs)

        return to_portable(**all_kwargs)


def write_pyc(f, codeobj, version, magic_int, timestamp=None, filesize=0):
    """
    Mostly taken from xdis.load's write_bytecode_file function.
    Does not close the provided fileobject upon return.
    """

    version = PythonVersion(version)
    if version >= (3, 0):
        f.write(pack("<Hcc", magic_int, b"\r", b"\n"))
        if version >= (3, 7):  # pep552 bytes
            f.write(pack("<I", 0))  # pep552 bytes
    else:
        f.write(pack("<Hcc", magic_int, b"\r", b"\n"))

    if timestamp is not None:
        if isinstance(timestamp, datetime):
            f.write(pack("<I", int(timestamp.timestamp())))
        elif isinstance(timestamp, int):
            f.write(pack("<I", timestamp))
    else:
        f.write(pack("<I", int(datetime.now().timestamp())))

    if version >= (3, 3):
        # In Python 3.3+, these 4 bytes are the size of the source code_obj file (mod 2^32)
        f.write(pack("<I", filesize))

    f.write(marshal.dumps(codeobj, python_version=version.as_tuple()))


def find_loadconst_codeobj_from_makefunc(makefunc_inst):
    """Finds the LOAD_CONST that would likely load the corresponding codeobj when MAKE_FUNCTION is called"""
    bytecode = makefunc_inst.bytecode
    idx = list(bytecode).index(makefunc_inst)

    for inst in reversed(bytecode[:idx]):
        if inst.opcode == bytecode.opcode.LOAD_CONST:
            if iscode(inst.argval):
                return inst


# finds non "alphanumeric-ish" characters
non_alphanumeric = re.compile(r"[^A-Za-z0-9_\-.]+")

# Lists of special names for various types of comprehensions and expressions with code objects associated with them.
# This is used partially as a heuristic to figure out
comprehension_names = (
    "<genexpr>",
    "<lambda>",
    "<listcomp>",
    "<setcomp>",
    "<dictcomp>",
)
