import os
import numpy as np
import unittest
from context import dpdata

class TestEmptySystem(unittest.TestCase):

    def test_empty(self):
        sys1 = dpdata.System(type_map=['A', 'H', 'B', 'O', 'D'])
        sys2 = dpdata.LabeledSystem(type_map=['A', 'H', 'B', 'O', 'D'])

    def test_data_empty(self):
        data = {'atom_names': ['A', 'B'], 'atom_numbs': [0, 0], 'atom_types': np.array([], dtype=int), 'orig': np.array([0, 0, 0]), 'cells': np.array([]), 'coords': np.array([])}
        sys1 = dpdata.System(data=data)
        data = {'atom_names': ['A', 'B'], 'atom_numbs': [0, 0], 'atom_types': np.array([], dtype=int), 'orig': np.array([0, 0, 0]), 'cells': np.array([]), 'coords': np.array([]), 'forces': np.array([]), 'energies': np.array([]), 'virials': np.array([])}
        sys2 = dpdata.LabeledSystem(data=data)