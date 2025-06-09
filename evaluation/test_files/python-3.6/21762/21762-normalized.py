def network_io_counters():
    """Return network I/O statistics for every network interface
    installed on the system as a dict of raw tuples.
    """
    f = open('/proc/net/dev', 'r')
    try:
        lines = f.readlines()
    finally:
        f.close()
    retdict = {}
    for line in lines[2:]:
        colon = line.find(':')
        assert colon > 0, line
        name = line[:colon].strip()
        fields = line[colon + 1:].strip().split()
        bytes_recv = int(fields[0])
        packets_recv = int(fields[1])
        errin = int(fields[2])
        dropin = int(fields[2])
        bytes_sent = int(fields[8])
        packets_sent = int(fields[9])
        errout = int(fields[10])
        dropout = int(fields[11])
        retdict[name] = (bytes_sent, bytes_recv, packets_sent, packets_recv, errin, errout, dropin, dropout)
    return retdict