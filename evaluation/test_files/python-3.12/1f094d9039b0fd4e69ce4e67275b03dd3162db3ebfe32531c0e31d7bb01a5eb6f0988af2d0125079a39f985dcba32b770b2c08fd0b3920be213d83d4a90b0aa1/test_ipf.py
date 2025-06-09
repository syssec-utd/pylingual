import os
import uuid
from shutil import copytree
from tempfile import gettempdir
from unittest import TestCase
import numpy as np
from aequilibrae import Project
from aequilibrae.distribution import Ipf
from aequilibrae.matrix import AequilibraeData
from ...data import siouxfalls_project

class TestIpf(TestCase):

    def setUp(self) -> None:
        os.environ['PATH'] = os.path.join(gettempdir(), 'temp_data') + ';' + os.environ['PATH']
        self.proj_dir = os.path.join(gettempdir(), uuid.uuid4().hex)
        copytree(siouxfalls_project, self.proj_dir)

    def test_fit(self):
        proj = Project()
        proj.open(self.proj_dir)
        mats = proj.matrices
        mats.update_database()
        seed = mats.get_matrix('SiouxFalls_omx')
        seed.computational_view('matrix')
        args = {'entries': seed.zones, 'field_names': ['rows'], 'data_types': [np.float64], 'memory_mode': True}
        row_vector = AequilibraeData()
        row_vector.create_empty(**args)
        row_vector.rows[:] = np.random.rand(seed.zones)[:] * 1000
        row_vector.index[:] = seed.index[:]
        args['field_names'] = ['columns']
        column_vector = AequilibraeData()
        column_vector.create_empty(**args)
        column_vector.columns[:] = np.random.rand(seed.zones)[:] * 1000
        column_vector.index[:] = seed.index[:]
        column_vector.columns[:] = column_vector.columns[:] * (row_vector.rows.sum() / column_vector.columns.sum())
        args = {'matrix': seed, 'rows': row_vector, 'row_field': 'rows', 'columns': column_vector, 'column_field': 'columns', 'nan_as_zero': False}
        with self.assertRaises(TypeError):
            fratar = Ipf(data='test', test='data')
            fratar.fit()
        with self.assertRaises(ValueError):
            fratar = Ipf(**args)
            fratar.parameters = ['test']
            fratar.fit()
        fratar = Ipf(**args)
        fratar.fit()
        result = fratar.output
        self.assertAlmostEqual(np.nansum(result.matrix_view), np.nansum(row_vector.data['rows']), 4, 'Ipf did not converge')
        self.assertGreater(fratar.parameters['convergence level'], fratar.gap, 'Ipf did not converge')
        mr = fratar.save_to_project('my_matrix_ipf', 'my_matrix_ipf.aem')
        self.assertTrue(os.path.isfile(os.path.join(mats.fldr, 'my_matrix_ipf.aem')), 'Did not save file to the appropriate place')
        self.assertEqual(mr.procedure_id, fratar.procedure_id, 'procedure ID saved wrong')
        proj.close()