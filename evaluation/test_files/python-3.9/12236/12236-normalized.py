def merge(infiles, outfile, same_run, templatefile):
    """
    Merge multiple OSW files and (for large experiments, it is recommended to subsample first).
    """
    if len(infiles) < 1:
        raise click.ClickException('At least one PyProphet input file needs to be provided.')
    merge_osw(infiles, outfile, templatefile, same_run)