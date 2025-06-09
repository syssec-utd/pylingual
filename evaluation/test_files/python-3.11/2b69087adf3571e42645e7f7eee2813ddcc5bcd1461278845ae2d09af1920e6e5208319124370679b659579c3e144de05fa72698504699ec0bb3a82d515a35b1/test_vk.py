import os
import numpy as np
import pytest
from NuMPI import MPI
from SurfaceTopography import read_topography
from SurfaceTopography.IO import VKReader
pytestmark = pytest.mark.skipif(MPI.COMM_WORLD.Get_size() > 1, reason='tests only serial funcionalities, please execute with pytest')

def test_read_filestream(file_format_examples):
    """
    The reader has to work when the file was already opened as binary for
    it to work in topobank.
    """
    file_path = os.path.join(file_format_examples, 'example.vk4')
    read_topography(file_path)
    with open(file_path, 'r') as f:
        read_topography(f)

def test_vk3_metadata(file_format_examples):
    file_path = os.path.join(file_format_examples, 'example.vk3')
    r = VKReader(file_path)
    t = r.topography()
    nx, ny = t.nb_grid_pts
    assert nx == 1024
    assert ny == 768
    sx, sy = t.physical_sizes
    np.testing.assert_almost_equal(sx, 704847000)
    np.testing.assert_almost_equal(sy, 528463000)
    assert t.unit == 'pm'
    np.testing.assert_almost_equal(t.rms_height_from_area(), 1223148.5774419378)
    assert t.info['acquisition_time'] == '2022-10-28 09:51:59+02:00'

def test_vk4_metadata(file_format_examples):
    file_path = os.path.join(file_format_examples, 'example.vk4')
    r = VKReader(file_path)
    t = r.topography()
    nx, ny = t.nb_grid_pts
    assert nx == 1024
    assert ny == 768
    sx, sy = t.physical_sizes
    np.testing.assert_almost_equal(sx, 1396330551)
    np.testing.assert_almost_equal(sy, 1046906679)
    assert t.unit == 'pm'
    np.testing.assert_almost_equal(t.rms_height_from_area(), 54193042.85097)
    assert t.info['acquisition_time'] == '2022-10-14 09:23:04+02:00'

def test_vk6_metadata(file_format_examples):
    file_path = os.path.join(file_format_examples, 'example.vk6')
    r = VKReader(file_path)
    t = r.topography()
    nx, ny = t.nb_grid_pts
    assert nx == 2048
    assert ny == 1536
    sx, sy = t.physical_sizes
    np.testing.assert_almost_equal(sx, 97169043)
    np.testing.assert_almost_equal(sy, 72864915)
    assert t.unit == 'pm'
    np.testing.assert_almost_equal(t.rms_height_from_area(), 1061663.7395845044)
    assert t.info['acquisition_time'] == '2022-10-23 12:13:10-04:00'