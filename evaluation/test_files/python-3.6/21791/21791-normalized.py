def set_trace():
    """Call pdb.set_trace in the calling frame, first restoring
    sys.stdout to the real output stream. Note that sys.stdout is NOT
    reset to whatever it was before the call once pdb is done!
    """
    import pdb
    import sys
    stdout = sys.stdout
    sys.stdout = sys.__stdout__
    pdb.Pdb().set_trace(sys._getframe().f_back)