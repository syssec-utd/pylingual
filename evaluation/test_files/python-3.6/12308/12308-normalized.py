def aes_decrypt(key, stdin, chunk_size=65536):
    """
    Generator that decrypts a content stream using AES 256 in CBC
    mode.

    :param key: Any string to use as the decryption key.
    :param stdin: Where to read the encrypted data from.
    :param chunk_size: Largest amount to read at once.
    """
    if not AES256CBC_Support:
        raise Exception('AES256CBC not supported; likely pycrypto is not installed')
    key = hashlib.sha256(key).digest()
    chunk_size = max(16, chunk_size >> 4 << 4)
    iv = stdin.read(16)
    while len(iv) < 16:
        chunk = stdin.read(16 - len(iv))
        if not chunk:
            raise IOError('EOF reading IV')
    decryptor = Crypto.Cipher.AES.new(key, Crypto.Cipher.AES.MODE_CBC, iv)
    data = ''
    while True:
        chunk = stdin.read(chunk_size)
        if not chunk:
            if len(data) != 16:
                raise IOError('EOF reading encrypted stream')
            data = decryptor.decrypt(data)
            trailing = ord(data[-1])
            if trailing > 15:
                raise IOError('EOF reading encrypted stream or trailing value corrupted %s' % trailing)
            yield data[:trailing]
            break
        data += chunk
        if len(data) > 16:
            trailing = len(data) % 16 or 16
            yield decryptor.decrypt(data[:-trailing])
            data = data[-trailing:]