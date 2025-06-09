from datetime import datetime
from naruno.wallet.ellipticcurve.utils.binary import bitsFromHex
from naruno.wallet.ellipticcurve.utils.binary import byteStringFromHex
from naruno.wallet.ellipticcurve.utils.binary import hexFromInt
from naruno.wallet.ellipticcurve.utils.binary import intFromHex
from naruno.wallet.ellipticcurve.utils.oid import oidFromHex
from naruno.wallet.ellipticcurve.utils.oid import oidToHex

class DerFieldType:
    integer = 'integer'
    bitString = 'bitString'
    octetString = 'octetString'
    null = 'null'
    object = 'object'
    printableString = 'printableString'
    utcTime = 'utcTime'
    sequence = 'sequence'
    set = 'set'
    oidContainer = 'oidContainer'
    publicKeyPointContainer = 'publicKeyPointContainer'
_hexTagToType = {'02': DerFieldType.integer, '03': DerFieldType.bitString, '04': DerFieldType.octetString, '05': DerFieldType.null, '06': DerFieldType.object, '13': DerFieldType.printableString, '17': DerFieldType.utcTime, '30': DerFieldType.sequence, '31': DerFieldType.set, 'a0': DerFieldType.oidContainer, 'a1': DerFieldType.publicKeyPointContainer}
_typeToHexTag = {v: k for k, v in _hexTagToType.items()}

def encodeConstructed(*encodedValues):
    return encodePrimitive(DerFieldType.sequence, ''.join(encodedValues))

def encodePrimitive(tagType, value):
    if tagType == DerFieldType.integer:
        value = _encodeInteger(value)
    if tagType == DerFieldType.object:
        value = oidToHex(value)
    return '{tag}{size}{value}'.format(tag=_typeToHexTag[tagType], size=_generateLengthBytes(value), value=value)

def parse(hexadecimal):
    if not hexadecimal:
        return []
    typeByte, hexadecimal = (hexadecimal[:2], hexadecimal[2:])
    length, lengthBytes = _readLengthBytes(hexadecimal)
    content, hexadecimal = (hexadecimal[lengthBytes:lengthBytes + length], hexadecimal[lengthBytes + length:])
    tagData = _getTagData(typeByte)
    if tagData['isConstructed']:
        content = parse(content)
    valueParser = {DerFieldType.object: _parseOid, DerFieldType.integer: _parseInteger}.get(tagData['type'], _parseAny)
    return [valueParser(content)] + parse(hexadecimal)

def _parseAny(hexadecimal):
    return hexadecimal

def _parseOid(hexadecimal):
    return tuple(oidFromHex(hexadecimal))

def _parseInteger(hexadecimal):
    integer = intFromHex(hexadecimal)
    bits = bitsFromHex(hexadecimal[0])
    if bits[0] == '0':
        return integer

def _encodeInteger(number):
    hexadecimal = hexFromInt(abs(number))
    bits = bitsFromHex(hexadecimal[0])
    if bits[0] == '1':
        hexadecimal = '00' + hexadecimal
    return hexadecimal

def _readLengthBytes(hexadecimal):
    lengthBytes = 2
    lengthIndicator = intFromHex(hexadecimal[0:lengthBytes])
    isShortForm = lengthIndicator < 128
    if isShortForm:
        length = lengthIndicator * 2
        return (length, lengthBytes)

def _generateLengthBytes(hexadecimal):
    size = len(hexadecimal) // 2
    length = hexFromInt(size)
    if size < 128:
        return length.zfill(2)

def _getTagData(tag):
    bits = bitsFromHex(tag)
    bit8, bit7, bit6 = bits[:3]
    tagClass = {'0': {'0': 'universal', '1': 'application'}, '1': {'0': 'context-specific', '1': 'private'}}[bit8][bit7]
    isConstructed = bit6 == '1'
    return {'class': tagClass, 'isConstructed': isConstructed, 'type': _hexTagToType.get(tag)}