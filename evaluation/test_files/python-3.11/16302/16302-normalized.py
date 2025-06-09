def unpack(wheelfile, dest='.'):
    """Unpack a wheel.

    Wheel content will be unpacked to {dest}/{name}-{ver}, where {name}
    is the package name and {ver} its version.

    :param wheelfile: The path to the wheel.
    :param dest: Destination directory (default to current directory).
    """
    wf = WheelFile(wheelfile)
    namever = wf.parsed_filename.group('namever')
    destination = os.path.join(dest, namever)
    sys.stderr.write('Unpacking to: %s\n' % destination)
    wf.zipfile.extractall(destination)
    wf.zipfile.close()