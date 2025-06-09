def reduce(infile, outfile):
    """
    Reduce scored PyProphet file to minimum for global scoring
    """
    if outfile is None:
        outfile = infile
    else:
        outfile = outfile
    reduce_osw(infile, outfile)