def unsign(wheelfile):
    """
    Remove RECORD.jws from a wheel by truncating the zip file.
    
    RECORD.jws must be at the end of the archive. The zip file must be an 
    ordinary archive, with the compressed files and the directory in the same 
    order, and without any non-zip content after the truncation point.
    """
    import wheel.install
    vzf = wheel.install.VerifyingZipFile(wheelfile, 'a')
    info = vzf.infolist()
    if not (len(info) and info[-1].filename.endswith('/RECORD.jws')):
        raise WheelError('RECORD.jws not found at end of archive.')
    vzf.pop()
    vzf.close()