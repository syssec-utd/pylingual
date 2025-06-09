def correlation(self, x, y=None, binby=[], limits=None, shape=default_shape, sort=False, sort_key=np.abs, selection=False, delay=False, progress=None):
    """Calculate the correlation coefficient cov[x,y]/(std[x]*std[y]) between and x and y, possibly on a grid defined by binby.

        Example:

        >>> df.correlation("x**2+y**2+z**2", "-log(-E+1)")
        array(0.6366637382215669)
        >>> df.correlation("x**2+y**2+z**2", "-log(-E+1)", binby="Lz", shape=4)
        array([ 0.40594394,  0.69868851,  0.61394099,  0.65266318])

        :param x: {expression}
        :param y: {expression}
        :param binby: {binby}
        :param limits: {limits}
        :param shape: {shape}
        :param selection: {selection}
        :param delay: {delay}
        :param progress: {progress}
        :return: {return_stat_scalar}
        """

    @delayed
    def corr(cov):
        with np.errstate(divide='ignore', invalid='ignore'):
            return cov[..., 0, 1] / (cov[..., 0, 0] * cov[..., 1, 1]) ** 0.5
    if y is None:
        if not isinstance(x, (tuple, list)):
            raise ValueError('if y not given, x is expected to be a list or tuple, not %r' % x)
        if _issequence(x) and (not _issequence(x[0])) and (len(x) == 2):
            x = [x]
        if not (_issequence(x) and all([_issequence(k) and len(k) == 2 for k in x])):
            raise ValueError('if y not given, x is expected to be a list of lists with length 2, not %r' % x)
        waslist = True
        xlist, ylist = zip(*x)
    else:
        waslist, [xlist, ylist] = vaex.utils.listify(x, y)
    limits = self.limits(binby, limits, selection=selection, delay=True)

    @delayed
    def echo(limits):
        logger.debug('>>>>>>>>: %r %r', limits, np.array(limits).shape)
    echo(limits)

    @delayed
    def calculate(limits):
        results = []
        for x, y in zip(xlist, ylist):
            task = self.cov(x, y, binby=binby, limits=limits, shape=shape, selection=selection, delay=True, progress=progressbar)
            results.append(corr(task))
        return results
    progressbar = vaex.utils.progressbars(progress)
    correlations = calculate(limits)

    @delayed
    def finish(correlations):
        if sort:
            correlations = np.array(correlations)
            indices = np.argsort(sort_key(correlations) if sort_key else correlations)[::-1]
            sorted_x = list([x[k] for k in indices])
            return (correlations[indices], sorted_x)
        value = np.array(vaex.utils.unlistify(waslist, correlations))
        return value
    return self._delay(delay, finish(delayed_list(correlations)))