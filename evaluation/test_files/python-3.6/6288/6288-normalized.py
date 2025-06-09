def enrich(self, gmt):
    """use local mode
         
        p = p-value computed using the Fisher exact test (Hypergeometric test)  

        Not implemented here:

            combine score = log(p)·z

        see here: http://amp.pharm.mssm.edu/Enrichr/help#background&q=4
        
        columns contain:
            
            Term Overlap P-value Adjusted_P-value Genes

        """
    if isscalar(self.background):
        if isinstance(self.background, int) or self.background.isdigit():
            self._bg = int(self.background)
        elif isinstance(self.background, str):
            self._bg = self.get_background()
            self._logger.info('Background: found %s genes' % len(self._bg))
        else:
            raise Exception('Unsupported background data type')
    else:
        try:
            it = iter(self.background)
            self._bg = set(self.background)
        except TypeError:
            self._logger.error('Unsupported background data type')
    hgtest = list(calc_pvalues(query=self._gls, gene_sets=gmt, background=self._bg))
    if len(hgtest) > 0:
        (terms, pvals, olsz, gsetsz, genes) = hgtest
        (fdrs, rej) = multiple_testing_correction(ps=pvals, alpha=self.cutoff, method='benjamini-hochberg')
        odict = OrderedDict()
        odict['Term'] = terms
        odict['Overlap'] = list(map(lambda h, g: '%s/%s' % (h, g), olsz, gsetsz))
        odict['P-value'] = pvals
        odict['Adjusted P-value'] = fdrs
        odict['Genes'] = [';'.join(g) for g in genes]
        res = pd.DataFrame(odict)
        return res
    return