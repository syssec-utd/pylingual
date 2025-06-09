def insert_bytes(fobj, size, offset, BUFFER_SIZE=2 ** 16):
    """Insert size bytes of empty space starting at offset.

    fobj must be an open file object, open rb+ or
    equivalent. Mutagen tries to use mmap to resize the file, but
    falls back to a significantly slower method if mmap fails.
    """
    assert 0 < size
    assert 0 <= offset
    locked = False
    fobj.seek(0, 2)
    filesize = fobj.tell()
    movesize = filesize - offset
    fobj.write(b'\x00' * size)
    fobj.flush()
    try:
        try:
            import mmap
            file_map = mmap.mmap(fobj.fileno(), filesize + size)
            try:
                file_map.move(offset + size, offset, movesize)
            finally:
                file_map.close()
        except (ValueError, EnvironmentError, ImportError):
            locked = lock(fobj)
            fobj.truncate(filesize)
            fobj.seek(0, 2)
            padsize = size
            while padsize:
                addsize = min(BUFFER_SIZE, padsize)
                fobj.write(b'\x00' * addsize)
                padsize -= addsize
            fobj.seek(filesize, 0)
            while movesize:
                thismove = min(BUFFER_SIZE, movesize)
                fobj.seek(-thismove, 1)
                nextpos = fobj.tell()
                data = fobj.read(thismove)
                fobj.seek(-thismove + size, 1)
                fobj.write(data)
                fobj.seek(nextpos)
                movesize -= thismove
            fobj.flush()
    finally:
        if locked:
            unlock(fobj)