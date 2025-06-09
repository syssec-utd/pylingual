def runSamples(self, df, gmt=None):
    """Single Sample GSEA workflow.
           multiprocessing utility on samples.
        """
    self.resultsOnSamples = OrderedDict()
    outdir = self.outdir
    subsets = sorted(gmt.keys())
    tempes = []
    names = []
    rankings = []
    pool = Pool(processes=self._processes)
    for name, ser in df.iteritems():
        dat = ser.sort_values(ascending=self.ascending)
        rankings.append(dat)
        names.append(name)
        genes_sorted, cor_vec = (dat.index.values, dat.values)
        rs = np.random.RandomState(self.seed)
        tempes.append(pool.apply_async(enrichment_score_tensor, args=(genes_sorted, cor_vec, gmt, self.weighted_score_type, self.permutation_num, rs, True, self.scale)))
    pool.close()
    pool.join()
    for i, temp in enumerate(tempes):
        name, rnk = (names[i], rankings[i])
        self._logger.info('Calculate Enrichment Score for Sample: %s ' % name)
        es, esnull, hit_ind, RES = temp.get()
        self.outdir = os.path.join(outdir, str(name))
        mkdirs(self.outdir)
        self.resultsOnSamples[name] = pd.Series(data=es, index=subsets, name=name)
        if self._noplot:
            continue
        self._logger.info('Plotting Sample: %s \n' % name)
        for i, term in enumerate(subsets):
            term = term.replace('/', '_').replace(':', '_')
            outfile = '{0}/{1}.{2}.{3}'.format(self.outdir, term, self.module, self.format)
            gseaplot(rank_metric=rnk, term=term, hits_indices=hit_ind[i], nes=es[i], pval=1, fdr=1, RES=RES[i], pheno_pos='', pheno_neg='', figsize=self.figsize, ofname=outfile)
    self._save(outdir)
    return