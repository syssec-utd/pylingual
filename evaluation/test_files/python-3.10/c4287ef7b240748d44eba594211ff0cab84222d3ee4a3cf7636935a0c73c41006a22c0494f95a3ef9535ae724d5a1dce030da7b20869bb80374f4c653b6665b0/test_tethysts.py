"""
Created on 2021-04-27.

@author: Mike K
"""
import os
import pathlib
import shutil
from tethysts import Tethys
import pandas as pd
import os
import pytest
pd.options.display.max_columns = 10
base_path = os.path.join(os.path.split(os.path.realpath(os.path.dirname(__file__)))[0], 'datasets/tests')
remote2 = {'bucket': 'nz-open-modelling-consortium', 'public_url': 'https://b2.nzrivers.xyz/file/', 'version': 4}
remote3 = {'bucket': 'fire-emergency-nz', 'public_url': 'https://b2.tethys-ts.xyz/file/', 'version': 4}
remote4 = {'bucket': 'ecan-env-monitoring', 'public_url': 'https://b2.tethys-ts.xyz/file', 'version': 4}
remote5 = {'bucket': 'gwrc-env', 'public_url': 'https://b2.tethys-ts.xyz/file', 'version': 4}
dataset_id = '7751c5f1bf47867fb109d7eb'
remotes = [{'remote': remote2, 'dataset_id': dataset_id, 'heights': [10], 'assert': {'datasets': 1, 'stations': 2, 'versions': 0, 'results': 0}}, {'remote': remote3, 'dataset_id': 'dddb02cd5cb7ae191311ab19', 'heights': None, 'assert': {'datasets': 1, 'stations': 2, 'versions': 0, 'results': 1}}, {'remote': remote4, 'dataset_id': 'f16774ea29f024a306c7fc7a', 'heights': None, 'assert': {'datasets': 1, 'stations': 2, 'versions': 0, 'results': 1}}, {'remote': remote5, 'dataset_id': '9568f663d566aabb62a8e98e', 'heights': None, 'assert': {'datasets': 1, 'stations': 2, 'versions': 0, 'results': 1}}]
geometry1 = {'type': 'Point', 'coordinates': [172, -42.8]}
lat = -42.8
lon = 172.0
distance = 1
bp = pathlib.Path(base_path)
bp.mkdir(parents=True, exist_ok=True)

@pytest.mark.parametrize('remote', remotes)
def test_tethys_memory(remote):
    """

    """
    t1 = Tethys([remote['remote']])
    datasets = t1.datasets
    assert len(datasets) > remote['assert']['datasets']
    stn_list1 = t1.get_stations(remote['dataset_id'])
    assert len(stn_list1) > remote['assert']['stations']
    rv1 = t1.get_versions(remote['dataset_id'])
    assert len(rv1) > remote['assert']['versions']
    station_ids = [s['station_id'] for s in stn_list1[:2]]
    data1 = t1.get_results(remote['dataset_id'], station_ids, heights=remote['heights'])
    assert len(data1) > remote['assert']['results']
    test_h5 = os.path.join(base_path, remote['dataset_id'] + '_test.h5')
    s2 = t1.get_results(remote['dataset_id'], station_ids, heights=remote['heights'], output_path=test_h5)
    assert len(s2) > 0
    os.remove(test_h5)

@pytest.mark.parametrize('remote', remotes)
def test_tethys_cache(remote):
    """

    """
    t1 = Tethys([remote['remote']], cache=base_path)
    datasets = t1.datasets
    assert len(datasets) > remote['assert']['datasets']
    stn_list1 = t1.get_stations(remote['dataset_id'])
    assert len(stn_list1) > remote['assert']['stations']
    rv1 = t1.get_versions(remote['dataset_id'])
    assert len(rv1) > remote['assert']['versions']
    station_ids = [s['station_id'] for s in stn_list1[:2]]
    data1 = t1.get_results(remote['dataset_id'], station_ids, heights=remote['heights'])
    assert len(data1) > remote['assert']['results']
    test_h5 = os.path.join(base_path, remote['dataset_id'] + '_test.h5')
    s2 = t1.get_results(remote['dataset_id'], station_ids, heights=remote['heights'], output_path=test_h5)
    assert len(s2) > 0
    shutil.rmtree(base_path)
t1 = Tethys([remote2])

def test_get_nearest_station1():
    s1 = t1.get_stations(dataset_id, geometry1)
    assert len(s1) == 1

def test_get_nearest_station2():
    s2 = t1.get_stations(dataset_id, lat=lat, lon=lon)
    assert len(s2) == 1

def test_get_intersection_stations1():
    s3 = t1.get_stations(dataset_id, lat=lat, lon=lon, distance=distance)
    assert len(s3) >= 2

def test_get_nearest_results1():
    s1 = t1.get_results(dataset_id, geometry=geometry1, heights=[10])
    assert len(s1) > 0

def test_get_nearest_results2():
    s2 = t1.get_results(dataset_id, lat=lat, lon=lon, heights=[10])
    assert len(s2) > 0