def _lazysecret(secret, blocksize=32, padding='}'):
    """Pads secret if not legal AES block size (16, 24, 32)"""
    if not len(secret) in (16, 24, 32):
        return secret + (blocksize - len(secret)) * padding
    return secret