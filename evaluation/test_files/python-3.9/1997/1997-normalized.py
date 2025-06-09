def plot(self, timestep='AUTO', metric='AUTO', server=False, **kwargs):
    """
        Plot training set (and validation set if available) scoring history for an H2OBinomialModel.

        The timestep and metric arguments are restricted to what is available in its scoring history.

        :param str timestep: A unit of measurement for the x-axis.
        :param str metric: A unit of measurement for the y-axis.
        :param bool server: if True, then generate the image inline (using matplotlib's "Agg" backend)
        """
    assert_is_type(metric, 'AUTO', 'logloss', 'auc', 'classification_error', 'rmse')
    if self._model_json['algo'] in ('deeplearning', 'deepwater', 'xgboost', 'drf', 'gbm'):
        if metric == 'AUTO':
            metric = 'logloss'
    self._plot(timestep=timestep, metric=metric, server=server)