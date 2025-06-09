def estimate_clock_model(params):
    """
    implementing treetime clock
    """
    if assure_tree(params, tmp_dir='clock_model_tmp'):
        return 1
    dates = utils.parse_dates(params.dates)
    if len(dates) == 0:
        return 1
    outdir = get_outdir(params, '_clock')
    aln, ref, fixed_pi = read_if_vcf(params)
    is_vcf = True if ref is not None else False
    if params.aln is None and params.sequence_length is None:
        print("one of arguments '--aln' and '--sequence-length' is required.", file=sys.stderr)
        return 1
    basename = get_basename(params, outdir)
    myTree = TreeTime(dates=dates, tree=params.tree, aln=aln, gtr='JC69', verbose=params.verbose, seq_len=params.sequence_length, ref=ref)
    myTree.tip_slack = params.tip_slack
    if myTree.tree is None:
        print('ERROR: tree loading failed. exiting...')
        return 1
    if params.clock_filter:
        n_bad = [n.name for n in myTree.tree.get_terminals() if n.bad_branch]
        myTree.clock_filter(n_iqd=params.clock_filter, reroot=params.reroot or 'least-squares')
        n_bad_after = [n.name for n in myTree.tree.get_terminals() if n.bad_branch]
        if len(n_bad_after) > len(n_bad):
            print("The following leaves don't follow a loose clock and will be ignored in rate estimation:\n\t" + '\n\t'.join(set(n_bad_after).difference(n_bad)))
    if not params.keep_root:
        if params.covariation:
            myTree.run(root='least-squares', max_iter=0, use_covariation=params.covariation)
        res = myTree.reroot(params.reroot, force_positive=not params.allow_negative_rate)
        myTree.get_clock_model(covariation=params.covariation)
        if res == ttconf.ERROR:
            print("ERROR: unknown root or rooting mechanism!\n\tvalid choices are 'least-squares', 'ML', and 'ML-rough'")
            return 1
    else:
        myTree.get_clock_model(covariation=params.covariation)
    d2d = utils.DateConversion.from_regression(myTree.clock_model)
    print('\n', d2d)
    print('The R^2 value indicates the fraction of variation in\nroot-to-tip distance explained by the sampling times.\nHigher values corresponds more clock-like behavior (max 1.0).')
    print('\nThe rate is the slope of the best fit of the date to\nthe root-to-tip distance and provides an estimate of\nthe substitution rate. The rate needs to be positive!\nNegative rates suggest an inappropriate root.\n')
    print('\nThe estimated rate and tree correspond to a root date:')
    if params.covariation:
        reg = myTree.clock_model
        dp = np.array([reg['intercept'] / reg['slope'] ** 2, -1.0 / reg['slope']])
        droot = np.sqrt(reg['cov'][:2, :2].dot(dp).dot(dp))
        print('\n--- root-date:\t %3.2f +/- %1.2f (one std-dev)\n\n' % (-d2d.intercept / d2d.clock_rate, droot))
    else:
        print('\n--- root-date:\t %3.2f\n\n' % (-d2d.intercept / d2d.clock_rate))
    if not params.keep_root:
        outtree_name = basename + 'rerooted.newick'
        Phylo.write(myTree.tree, outtree_name, 'newick')
        print('--- re-rooted tree written to \n\t%s\n' % outtree_name)
    table_fname = basename + 'rtt.csv'
    with open(table_fname, 'w') as ofile:
        ofile.write('#name, date, root-to-tip distance\n')
        ofile.write("#Dates of nodes that didn't have a specified date are inferred from the root-to-tip regression.\n")
        for n in myTree.tree.get_terminals():
            if hasattr(n, 'raw_date_constraint') and n.raw_date_constraint is not None:
                if np.isscalar(n.raw_date_constraint):
                    tmp_str = str(n.raw_date_constraint)
                elif len(n.raw_date_constraint):
                    tmp_str = str(n.raw_date_constraint[0]) + '-' + str(n.raw_date_constraint[1])
                else:
                    tmp_str = ''
                ofile.write('%s, %s, %f\n' % (n.name, tmp_str, n.dist2root))
            else:
                ofile.write('%s, %f, %f\n' % (n.name, d2d.numdate_from_dist2root(n.dist2root), n.dist2root))
        for n in myTree.tree.get_nonterminals(order='preorder'):
            ofile.write('%s, %f, %f\n' % (n.name, d2d.numdate_from_dist2root(n.dist2root), n.dist2root))
        print('--- wrote dates and root-to-tip distances to \n\t%s\n' % table_fname)
    plot_rtt(myTree, outdir + params.plot_rtt)
    return 0