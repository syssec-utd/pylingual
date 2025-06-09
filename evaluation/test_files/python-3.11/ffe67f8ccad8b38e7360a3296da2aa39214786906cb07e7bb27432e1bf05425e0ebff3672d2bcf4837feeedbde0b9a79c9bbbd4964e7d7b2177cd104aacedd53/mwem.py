import math
import random
from typing import List
import warnings
from itertools import combinations, product
import numpy as np
import pandas as pd
from snsynth.base import Synthesizer

class Query:

    def __init__(self, query):
        self.query = query

    def evaluate(self, hist):
        e = hist.T[tuple(self.query)]
        if isinstance(e, np.ndarray):
            return np.sum(e)
        else:
            return e

    def error(self, hist, synth_hist):
        return np.abs(self.evaluate(hist) - self.evaluate(synth_hist))

    def mask(self, hist):
        data = np.zeros_like(hist.copy())
        view = data.copy()
        view.T[tuple(self.query)] = 1.0
        return view

    @property
    def queries(self):
        return [self]

    @classmethod
    def make_arbitrary(cls, dims):
        inds = []
        for _, s in np.ndenumerate(dims):
            a = np.random.randint(s)
            b = np.random.randint(s)
            l_b = min(a, b)
            u_b = max(a, b) + 1
            pre = []
            pre.append(l_b)
            pre.append(u_b)
            inds.append(pre)
        sl = []
        for ind in inds:
            sl.append(np.s_[ind[0]:ind[1]])
        return Query(sl)

    @classmethod
    def make_marginals(cls, dims_mask):
        dims_mask = list(reversed(dims_mask))
        mask = [1 if v is not None else 0 for v in dims_mask]
        mask = np.cumsum(mask) - 1
        mask = [x if y is not None else None for x, y in zip(mask, dims_mask)]
        dims = [d for d in dims_mask if d is not None]
        ranges = [range(d) for d in dims]
        prod = product(*ranges)
        return [Query([np.s_[:] if v is None else np.s_[p[v]] for v in mask]) for p in prod]

class Cuboid:

    def __init__(self, queries, dims_mask):
        self.queries = queries
        dims_mask = dims_mask

    @property
    def n_cells(self):
        return len(self.queries)

    @property
    def n_cols(self):
        return np.sum([1 if c is not None else 0 for c in self.dims_mask])

    def error(self, hist, synth_hist):
        err = np.sum([q.error(hist, synth_hist) for q in self.queries])
        err = err / self.n_cells
        return err if err > 0.0 else 0.0

    @classmethod
    def make_cuboid(cls, dimensions, columns):
        assert max(columns) < len(dimensions)
        dims_mask = [d if c in columns else None for c, d in enumerate(dimensions)]
        queries = Query.make_marginals(dims_mask)
        return Cuboid(queries, dims_mask)

    @classmethod
    def make_n_way(cls, dimensions, n):
        n_dims = len(dimensions)
        if n_dims < n:
            return []
        indices = list(np.arange(n_dims))
        combos = list(combinations(indices, n))
        return [cls.make_cuboid(dimensions, c) for c in combos]

class Histogram:

    def __init__(self, data, dimensions, bins, split):
        self.data = data
        self.dimensions = dimensions
        self.bins = bins
        self.split = split
        self.queries = []
        assert len(self.dimensions) == len(self.bins)
        assert len(self.dimensions) == len(self.split)
        assert all([a == b for a, b in zip(self.data.shape, self.dimensions)])

    @property
    def dimensionality(self):
        return np.prod(self.dimensions)

    @property
    def n_cols(self):
        return len(self.dimensions)

    @property
    def n_cuboids(self):
        return 2 ** self.n_cols - 1

    @property
    def n_queries(self):
        return len(self.queries)

    @property
    def n_slices(self):
        return np.sum([len(q.queries) for q in self.queries])

    def add_arbitrary_queries(self, n_queries):
        for _ in range(n_queries):
            self.queries.append(Query.make_arbitrary(self.dimensions))

    def add_marginal_queries(self, max_cols=2):
        dims = self.dimensions
        for n in range(1, max_cols + 1):
            cuboids = Cuboid.make_n_way(dims, n)
            for c in cuboids:
                self.queries.extend(c.queries)

    def add_cuboid_queries(self, max_cols):
        dims = self.dimensions
        max_cols = max_cols if max_cols <= len(dims) else len(dims)
        for n in range(1, max_cols + 1):
            cuboids = Cuboid.make_n_way(dims, n)
            self.queries.extend(cuboids)

    @classmethod
    def histogramdd_indexes(cls, x: np.ndarray, category_lengths: List[int]) -> np.ndarray:
        """Compute counts of each combination of categories in d dimensions.
        Discrete version of np.histogramdd.
        :param x: data of shape [n, len(`category_lengths`)] of non-negative category indexes
        :param category_lengths: the number of unique categories per column
        """
        assert x.shape[1] == len(category_lengths)
        assert x.ndim == 2
        if not len(category_lengths):
            return np.array(x.shape[0])
        flat_indices = np.ravel_multi_index(x.T, category_lengths)
        hist = np.bincount(flat_indices, minlength=np.prod(category_lengths))
        return hist.reshape(category_lengths)

class MWEMSynthesizer(Synthesizer):
    """
        N-Dimensional numpy implementation of MWEM.
        (http://users.cms.caltech.edu/~katrina/papers/mwem-nips.pdf)

    From the paper:
    "[MWEM is] a broadly applicable, simple, and easy-to-implement
    algorithm, capable of substantially improving the performance of
    linear queries on many realistic datasets...
    (circa 2012)...MWEM matches the best known and nearly
    optimal theoretical accuracy guarantees for differentially private
    data analysis with linear queries."

    Linear queries used for sampling in this implementation are
    random contiguous slices of the n-dimensional numpy array.

    :param epsilon: Privacy budget.
    :type epsilon: float, optional
    :param q_count: Number of random queries in the pool to generate.
        Must be more than # of iterations
    :type q_count: int, optional
    :param iterations: Number of iterations of MWEM to run.  MWEM will
        guess a reasonable number of iterations if this is not specified.
    :type iterations: int, optional
    :param splits: Allows you to specify feature dependence when creating
        internal histograms.
        Columns that are known to be dependent can be kept together.
        Example: splits=[[0,1],[2,3]] where
        columns 0 and 1 are dependent, columns 2 and 3 are dependent,
        and between groupings there is independence, defaults to []
    :type splits: list, optional
    :param split_factor: If splits not specified, can instead subdivide
        pseudo-randomly. For example, split_factor=3
        will make groupings of features of size 3 for the histograms.
        Note: this will likely make synthetic data worse.
        defaults to None
    :type split_factor: int, optional
    :param marginal_width: MWEM by default will create cuboids to measure
        marginals, and will use a heuristic to determine the maximum width
        of the marginals.  This parameter allows you to specify that MWEM
        should always measure marginals up to width marginal_width.
    :type marginal_width: int, optional
    :param add_ranges: In addition to measuring cuboids, MWEM can measure
        randomly generated range queries.  Range queries work well on columns
        that are binned from continuous values.
    :type add_range: bool, optional
    :param measure_only: MWEM operates by spending some privacy budget to select
        the best query.  This parameter allows you to specify that MWEM should
        uniformly measure all queries, and not spend any privacy budget on the
        query selection.  This is useful in limited cases.  Allowing MWEM to select
        will usually work best.
    :type measure_only: bool, optional
    :param max_retries_exp_mechanism: In each iteration, MWEM tries to select
        a poorly-peforming query that hasn't yet been measured.  If it fails,
        it will select one of the remaining queries uniformly at random.
    :type max_retries_exp_mechanism: int, optional
    :param mult_weights_iterations: Number of iterations of multiplicative weights,
        per iteration of MWEM, defaults to 20
    :type mult_weights_iterations: int, optional
    :param verbose: Set to True to print debug information.
    :type verbose: bool, optional
    """

    def __init__(self, epsilon=3.0, *ignore, q_count=None, iterations=None, splits=[], split_factor=None, marginal_width=None, add_ranges=False, measure_only=False, max_retries_exp_mechanism=10, mult_weights_iterations=20, verbose=False):
        self.epsilon = epsilon
        self.q_count = q_count
        self.iterations = iterations
        self.mult_weights_iterations = mult_weights_iterations
        self.add_ranges = add_ranges
        self.measure_only = measure_only
        self.synthetic_data = None
        self.data_bins = None
        self.real_data = None
        self.splits = splits
        self.split_factor = split_factor
        self.mins_maxes = {}
        self.scale = {}
        self.marginal_width = marginal_width
        self.debug = verbose
        self.pandas = False
        self.pd_cols = None
        self.pd_index = None
        self.q_values = None
        self.max_retries_exp_mechanism = max_retries_exp_mechanism
        self.accountant = []

    @property
    def spent(self):
        return sum([a for a in self.accountant])

    def fit(self, data, *ignore, transformer=None, categorical_columns=None, ordinal_columns=None, continuous_columns=None, preprocessor_eps=0.0, nullable=False):
        """
        Follows sdgym schema to be compatible with their benchmark system.

        :param data: Dataset to use as basis for synthetic data
        :type data: np.ndarray
        :return: synthetic data, real data histograms
        :rtype: np.ndarray
        """
        train_data = self._get_train_data(data, style='cube', transformer=transformer, categorical_columns=categorical_columns, ordinal_columns=ordinal_columns, continuous_columns=continuous_columns, nullable=nullable, preprocessor_eps=preprocessor_eps)
        data = train_data
        if isinstance(data, np.ndarray):
            self.data = data.copy()
        elif isinstance(data, pd.DataFrame):
            self.pandas = True
            for col in data.columns:
                data[col] = pd.to_numeric(data[col], errors='ignore')
            self.data = data.to_numpy().copy()
            self.pd_cols = data.columns
            self.pd_index = data.index
        elif isinstance(data, list):
            self.data = np.array(data)
        else:
            raise ValueError('Data must be a list of tuples, a numpy array, or a pandas dataframe.')
        if self.split_factor is not None and self.splits == []:
            self.splits = self._generate_splits(self.data.T.shape[0], self.split_factor)
        elif self.split_factor is None and self.splits == []:
            self.split_factor = self.data.shape[1]
            self.splits = self._generate_splits(self.data.T.shape[0], self.split_factor)
        self.splits = np.array(self.splits)
        if self.splits.size == 0:
            self.histograms = self._histogram_from_data_attributes(self.data, [np.arange(self.data.shape[1])])
        else:
            self.histograms = self._histogram_from_data_attributes(self.data, self.splits)
        if self.debug:
            print(f'Processing {len(self.histograms)} histograms')
            print()
        n_histograms = len(self.histograms)
        for idx, h in enumerate(self.histograms):
            marginal_width = self.marginal_width
            scale = np.sum(h.data)
            iterations = self.iterations
            if iterations is None:
                iterations = int(np.ceil(np.log10(scale))) * 10
            if marginal_width is None:
                if scale > 10000:
                    marginal_width = 3
                else:
                    marginal_width = 2
            h.add_cuboid_queries(marginal_width)
            q_count = self.q_count if self.q_count is not None else 2 * iterations
            while h.n_queries < q_count:
                if self.add_ranges:
                    h.add_arbitrary_queries(q_count - h.n_queries)
                else:
                    h.add_cuboid_queries(marginal_width)
            if h.n_queries > q_count:
                h.queries = np.random.choice(h.queries, q_count, replace=False)
            meas_eps = self.epsilon / 2.0 / n_histograms / iterations
            meas_bounds = -np.log(2 * 0.05) * (1 / meas_eps)
            h.iterations = iterations
            h.meas_eps = meas_eps
            h.meas_bound = meas_bounds
            if self.debug:
                print(f'Histogram #{idx} split: {h.split}')
                print(f'Columns: {h.n_cols}')
                print(f'Dimensionality: {h.dimensionality:,}')
                print(f'Cuboids possible: {h.n_cuboids}')
                print(f'1-2-way cuboids possible: {math.comb(h.n_cols, 2) + h.n_cols}')
                print(f'Fitting for {h.iterations} iterations')
                print(f'Number of queries: {h.n_queries}')
                print(f'Number of slices in queries: {h.n_slices}')
                print(f'Per-Measure Epsilon: {h.meas_eps:.3f}')
                print(f'Measurement Error: {h.meas_bound:.2f}')
                print()
        self.max_iterations = max([h.iterations for h in self.histograms])
        self.synthetic_histograms = self.mwem()

    def sample(self, samples):
        """
        Creates samples from the histogram data.
        Follows sdgym schema to be compatible with their benchmark system.
        NOTE: We are sampling from each split dimensional
        group as though they are *independent* from one another.
        We have essentially created len(splits) DP histograms as
        if they are separate databases, and combine the results into
        a single sample.

        :param samples: Number of samples to generate
        :type samples: int
        :return: N samples
        :rtype: list(np.ndarray)
        """
        synthesized_columns = ()
        first = True
        for fake, _, split in self.synthetic_histograms:
            s = []
            fake_indices = np.arange(len(np.ravel(fake)))
            fake_distribution = np.ravel(fake)
            norm = np.sum(fake)
            for _ in range(samples):
                s.append(np.random.choice(fake_indices, p=fake_distribution / norm))
            s_unraveled = []
            for ind in s:
                s_unraveled.append(np.unravel_index(ind, fake.shape))
            np_unraveled = np.array(s_unraveled)
            for i in range(np_unraveled.shape[-1]):
                min_c, max_c = self.mins_maxes[str(split[i])]
                np_unraveled[:, i] = np_unraveled[:, i] * self.scale[str(split[i])]
                np_unraveled[:, i] = np_unraveled[:, i] + min_c
            if first:
                synthesized_columns = np_unraveled
                first = False
            else:
                synthesized_columns = np.hstack((synthesized_columns, np_unraveled))
        combined = synthesized_columns
        r = self._reorder(self.splits)
        return self._transformer.inverse_transform(combined[:, r])

    def mwem(self):
        """
        Runner for the mwem algorithm.
        Initializes the synthetic histogram, and updates it
        for up to self.max_iterations using the exponential mechanism and
        multiplicative weights. Draws from the initialized query store
        for measurements.

        :return: synth_hist, self.histogram - synth_hist is the
            synthetic data histogram, self.histogram is original histo
        :rtype: np.ndarray, np.ndarray
        """
        a_values = []
        for idx, h in enumerate(self.histograms):
            hist = h.data
            dimensions = h.dimensions
            split = h.split
            queries = h.queries
            synth_hist = self._initialize_a(hist, dimensions)
            measurements = {}
            flat_dim = h.dimensionality
            iterations = h.iterations
            if 2 * flat_dim <= iterations:
                warnings.warn('Flattened dimensionality of synthetic histogram is less than' + ' the number of iterations. This is a privacy risk.' + ' Consider increasing your split_factor (especially if it is 1), ' + 'or decreasing the number of iterations. ' + 'Dim: ' + str(flat_dim) + ' Split: ' + str(split), Warning)
            eps = h.meas_eps if not self.measure_only else 2 * h.meas_eps
            for i in range(iterations):
                qi = self._exponential_mechanism(hist, synth_hist, queries, eps, measurements, i)
                for query in queries[qi].queries:
                    assert isinstance(query, Query)
                    actual = query.evaluate(hist)
                    lap = self._laplace(1.0 / eps)
                    if qi in measurements:
                        measurements[qi].append(actual + lap)
                    else:
                        measurements[qi] = [actual + lap]
                self.accountant.append(eps)
                synth_hist = self._multiplicative_weights(synth_hist, queries, measurements, hist, self.mult_weights_iterations)
            a_values.append((synth_hist, hist, split))
        return a_values

    def _initialize_a(self, histogram, dimensions):
        """
        Initializes a uniform distribution histogram from
        the given histogram with dimensions

        :param histogram: Reference histogram
        :type histogram: np.ndarray
        :param dimensions: Reference dimensions
        :type dimensions: np.ndarray
        :return: New histogram, uniformly distributed according to
            reference histogram
        :rtype: np.ndarray
        """
        n = np.sum(histogram)
        value = n / np.prod(dimensions)
        synth_hist = np.zeros_like(histogram)
        synth_hist += value
        return synth_hist

    def _histogram_from_data_attributes(self, data, splits=[]):
        """
        Create a histogram from given data

        :param data: Reference histogram
        :type data: np.ndarray
        :return: Histogram over given data, dimensions,
            bins created (output of np.histogramdd)
        :rtype: np.ndarray, np.shape, np.ndarray
        """
        histograms = []
        for split in splits:
            split_data = data[:, split]
            mins_data = []
            maxs_data = []
            dims_sizes = []
            for i, column in enumerate(split_data.T):
                min_c = min(column)
                max_c = max(column)
                mins_data.append(min_c)
                maxs_data.append(max_c)
                bin_count = int(max_c - min_c + 1)
                self.mins_maxes[str(split[i])] = (min_c, max_c)
                self.scale[str(split[i])] = 1
                dims_sizes.append(bin_count)
            if any([a > 0 for a in mins_data]):
                warnings.warn('Data should be preprocessed to have 0 based indices.')
            dimensionality = np.product(dims_sizes)
            if dimensionality > 100000000.0:
                warnings.warn(f'Dimensionality of histogram is {dimensionality:,}, consider using splits.')
            histogram, bins = np.histogramdd(split_data, bins=dims_sizes)
            h = Histogram(histogram, dims_sizes, bins, split)
            histograms.append(h)
        return histograms

    def _exponential_mechanism(self, hist, synth_hist, queries, eps, measurements, iteration):
        """
        Refer to paper for in depth description of
        Exponential Mechanism.
        Parametrized with epsilon value epsilon/(2 * iterations)

        :param hist: Basis histogram
        :type hist: np.ndarray
        :param synth_hist: Synthetic histogram
        :type synth_hist: np.ndarray
        :param queries: Queries to draw from
        :type queries: list
        :param eps: Budget
        :type eps: float
        :return: # of errors
        :rtype: int
        """
        errors = [queries[i].error(hist, synth_hist) * (eps / 2.0) for i in range(len(queries))]
        maxi = max(errors)
        mean_err = np.mean(errors)
        exp_errors = [math.exp(errors[i] - maxi) for i in range(len(errors))]
        count_retries = 0
        qi = None
        while qi is None or qi in measurements:
            if self.measure_only or count_retries > self.max_retries_exp_mechanism:
                options = [i for i in range(len(queries))]
                options = [i for i in options if i not in measurements]
                qi = np.random.choice(options)
            else:
                r = random.random()
                e_s = sum(exp_errors)
                c = 0
                qi = len(exp_errors) - 1
                for i in range(len(exp_errors)):
                    c += exp_errors[i]
                    if c > r * e_s:
                        qi = i
                        break
                count_retries += 1
        if self.debug:
            log = int(np.floor(np.log10(self.max_iterations)))
            skip = 1 if log < 2 else 10 ** (log - 1)
            if iteration % skip == 0:
                print(f'[{iteration}] - Average error: {mean_err:.3f}. Selected {len(queries[qi].queries)} slices')
        if not self.measure_only:
            self.accountant.append(eps)
        return qi

    def _multiplicative_weights(self, synth_hist, queries, m, hist, iterate):
        """
        Multiplicative weights update algorithm,
        used to boost the synthetic data accuracy given measurements m.
        Run for iterate times

        :param synth_hist: Synthetic histogram
        :type synth_hist: np.ndarray
        :param queries: Queries to draw from
        :type queries: list
        :param m: Measurements taken from real data for each qi query
        :type m: dict
        :param hist: Basis histogram
        :type hist: np.ndarray
        :param iterate: Number of iterations to run mult weights
        :type iterate: iterate
        :return: synth_hist
        :rtype: np.ndarray
        """
        sum_a = np.sum(synth_hist)
        for _ in range(iterate):
            for qi in m:
                measurements = m[qi]
                queries_list = queries[qi].queries
                assert len(measurements) == len(queries_list)
                for measurement, query in zip(measurements, queries_list):
                    error = measurement - query.evaluate(synth_hist)
                    query_update = query.mask(synth_hist)
                    a_multiplier = np.exp(query_update * error / (2.0 * sum_a))
                    a_multiplier[a_multiplier == 0.0] = 1.0
                    synth_hist = synth_hist * a_multiplier
                    count_a = np.sum(synth_hist)
                    synth_hist = synth_hist * (sum_a / count_a)
        return synth_hist

    def _reorder(self, splits):
        """
        Given an array of dimensionality splits (column indices)
        returns the corresponding reorder array (indices to return
        columns to original order)
        Example:
        original = [[1, 2, 3, 4, 5, 6],
        [ 6,  7,  8,  9, 10, 11]]

        splits = [[1,3,4],[0,2,5]]

        mod_data = [[2 4 5 1 3 6]
                [ 7  9 10  6  8 11]]

        reorder = [3 0 4 1 2 5]

        :param splits: 2d list with splits (column indices)
        :type splits: array of arrays
        :return: 2d list with splits (column indices)
        :rtype: array of arrays
        """
        flat = np.concatenate(np.asarray(splits)).ravel()
        reordered = np.zeros(len(flat))
        for i, ind in enumerate(flat):
            reordered[ind] = i
        return reordered.astype(int)

    def _generate_splits(self, n_dim, factor):
        """
        If user specifies, do the work and figure out how to divide the dimensions
        into even splits to speed up MWEM
        Last split will contain leftovers <= sizeof(factor)

        :param n_dim: Total # of dimensions
        :type n_dim: int
        :param factor: Desired size of the splits
        :type factor: int
        :return: Splits
        :rtype: np.array(np.array(),...)
        """
        indices = np.arange(n_dim)
        fits = int(np.floor(len(indices) / factor) * factor)
        even_inds = indices[:fits].copy().reshape((int(len(indices) / factor), factor))
        s1 = even_inds.tolist()
        if indices[fits:].size != 0:
            s1.append(indices[fits:])
        s2 = [np.array(l_val) for l_val in s1]
        return np.array(s2)

    def _laplace(self, sigma):
        """
        Laplace mechanism

        :param sigma: Laplace scale param sigma
        :type sigma: float
        :return: Random value from laplace distribution [-1,1]
        :rtype: float
        """
        return sigma * np.log(random.random()) * np.random.choice([-1, 1])