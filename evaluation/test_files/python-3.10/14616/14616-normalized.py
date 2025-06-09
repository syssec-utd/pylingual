def encodeString(string):
    """
    Encode an UTF-8 string into MQTT format. 
    Returns a bytearray
    """
    encoded = bytearray(2)
    encoded.extend(bytearray(string, encoding='utf-8'))
    l = len(encoded) - 2
    if l > 65535:
        raise StringValueError(l)
    encoded[0] = l >> 8
    encoded[1] = l & 255
    return encoded