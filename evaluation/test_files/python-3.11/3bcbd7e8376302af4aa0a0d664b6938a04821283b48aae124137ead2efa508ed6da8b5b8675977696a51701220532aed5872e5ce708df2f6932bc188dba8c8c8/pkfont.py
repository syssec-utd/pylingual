"""
monobit.formats.pkfont - TeX packed font font files

(c) 2023 Rob Hagemans
licence: https://opensource.org/licenses/MIT
"""
import logging
from itertools import count
from ..storage import loaders, savers
from ..font import Font
from ..glyph import Glyph
from ..raster import Raster
from .. import struct
from ..struct import big_endian as be, bitfield, sizeof
from ..binary import ceildiv, align
from ..properties import Props
from ..magic import Regex

@loaders.register(name='pkfont', magic=(b'\xf7Y',), patterns=(Regex('.+\\.\\d+pk'),))
def load_pkfont(instream):
    """Load fonts from a METAFONT/TeX PKFONT."""
    return _load_pkfont(instream)
_PK_PRE0 = be.Struct(command='uint8', i='uint8', k='uint8')
_PK_PRE1 = be.Struct(ds='uint32', cs='uint32', hppp='uint32', vppp='uint32')

def _read_preamble(instream):
    """Read a pk_pre preamble command."""
    preamble0 = _PK_PRE0.read_from(instream)
    name = instream.read(preamble0.k)
    preamble1 = _PK_PRE1.read_from(instream)
    return Props(**vars(preamble0), x=name, **vars(preamble1))

def _read_command(command, instream):
    """Read a command."""
    if command == 240:
        k = int(be.uint8.read_from(instream))
        return instream.read(k)
    elif command == 241:
        k = int(be.uint16.read_from(instream))
        return instream.read(k)
    elif command == 242:
        kbytes = instream.read(3)
        k = int.from_bytes(kbytes, 'big')
        return instream.read(k)
    elif command == 243:
        k = int(be.uint32.read_from(instream))
        return instream.read(k)
    elif command == 244:
        y = int(be.uint32.read_from(instream))
        return y
    elif command == 245:
        instream.read()
        return None
    elif command == 246:
        return None
    elif command == 247:
        raise ValueError('Preamble not expected here')
    raise ValueError('Invalid command %d', command)
_CHAR_FLAG = be.Struct(dyn_f=bitfield('uint8', 4), ink_run=bitfield('uint8', 1), two_byte=bitfield('uint8', 1), prepend=bitfield('uint8', 2))
_CHAR_SHORT = be.Struct(pl='uint8', cc='uint8', tfm=be.uint8 * 3, dx='uint8', w='uint8', h='uint8', hoff='int8', voff='int8')
_CHAR_EXTENDED = be.Struct(pl='uint16', cc='uint8', tfm=be.uint8 * 3, dx='uint16', w='uint16', h='uint16', hoff='int16', voff='int16')
_CHAR_LONG = be.Struct(pl='uint32', cc='uint32', tfm=be.uint8 * 4, dx='uint32', dy='uint32', w='uint32', h='uint32', hoff='int32', voff='int32')

def _read_chardef(first, instream):
    """Read a character definition."""
    flag = _CHAR_FLAG.from_bytes(first)
    if flag.two_byte == 1 and flag.prepend == 3:
        chardef = _CHAR_LONG.read_from(instream)
        packet_length = chardef.pl
        tfm_offset = 8
        denominator = 2 ** 16
    elif flag.two_byte == 1:
        chardef = _CHAR_EXTENDED.read_from(instream)
        packet_length = flag.prepend * 65536 + chardef.pl
        tfm_offset = 3
        denominator = 1
    else:
        chardef = _CHAR_SHORT.read_from(instream)
        packet_length = flag.prepend * 256 + chardef.pl
        tfm_offset = 2
        denominator = 1
    payload_size = packet_length + tfm_offset - sizeof(chardef)
    payload = instream.read(payload_size)
    if len(payload) != payload_size:
        logging.warning('Raster data truncated: %d < %d', len(payload), payload_size)
    char = Props(**vars(flag), **vars(chardef), denominator=denominator, raster_data=payload)
    return char

def _convert_char(char):
    """Convert pkfont character definition to glyph."""
    if char.dyn_f == 14:
        raster = Raster.from_bytes(char.raster_data, stride=char.w, width=char.w, align='bit')
    else:
        bitmap = _unpack_bits(char)
        raster = Raster.from_vector(bitmap, stride=char.w)
    raster = raster.crop(bottom=max(0, raster.height - char.h))
    props = dict(codepoint=char.cc, left_bearing=-char.hoff, shift_up=char.voff - raster.height + 1, right_bearing=char.dx // char.denominator - char.w + char.hoff)
    return Glyph(raster, **props)

def _unpack_bits(char):
    """Unpack a packed character definition."""
    iternyb = _iter_nybbles(char.raster_data)
    repeat = 0
    bitmap = []
    colour = bool(char.ink_run)
    while True:
        try:
            run, new_repeat = _pk_packed_num(iternyb, char.dyn_f)
            if new_repeat is not None:
                repeat = new_repeat
        except StopIteration as e:
            break
        row_remaining = char.w - len(bitmap) % char.w
        if run >= row_remaining:
            bitmap.extend([colour] * row_remaining)
            run -= row_remaining
            bitmap.extend(bitmap[-char.w:] * repeat)
            repeat = 0
        bitmap.extend([colour] * run)
        colour = not colour
    return bitmap

def _iter_nybbles(bytestr):
    """Iterate over a bytes string in 4-bit steps (big-endian)."""
    for byte in bytestr:
        hi, lo = divmod(byte, 16)
        yield hi
        yield lo

def _pk_packed_num(iternyb, dyn_f):
    """
    Read a run number or repeat count.
    returns a tuple run, repeat
    """
    i = next(iternyb)
    if i < 14:
        if i == 0:
            j = 0
            while j == 0:
                j = next(iternyb)
                i += 1
            while i > 0:
                j = j * 16 + next(iternyb)
                i -= 1
            run = j - 15 + (13 - dyn_f) * 16 + dyn_f
        elif i <= dyn_f:
            run = i
        else:
            get_nyb = next(iternyb)
            run = (i - dyn_f - 1) * 16 + get_nyb + dyn_f + 1
        return (run, None)
    if i == 14:
        repeat, should_be_none = _pk_packed_num(iternyb, dyn_f)
        if should_be_none is not None:
            logging.warning('Duplicate repeat count')
    else:
        repeat = 1
    run, should_be_none = _pk_packed_num(iternyb, dyn_f)
    if should_be_none is not None:
        logging.warning('Duplicate repeat count')
    return (run, repeat)

def _load_pkfont(instream):
    """Load fonts from a METAFONT/TeX PKFONT."""
    preamble = _read_preamble(instream)
    chars = []
    specials = []
    while True:
        command = instream.read(1)
        if not command:
            break
        if ord(command) >= 240:
            special = _read_command(ord(command), instream)
            specials.append(special)
        else:
            char = _read_chardef(command, instream)
            chars.append(char)
    glyphs = tuple((_convert_char(_char) for _char in chars))
    return Font(glyphs)