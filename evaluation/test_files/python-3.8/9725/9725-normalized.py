def propagateClkRst(obj):
    """
    Propagate "clk" clock and reset "rst" signal to all subcomponents
    """
    clk = obj.clk
    rst = obj.rst
    for u in obj._units:
        _tryConnect(clk, u, 'clk')
        _tryConnect(~rst, u, 'rst_n')
        _tryConnect(rst, u, 'rst')