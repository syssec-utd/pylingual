from typing import Optional, Union
from dataclasses import dataclass
import re
from sciform.modes import FillMode, FormatMode, PrecMode, SignMode, GroupingSeparator, DecimalSeparator

@dataclass(frozen=True)
class FormatSpec:
    fill_mode: FillMode
    sign_mode: SignMode
    alternate_mode: bool
    top_dig_place: int
    thousands_separator: GroupingSeparator
    decimal_separator: DecimalSeparator
    thousandths_separator: GroupingSeparator
    prec_mode: PrecMode
    prec: Optional[int]
    format_mode: FormatMode
    capital_exp_char: bool
    percent_mode: bool
    exp: Optional[int]
    prefix_mode: bool
DEFAULT_FORMAT_SPEC = FormatSpec(fill_mode=FillMode.SPACE, sign_mode=SignMode.NEGATIVE, alternate_mode=False, top_dig_place=0, thousands_separator=GroupingSeparator.NO_GROUPING, decimal_separator=DecimalSeparator.POINT, thousandths_separator=GroupingSeparator.NO_GROUPING, prec_mode=PrecMode.SIG_FIG, prec=None, format_mode=FormatMode.FIXEDPOINT, capital_exp_char=False, percent_mode=False, exp=None, prefix_mode=False)

def get_format_spec(*, fill_mode: Union[str, FillMode]=None, sign_mode: Union[str, SignMode]=None, alternate_mode: bool=None, top_dig_place: int=None, thousands_separator: Union[str, GroupingSeparator]=None, decimal_separator: Union[str, DecimalSeparator]=None, thousandths_separator: Union[str, GroupingSeparator]=None, prec_mode: Union[str, PrecMode]=None, prec: int=None, format_mode: Union[str, FormatMode]=None, capital_exp_char: bool=None, percent_mode: bool=None, exp: int=None, prefix_mode: bool=None, default_fmt_spec: Optional[FormatSpec]=None):
    if default_fmt_spec is None:
        default_fmt_spec = DEFAULT_FORMAT_SPEC
    if fill_mode is None:
        fill_mode = default_fmt_spec.fill_mode
    elif isinstance(fill_mode, str):
        fill_mode = FillMode.from_flag(fill_mode)
    if sign_mode is None:
        sign_mode = default_fmt_spec.sign_mode
    elif isinstance(sign_mode, str):
        sign_mode = SignMode.from_flag(sign_mode)
    if alternate_mode is None:
        alternate_mode = default_fmt_spec.alternate_mode
    if top_dig_place is None:
        top_dig_place = default_fmt_spec.top_dig_place
    if thousands_separator is None:
        thousands_separator = default_fmt_spec.thousands_separator
    elif isinstance(thousands_separator, str):
        thousands_separator = GroupingSeparator.from_flag(thousands_separator)
    if decimal_separator is None:
        decimal_separator = default_fmt_spec.decimal_separator
    elif isinstance(decimal_separator, str):
        decimal_separator = DecimalSeparator.from_flag(decimal_separator)
    if thousandths_separator is None:
        thousandths_separator = default_fmt_spec.thousandths_separator
    elif isinstance(thousandths_separator, str):
        thousandths_separator = GroupingSeparator.from_flag(thousandths_separator)
    if prec_mode is None:
        prec_mode = default_fmt_spec.prec_mode
    elif isinstance(prec_mode, str):
        prec_mode = PrecMode.from_flag(prec_mode)
    if prec is None:
        prec = default_fmt_spec.prec
    if prec_mode is PrecMode.SIG_FIG:
        if isinstance(prec, int):
            if prec <= 0:
                raise ValueError(f'Precision must be >= 1 for sig fig format mode, not {prec}.')
    if format_mode is None:
        format_mode = default_fmt_spec.format_mode
    elif isinstance(format_mode, str):
        capital_exp_char = format_mode.isupper()
        percent_mode = format_mode == '%'
        format_mode = FormatMode.from_flag(format_mode)
    if capital_exp_char is None:
        capital_exp_char = default_fmt_spec.capital_exp_char
    if percent_mode is None:
        percent_mode = default_fmt_spec.percent_mode
    if percent_mode and format_mode is not FormatMode.FIXEDPOINT:
        raise ValueError(f'percent mode only valid in fixed point format mode, not {format_mode}.')
    if exp is None:
        exp = default_fmt_spec.exp
    if prefix_mode is None:
        prefix_mode = default_fmt_spec.prefix_mode
    return FormatSpec(fill_mode=fill_mode, sign_mode=sign_mode, alternate_mode=alternate_mode, top_dig_place=top_dig_place, thousands_separator=thousands_separator, decimal_separator=decimal_separator, thousandths_separator=thousandths_separator, prec_mode=prec_mode, prec=prec, format_mode=format_mode, capital_exp_char=capital_exp_char, percent_mode=percent_mode, exp=exp, prefix_mode=prefix_mode)
pattern = re.compile('^\n                         (?:(?P<fill>[ 0])=)?\n                         (?P<sign>[+\\- ])?\n                         (?P<alternate>\\#)?                         \n                         (?P<top_dig_place>\\d+)?\n                         (?P<thousands_separator>[n,.s_])?                     \n                         (?P<decimal_separator>[.,])?            \n                         (?P<thousandths_separator>[ns_])?                  \n                         (?:(?P<prec_mode>[.!])(?P<prec>-?\\d+))?\n                         (?P<format_mode>[fF%eErRbB])?\n                         (?P<exp>[+-]\\d+)?\n                         (?P<prefix_mode>p)?\n                         $', re.VERBOSE)

def parse_format_spec(fmt: str, default_fmt_spec: Optional[FormatSpec]=None) -> FormatSpec:
    match = pattern.match(fmt)
    if match is None:
        raise ValueError(f"Invalid format specifier: '{fmt}'")
    fill = match.group('fill')
    sign_mode = match.group('sign')
    alternate_mode = match.group('alternate')
    top_dig_place = match.group('top_dig_place')
    if top_dig_place is not None:
        top_dig_place = int(top_dig_place)
    thousands_separator = match.group('thousands_separator')
    decimal_separator = match.group('decimal_separator')
    thousandths_separator = match.group('thousandths_separator')
    prec_mode = match.group('prec_mode')
    prec = match.group('prec')
    if prec is not None:
        prec = int(prec)
    format_mode = match.group('format_mode')
    if format_mode is not None:
        capital_exp_char = format_mode.isupper()
        percent_mode = format_mode == '%'
    else:
        capital_exp_char = None
        percent_mode = None
    exp = match.group('exp')
    if exp is not None:
        exp = int(exp)
    prefix_mode = match.group('prefix_mode')
    return get_format_spec(fill_mode=fill, sign_mode=sign_mode, alternate_mode=alternate_mode, top_dig_place=top_dig_place, thousands_separator=thousands_separator, decimal_separator=decimal_separator, thousandths_separator=thousandths_separator, prec_mode=prec_mode, prec=prec, format_mode=format_mode, capital_exp_char=capital_exp_char, percent_mode=percent_mode, exp=exp, prefix_mode=prefix_mode, default_fmt_spec=default_fmt_spec)