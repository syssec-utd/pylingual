import pandas as pd
from dgl.data.utils import get_download_dir, download, _get_dgl_url, extract_archive
from .csv_dataset import MoleculeCSVDataset
__all__ = ['ToxCast']

class ToxCast(MoleculeCSVDataset):
    """ToxCast from MoleculeNet for the prediction of toxicology data

    The Toxicology in the 21st Century (https://tripod.nih.gov/tox21/challenge/)
    initiative created a data collection providing toxicology data for a large library
    of compounds based on in vitro high-throughput screening. The dataset includes qualitative
    results of over 600 experiments on 8615 compounds.

    References:

        * [1] MoleculeNet: A Benchmark for Molecular Machine Learning.
        * [2] ToxCast Chemical Landscape: Paving the Road to 21st Century Toxicology
        * [3] DeepChem

    Parameters
    ----------
    smiles_to_graph: callable, str -> DGLGraph
        A function turning a SMILES string into a DGLGraph. If None, it uses
        :func:`dgllife.utils.SMILESToBigraph` by default.
    node_featurizer : callable, rdkit.Chem.rdchem.Mol -> dict
        Featurization for nodes like atoms in a molecule, which can be used to update
        ndata for a DGLGraph. Default to None.
    edge_featurizer : callable, rdkit.Chem.rdchem.Mol -> dict
        Featurization for edges like bonds in a molecule, which can be used to update
        edata for a DGLGraph. Default to None.
    load : bool
        Whether to load the previously pre-processed dataset or pre-process from scratch.
        ``load`` should be False when we want to try different graph construction and
        featurization methods and need to preprocess from scratch. Default to False.
    log_every : bool
        Print a message every time ``log_every`` molecules are processed. Default to 1000.
    cache_file_path : str
        Path to the cached DGLGraphs, default to 'toxcast_dglgraph.bin'.
    n_jobs : int
        The maximum number of concurrently running jobs for graph construction and featurization,
        using joblib backend. Default to 1.

    Examples
    --------

    >>> import torch
    >>> from dgllife.data import ToxCast
    >>> from dgllife.utils import SMILESToBigraph, CanonicalAtomFeaturizer

    >>> smiles_to_g = SMILESToBigraph(node_featurizer=CanonicalAtomFeaturizer())
    >>> dataset = ToxCast(smiles_to_g)
    >>> # Get size of the dataset
    >>> len(dataset)
    8576
    >>> # Get the 0th datapoint, consisting of SMILES, DGLGraph, labels, and masks
    >>> dataset[0]
    ('[O-][N+](=O)C1=CC=C(Cl)C=C1',
     Graph(num_nodes=10, num_edges=20,
           ndata_schemes={'h': Scheme(shape=(74,), dtype=torch.float32)}
           edata_schemes={})
     tensor([0., ..., 0.]),
     tensor([1., ..., 1.]))

    To address the imbalance between positive and negative samples, we can re-weight
    positive samples for each task based on the training datapoints.

    >>> train_ids = torch.arange(500)
    >>> dataset.task_pos_weights(train_ids)
    tensor([4.0435e+00, ..., 1.7500e+01])
    """

    def __init__(self, smiles_to_graph=None, node_featurizer=None, edge_featurizer=None, load=False, log_every=1000, cache_file_path='./toxcast_dglgraph.bin', n_jobs=1):
        self._url = 'dataset/toxcast.zip'
        data_path = get_download_dir() + '/toxcast.zip'
        dir_path = get_download_dir() + '/toxcast'
        download(_get_dgl_url(self._url), path=data_path, overwrite=False)
        extract_archive(data_path, dir_path)
        df = pd.read_csv(dir_path + '/toxcast_data.csv')
        super(ToxCast, self).__init__(df=df, smiles_to_graph=smiles_to_graph, node_featurizer=node_featurizer, edge_featurizer=edge_featurizer, smiles_column='smiles', cache_file_path=cache_file_path, load=load, log_every=log_every, init_mask=True, n_jobs=n_jobs)

    def __getitem__(self, item):
        """Get datapoint with index

        Parameters
        ----------
        item : int
            Datapoint index

        Returns
        -------
        str
            SMILES for the ith datapoint
        DGLGraph
            DGLGraph for the ith datapoint
        Tensor of dtype float32 and shape (T)
            Labels of the ith datapoint for all tasks. T for the number of tasks.
        Tensor of dtype float32 and shape (T)
            Binary masks of the ith datapoint indicating the existence of labels for all tasks.
        """
        return (self.smiles[item], self.graphs[item], self.labels[item], self.mask[item])