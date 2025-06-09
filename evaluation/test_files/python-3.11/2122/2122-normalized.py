def stratified_split(self, test_frac=0.2, seed=-1):
    """
        Construct a column that can be used to perform a random stratified split.

        :param float test_frac: The fraction of rows that will belong to the "test".
        :param int seed: The seed for the random number generator.

        :returns: an H2OFrame having single categorical column with two levels: ``"train"`` and ``"test"``.

        :examples:
          >>> stratsplit = df["y"].stratified_split(test_frac=0.3, seed=12349453)
          >>> train = df[stratsplit=="train"]
          >>> test = df[stratsplit=="test"]
          >>>
          >>> # check that the distributions among the initial frame, and the
          >>> # train/test frames match
          >>> df["y"].table()["Count"] / df["y"].table()["Count"].sum()
          >>> train["y"].table()["Count"] / train["y"].table()["Count"].sum()
          >>> test["y"].table()["Count"] / test["y"].table()["Count"].sum()
        """
    return H2OFrame._expr(expr=ExprNode('h2o.random_stratified_split', self, test_frac, seed))