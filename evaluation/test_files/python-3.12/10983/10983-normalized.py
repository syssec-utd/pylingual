def ancestral_reconstruction(params):
    """
    implementing treetime ancestral
    """
    if assure_tree(params, tmp_dir='ancestral_tmp'):
        return 1
    outdir = get_outdir(params, '_ancestral')
    basename = get_basename(params, outdir)
    gtr = create_gtr(params)
    aln, ref, fixed_pi = read_if_vcf(params)
    is_vcf = True if ref is not None else False
    treeanc = TreeAnc(params.tree, aln=aln, ref=ref, gtr=gtr, verbose=1, fill_overhangs=not params.keep_overhangs)
    ndiff = treeanc.infer_ancestral_sequences('ml', infer_gtr=params.gtr == 'infer', marginal=params.marginal, fixed_pi=fixed_pi)
    if ndiff == ttconf.ERROR:
        return 1
    if params.gtr == 'infer':
        print('\nInferred GTR model:')
        print(treeanc.gtr)
    export_sequences_and_tree(treeanc, basename, is_vcf, params.zero_based, report_ambiguous=params.report_ambiguous)
    return 0