def backpropagate(infile, outfile, apply_scores):
    """
    Backpropagate multi-run peptide and protein scores to single files
    """
    if outfile is None:
        outfile = infile
    else:
        outfile = outfile
    backpropagate_oswr(infile, outfile, apply_scores)