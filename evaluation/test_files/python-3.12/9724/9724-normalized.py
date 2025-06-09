def propagateClkRstn(obj):
    """
    Propagate "clk" clock and negative reset "rst_n" signal
    to all subcomponents
    """
    clk = obj.clk
    rst_n = obj.rst_n
    for u in obj._units:
        _tryConnect(clk, u, 'clk')
        _tryConnect(rst_n, u, 'rst_n')
        _tryConnect(~rst_n, u, 'rst')