from numbers import Real
from types import FunctionType
import numpy as np
import warnings
from scipy.spatial.distance import pdist, squareform
from sklearn.neighbors import KNeighborsTransformer, RadiusNeighborsTransformer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils import check_array
from sklearn.utils.validation import check_is_fitted
from gtda.homology import VietorisRipsPersistence
from gtda.utils.intervals import Interval
from gtda.utils.validation import validate_params
from gtda.plotting import plot_diagram
from gtda.base import PlotterMixin
from gtda.utils._docs import adapt_fit_transform_docs

class LocalVietorisRipsBase(BaseEstimator, TransformerMixin, PlotterMixin):
    """Base class for KNeighboursLocalVietorisRips and RadiusLocalVietorisRips.
    LocalVietorisRipsBase is not meant to be used. Please see documentation
    for KNeighboursLocalVietorisRips and RadiusLocalVietorisRips.

    """

    def __init__(self, metric='euclidean', homology_dimensions=(1, 2), neighborhood_params=(1, 2), collapse_edges=False, n_jobs=None):
        """Initializes the base class by setting the basic parameters.
        For more specific description, see specific children classes."""
        self.metric = metric
        self.homology_dimensions = homology_dimensions
        self.neighborhood_params = neighborhood_params
        self.collapse_edges = collapse_edges
        self.n_jobs = n_jobs

    def fit(self, X, y=None):
        """Initializes the object used for computing persistence homology,
        checks that the parameters were initialized correctly.

        """
        self.homology = VietorisRipsPersistence(metric='precomputed', collapse_edges=self.collapse_edges, homology_dimensions=self.homology_dimensions, n_jobs=self.n_jobs)
        if self.neighborhood_params[0] > self.neighborhood_params[1]:
            warnings.warn('First `neighborhood_params` is larger than second. The values are permuted. ')
            self.neighborhood_params = (self.neighborhood_params[1], self.neighborhood_params[0])
        if self.neighborhood_params[1] == 0:
            warnings.warn('Second `neighborhood_params` is less than 0. Second radius set to 1. ')
            self.radii = (self.radii[0], 1)
        if self.neighborhood_params[0] == self.neighborhood_params[1]:
            warnings.warn('For meaningful features, first `neighborhood_params` should be strictly smaller than second.')
        return self

    def transform(self, X, y=None):
        """Computes the local persistence diagrams at each element of X, and
        returns a list of persistence diagrams, indexed as the points of X.
        This is done in several steps:
            - First compute the nearest neighbors in the point cloud that
            was fitted on, for both values in n_neighbors.
            - For each point, compute the relevant points (corresponding to
            the larger neighborhood_params value), the close points
            (corresponding to the smaller neighborhood_params value), and the
            annulus to cone off (relevant points, but not close points).
            Compute the distance matrix of the relevant points, and add an
            additional row and column corresponding to the coning off point.
            - Finally compute the persistence diagrams of each coned matrices.

        Parameters
        ----------
        X : ndarray of shape (n_points, dimension)
             Input data representing  point cloud:
             an array of shape ``(n_points, n_dimensions)``.

        y : None
            There is no need for a target in a transformer, yet the pipeline
            API requires this parameter.

        Returns
        -------
        Xt : ndarray of shape (n_samples, n_features, 3)
            Array of persistence diagrams computed from the feature arrays.
            ``n_features`` equals :math:`\\sum_q n_q`, where :math:`n_q`
            is the maximum number of topological features in dimension
            :math:`q` across all samples in `X`.

        """
        check_is_fitted(self)
        Xt = check_array(X, accept_sparse=False)
        Xt_close = self.close_neighbors_.transform(Xt)
        Xt_relevant = self.relevant_neighbors_.transform(Xt)
        coned_mats = []
        for i in range(len(Xt)):
            close_indices = Xt_close.getrow(i).indices
            relevant_indices = Xt_relevant.getrow(i).indices
            annulus_indices = list(set(relevant_indices) - set(close_indices))
            reordered_relevant_indices = np.concatenate((close_indices, annulus_indices))
            if len(close_indices) == 0:
                coned_mat = np.zeros((1, 1))
            else:
                relevant_points = [self.relevant_neighbors_._fit_X[int(y)] for y in reordered_relevant_indices]
                local_mat = squareform(pdist(relevant_points, metric=self.metric))
                new_row = np.concatenate((np.ones(len(close_indices)) * np.inf, np.zeros(len(annulus_indices))))
                new_col = np.concatenate((new_row, [0]))
                pre_cone = np.concatenate((local_mat, [new_row]))
                coned_mat = np.concatenate((pre_cone, np.array([new_col], dtype=float).T), axis=1)
            coned_mats += [coned_mat]
        Xt = self.homology.fit_transform(coned_mats)
        return Xt

    @staticmethod
    def plot(Xt, sample=0, homology_dimensions=None, plotly_params=None):
        """Plot a sample from a collection of persistence diagrams, with
        homology in multiple dimensions.

        Parameters
        ----------
        Xt : ndarray of shape (n_samples, n_features, 3)
            Collection of persistence diagrams, such as returned by
            :meth:`transform`.

        sample : int, optional, default: ``0``
            Index of the sample in `Xt` to be plotted.

        homology_dimensions : list, tuple or None, optional, default: ``None``
            Which homology dimensions to include in the plot. ``None`` means
            plotting all dimensions present in ``Xt[sample]``.

        plotly_params : dict or None, optional, default: ``None``
            Custom parameters to configure the plotly figure. Allowed keys are
            ``"traces"`` and ``"layout"``, and the corresponding values should
            be dictionaries containing keyword arguments as would be fed to the
            :meth:`update_traces` and :meth:`update_layout` methods of
            :class:`plotly.graph_objects.Figure`.

        Returns
        -------
        fig : :class:`plotly.graph_objects.Figure` object
            Plotly figure.

        """
        return plot_diagram(Xt[sample], homology_dimensions=homology_dimensions, plotly_params=plotly_params)

@adapt_fit_transform_docs
class KNeighborsLocalVietorisRips(LocalVietorisRipsBase):
    """Given a :ref:`point cloud <finite_metric_spaces_and_point_clouds>` in
    Euclidean space, or an abstract :ref:`metric space
    <finite_metric_spaces_and_point_clouds>` encoded by a distance matrix,
    information about the local topology around each point is summarized in a
    collection of persistence diagrams.

    This is done by first isolating appropriate neighborhoods around each point
    using a nearest neighbor transformer, then "coning off" points in an
    annulus around each point, and finally computing the corresponding
    associated persistence diagram. The output can then be used to explore the
    point cloud, or fed into a vectorizer to obtain features.

    Parameters
    ----------
    metric : string or callable, optional, default: ``"euclidean"``
        Input data is to be interpreted as a point cloud (i.e. feature arrays),
        and `metric`determines a rule with which to calculate distances between
        pairs of points (i.e. row vectors). If `metric` is a string, it must be
        one of the options allowed by :func:`scipy.spatial.distance.pdist`
        for its metric parameter, or a metric listed in
        :obj:`sklearn.pairwise.PAIRWISE_DISTANCE_FUNCTIONS`, including
        ``"euclidean"``, ``"manhattan"`` or ``"cosine"``. If `metric` is a
        callable, it should take pairs of vectors (1D arrays) as input and, for
        each two vectors in a pair, it should return a scalar indicating the
        distance/dissimilarity between them.

    n_neighbors: tuple, optional, default: ``(10, 50)``, has to
        consist of two non-negative integers. This defines the number of points
        in the first and second neighborhoods considered.

    homology_dimensions: tuple, optional, default: ``(1, 2)``. Dimensions
        (non-negative integers) of the topological features to be detected.

    collapse_edges : bool, optional, default: ``False``
        Whether to run the edge collapse algorithm in [1]_ prior to the
        persistent homology computation (see the Notes). Can reduce the runtime
        dramatically when the data or the maximum homology dimensions are
        large.

    n_jobs : int or None, optional, default: ``None``
        The number of jobs to use for the computation. ``None`` means 1 unless
        in a :obj:`joblib.parallel_backend` context. ``-1`` means using all
        processors.

    References
    ----------

    .. [1] J.-D. Boissonnat and S. Pritam, "Edge Collapse and Persistence of
           Flag Complexes"; in *36th International Symposium on Computational
           Geometry (SoCG 2020)*, pp. 19:1–19:15,
           Schloss Dagstuhl-Leibniz–Zentrum für Informatik, 2020;
           `DOI: 10.4230/LIPIcs.SoCG.2020.19
           <https://doi.org/10.4230/LIPIcs.SoCG.2020.19>`_.

    """
    _hyperparameters = {'metric': {'type': (str, FunctionType)}, 'n_neighbors': {'type': (tuple, list), 'of': {type: int, 'in': Interval(1, np.inf, closed='left')}}, 'homology_dimensions': {'type': (tuple, list), 'of': {'type': int, 'in': Interval(0, np.inf, closed='left')}}, 'collapse_edges': {'type': bool}}

    def __init__(self, metric='euclidean', homology_dimensions=(1, 2), n_neighbors=(1, 2), collapse_edges=False, n_jobs=None):
        self.n_neighbors = n_neighbors
        super().__init__(metric=metric, homology_dimensions=homology_dimensions, neighborhood_params=self.n_neighbors, collapse_edges=collapse_edges, n_jobs=n_jobs)

    def fit(self, X, y=None):
        """Initiates and fits the transformers that efficiently computes the
        nearest neighbors of given points.
        This method is here to implement the usual scikit-learn API and hence
        work in pipelines.

        Parameters
        ----------
        X : ndarray of shape (n_points, dimension)
            Input data representing  point cloud. Can be either
            a point cloud: an array of shape ``(n_points, n_dimensions)``.

        y : None
            There is no need for a target in a transformer, yet the pipeline
            API requires this parameter.

        Returns
        -------
        self : object

        """
        super().fit(X)
        validate_params(self.get_params(), self._hyperparameters, exclude=['n_jobs'])
        check_array(X, accept_sparse=False)
        self.size_ = len(X)
        if self.size_ <= self.neighborhood_params[0]:
            warnings.warn('First n_neighbors is too large to be relevant. Consider reducing it.')
            self.neighborhood_params = (self.size_ - 1, self.size_)
        if self.size_ < self.neighborhood_params[1]:
            warnings.warn('Second `n_neighbors` is too large to be relevant. Consider reducing it. ')
            self.neighborhood_params = (self.neighborhood_params[0], self.size_)
        self.close_neighbors_ = KNeighborsTransformer(mode='connectivity', n_neighbors=self.neighborhood_params[0], metric=self.metric, n_jobs=self.n_jobs)
        self.relevant_neighbors_ = KNeighborsTransformer(mode='connectivity', n_neighbors=self.neighborhood_params[1], metric=self.metric, n_jobs=self.n_jobs)
        self.close_neighbors_.fit(X)
        self.relevant_neighbors_.fit(X)
        return self

@adapt_fit_transform_docs
class RadiusLocalVietorisRips(LocalVietorisRipsBase):
    """Given a :ref:`point cloud <finite_metric_spaces_and_point_clouds>` in
    Euclidean space, or an abstract :ref:`metric space
    <finite_metric_spaces_and_point_clouds>` encoded by a distance matrix,
    information about the local topology around each point is summarized in a
    collection of persistence diagrams.

    This is done by first isolating appropriate neighborhoods around each point
    using a radius neighbor transformer, then "coning off" points in an annulus
    around each point, and finally computing the corresponding associated
    persistence diagram. The output can then be used to explore the point
    cloud, or fed into a vectorizer to obtain features.

    Parameters
    ----------
    metric : string or callable, optional, default: ``"euclidean"``
        Input data is to be interpreted as a point cloud (i.e. feature arrays),
        and `metric`determines a rule with which to calculate distances between
        pairs of points (i.e. row vectors). If `metric` is a string, it must be
        one of the options allowed by :func:`scipy.spatial.distance.pdist` for
        its `metric` parameter, or a metric listed in
        :obj:`sklearn.pairwise.PAIRWISE_DISTANCE_FUNCTIONS`, including
        ``"euclidean"``, ``"manhattan"`` or ``"cosine"``. If `metric` is a
        callable, it should take pairs of vectors (1D arrays) as input and, for
        each two vectors in a pair, it should return a scalar indicating the
        distance/dissimilarity between them.

    radii: tuple, optional, default: ``(0.0, 1.0)`` has to consist of two
    non-negative floats. This determines the radius of the first and second
    neighborhood around points considered.

    homology_dimensions: tuple, optional, default: ``(1, 2)``. Dimensions
        (non-negative integers) of the topological features to be detected.

    collapse_edges : bool, optional, default: ``False``
        Whether to run the edge collapse algorithm in [1]_ prior to the
        persistent homology computation (see the Notes). Can reduce the runtime
        dramatically when the data or the maximum homology dimensions are
        large.

    n_jobs : int or None, optional, default: ``None``
        The number of jobs to use for the computation. ``None`` means 1 unless
        in a :obj:`joblib.parallel_backend` context. ``-1`` means using all
        processors.

    References
    ----------
    .. [1] J.-D. Boissonnat and S. Pritam, "Edge Collapse and Persistence of
           Flag Complexes"; in *36th International Symposium on Computational
           Geometry (SoCG 2020)*, pp. 19:1–19:15,
           Schloss Dagstuhl-Leibniz–Zentrum für Informatik, 2020;
           `DOI: 10.4230/LIPIcs.SoCG.2020.19
           <https://doi.org/10.4230/LIPIcs.SoCG.2020.19>`_.

    """
    _hyperparameters = {'metric': {'type': (str, FunctionType)}, 'radii': {'type': (tuple, list), 'of': {type: Real, 'in': Interval(0, np.inf, closed='left')}}, 'homology_dimensions': {'type': (tuple, list), 'of': {'type': int, 'in': Interval(0, np.inf, closed='left')}}, 'collapse_edges': {'type': bool}}

    def __init__(self, metric='euclidean', homology_dimensions=(1, 2), radii=(1, 2), collapse_edges=False, n_jobs=None):
        self.radii = radii
        super().__init__(metric=metric, homology_dimensions=homology_dimensions, neighborhood_params=self.radii, collapse_edges=collapse_edges, n_jobs=n_jobs)

    def fit(self, X, y=None):
        """Initiates and fits the transformers that efficiently computes the
        nearest neighbors of given points.
        This method is here to implement the usual scikit-learn API and hence
        work in pipelines.

        Parameters
        ----------
        X : ndarray of shape (n_points, dimension)
            Input data representing  point cloud. Can be either
            a point cloud: an array of shape ``(n_points, n_dimensions)``.

        y : None
            There is no need for a target in a transformer, yet the pipeline
            API requires this parameter.

        Returns
        -------
        self : object

        """
        super().fit(X)
        validate_params(self.get_params(), self._hyperparameters, exclude=['n_jobs'])
        check_array(X, accept_sparse=False)
        self.close_neighbors_ = RadiusNeighborsTransformer(mode='connectivity', radius=self.neighborhood_params[0], metric=self.metric, n_jobs=self.n_jobs)
        self.relevant_neighbors_ = RadiusNeighborsTransformer(mode='connectivity', radius=self.neighborhood_params[1], metric=self.metric, n_jobs=self.n_jobs)
        self.close_neighbors_.fit(X)
        self.relevant_neighbors_.fit(X)
        return self