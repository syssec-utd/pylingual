def _parse_receive(incomming):
    """Parse received response.

    Parameters
    ----------
    incomming : bytes string
        Incomming bytes from socket server.

    Returns
    -------
    list of OrderedDict
        Received message as a list of OrderedDict.

    """
    debug(b'< ' + incomming)
    incomming = incomming.rstrip(b'\x00')
    msgs = incomming.splitlines()
    return [bytes_as_dict(msg) for msg in msgs]