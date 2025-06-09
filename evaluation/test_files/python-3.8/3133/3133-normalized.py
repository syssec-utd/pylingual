def minmax(self, expression, binby=[], limits=None, shape=default_shape, selection=False, delay=False, progress=None):
    """Calculate the minimum and maximum for expressions, possibly on a grid defined by binby.


        Example:

        >>> df.minmax("x")
        array([-128.293991,  271.365997])
        >>> df.minmax(["x", "y"])
        array([[-128.293991 ,  271.365997 ],
                   [ -71.5523682,  146.465836 ]])
        >>> df.minmax("x", binby="x", shape=5, limits=[-10, 10])
        array([[-9.99919128, -6.00010443],
                   [-5.99972439, -2.00002384],
                   [-1.99991322,  1.99998057],
                   [ 2.0000093 ,  5.99983597],
                   [ 6.0004878 ,  9.99984646]])

        :param expression: {expression}
        :param binby: {binby}
        :param limits: {limits}
        :param shape: {shape}
        :param selection: {selection}
        :param delay: {delay}
        :param progress: {progress}
        :return: {return_stat_scalar}, the last dimension is of shape (2)
        """

    @delayed
    def finish(*minmax_list):
        value = vaex.utils.unlistify(waslist, np.array(minmax_list))
        value = value.astype(dtype0)
        return value

    @delayed
    def calculate(expression, limits):
        task = tasks.TaskStatistic(self, binby, shape, limits, weight=expression, op=tasks.OP_MIN_MAX, selection=selection)
        self.executor.schedule(task)
        progressbar.add_task(task, 'minmax for %s' % expression)
        return task

    @delayed
    def finish(*minmax_list):
        value = vaex.utils.unlistify(waslist, np.array(minmax_list))
        value = value.astype(dtype0)
        return value
    expression = _ensure_strings_from_expressions(expression)
    binby = _ensure_strings_from_expressions(binby)
    (waslist, [expressions]) = vaex.utils.listify(expression)
    dtypes = [self.dtype(expr) for expr in expressions]
    dtype0 = dtypes[0]
    if not all([k.kind == dtype0.kind for k in dtypes]):
        raise ValueError('cannot mix datetime and non-datetime expressions')
    progressbar = vaex.utils.progressbars(progress, name='minmaxes')
    limits = self.limits(binby, limits, selection=selection, delay=True)
    all_tasks = [calculate(expression, limits) for expression in expressions]
    result = finish(*all_tasks)
    return self._delay(delay, result)