def rehash(path, algo='sha256', blocksize=1 << 20):
    """Return (hash, length) for path using hashlib.new(algo)"""
    h = hashlib.new(algo)
    length = 0
    with open(path, 'rb') as f:
        block = f.read(blocksize)
        while block:
            length += len(block)
            h.update(block)
            block = f.read(blocksize)
    digest = 'sha256=' + urlsafe_b64encode(h.digest()).decode('latin1').rstrip('=')
    return (digest, length)