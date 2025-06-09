import pytest
import test.fixture.client
from cloudtower.api.snapshot_group_api import SnapshotGroupApi

@pytest.fixture(scope='session')
def snapshot_group_api(client):
    return SnapshotGroupApi(client)