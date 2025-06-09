"""
**Beartype validator text utilities** (i.e., callables performing low-level
string-centric operations on behalf of higher-level beartype validators).

This private submodule is *not* intended for importation by downstream callers.
"""
from beartype.roar._roarexc import _BeartypeValeUtilException
from beartype.typing import Optional
from beartype._cave._cavemap import NoneTypeOr

def format_diagnosis_line(validator_repr: str, indent_level_outer: str, indent_level_inner: str, is_obj_valid: Optional[bool]=None) -> str:
    """
    Single line of a larger human-readable **validation failure diagnosis**
    (i.e., substring describing how an arbitrary object either satisfies *or*
    violates an arbitrary validator), formatted with the passed indentation
    level and boolean value.

    Parameters
    ----------
    validator_repr : str
        **Validator representation** (i.e., unformatted single line of a larger
        diagnosis report to be formatted by this function).
    indent_level_outer : str
        **Outermost indentation level** (i.e., zero or more adjacent spaces
        prefixing each line of the returned substring).
    indent_level_inner : str
        **Innermost indentation level** (i.e., zero or more adjacent spaces
        delimiting the human-readable representation of the tri-state boolean
        and validator representation in the returned substring).
    is_obj_valid : Optional[bool]
        Tri-state boolean such that:

        * If ``True``, that arbitrary object satisfies the beartype validator
          described by this specific line.
        * If ``False``, that arbitrary object violates the beartype validator
          described by this specific line.
        * If ``None``, this specific line is entirely syntactic (e.g., a
          suffixing ")" delimiter) isolated to its own discrete line for
          readability. In this case, this line does *not* describe how an
          arbitrary object either satisfies *or* violates an arbitrary
          validator.

        Defaults to ``None``.

    Returns
    ----------
    str
        This diagnosis line formatted with this indentation level.

    Raises
    ----------
    _BeartypeValeUtilException
        If ``is_obj_valid`` is *not* a **tri-state boolean** (i.e., either
        ``True``, ``False``, or ``None``).
    """
    assert isinstance(validator_repr, str), f'{repr(validator_repr)} not string.'
    assert isinstance(indent_level_outer, str), f'{repr(indent_level_outer)} not string.'
    assert isinstance(indent_level_inner, str), f'{repr(indent_level_inner)} not string.'
    if not isinstance(is_obj_valid, NoneTypeOr[bool]):
        raise _BeartypeValeUtilException(f'beartype.vale._valeutiltext.format_diagnosis_line() parameter "is_obj_valid" value {repr(is_obj_valid)} not tri-state boolean for validator representation: {validator_repr}')
    is_obj_valid_str = ''
    if is_obj_valid is True:
        is_obj_valid_str = ' True == '
    elif is_obj_valid is False:
        is_obj_valid_str = 'False == '
    else:
        is_obj_valid_str = '         '
    return f'{indent_level_outer}{is_obj_valid_str}{indent_level_inner}{validator_repr}'