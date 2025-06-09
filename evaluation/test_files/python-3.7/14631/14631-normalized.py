def encode(self):
    """
        Encode and store a PUBLISH control packet.
        @raise e: C{ValueError} if encoded topic string exceeds 65535 bytes.
        @raise e: C{ValueError} if encoded packet size exceeds 268435455 bytes.
        @raise e: C{TypeError} if C{data} is not a string, bytearray, int, boolean or float.
        """
    header = bytearray(1)
    varHeader = bytearray()
    payload = bytearray()
    if self.qos:
        header[0] = 48 | self.retain | self.qos << 1 | self.dup << 3
        varHeader.extend(encodeString(self.topic))
        varHeader.extend(encode16Int(self.msgId))
    else:
        header[0] = 48 | self.retain
        varHeader.extend(encodeString(self.topic))
    if isinstance(self.payload, bytearray):
        payload.extend(self.payload)
    elif isinstance(self.payload, str):
        payload.extend(bytearray(self.payload, encoding='utf-8'))
    else:
        raise PayloadTypeError(type(self.payload))
    totalLen = len(varHeader) + len(payload)
    if totalLen > 268435455:
        raise PayloadValueError(totalLen)
    header.extend(encodeLength(totalLen))
    header.extend(varHeader)
    header.extend(payload)
    self.encoded = header
    return str(header) if PY2 else bytes(header)