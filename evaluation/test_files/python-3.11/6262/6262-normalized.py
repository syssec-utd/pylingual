def _load_ranking(self, rnk):
    """Parse ranking file. This file contains ranking correlation vector( or expression values)
           and gene names or ids.

            :param rnk: the .rnk file of GSEA input or a Pandas DataFrame, Series instance.
            :return: a Pandas Series with gene name indexed rankings

        """
    if isinstance(rnk, pd.DataFrame):
        rank_metric = rnk.copy()
        if rnk.shape[1] == 1:
            rank_metric = rnk.reset_index()
    elif isinstance(rnk, pd.Series):
        rank_metric = rnk.reset_index()
    elif os.path.isfile(rnk):
        rank_metric = pd.read_csv(rnk, header=None, comment='#', sep='\t')
    else:
        raise Exception('Error parsing gene ranking values!')
    rank_metric.sort_values(by=rank_metric.columns[1], ascending=self.ascending, inplace=True)
    if rank_metric.isnull().any(axis=1).sum() > 0:
        self._logger.warning('Input gene rankings contains NA values(gene name and ranking value), drop them all!')
        NAs = rank_metric[rank_metric.isnull().any(axis=1)]
        self._logger.debug('NAs list:\n' + NAs.to_string())
        rank_metric.dropna(how='any', inplace=True)
    if rank_metric.duplicated(subset=rank_metric.columns[0]).sum() > 0:
        self._logger.warning('Input gene rankings contains duplicated IDs, Only use the duplicated ID with highest value!')
        dups = rank_metric[rank_metric.duplicated(subset=rank_metric.columns[0])]
        self._logger.debug('Dups list:\n' + dups.to_string())
        rank_metric.drop_duplicates(subset=rank_metric.columns[0], inplace=True, keep='first')
    rank_metric.reset_index(drop=True, inplace=True)
    rank_metric.columns = ['gene_name', 'rank']
    rankser = rank_metric.set_index('gene_name')['rank']
    self.ranking = rankser
    return rankser