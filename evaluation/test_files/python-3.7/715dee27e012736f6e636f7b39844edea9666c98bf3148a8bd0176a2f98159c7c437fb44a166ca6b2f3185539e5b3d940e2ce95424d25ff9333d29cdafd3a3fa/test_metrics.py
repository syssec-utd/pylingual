from datetime import datetime, timedelta
from unittest.mock import ANY, Mock
import pytest
from quetz.dao import Dao
from quetz.metrics.db_models import IntervalType, next_timestamp, round_timestamp
from quetz.metrics.tasks import synchronize_metrics_from_mirrors

def test_round_timestamp():
    timestamp = datetime.fromisoformat('2020-02-03T04:05')
    rounded = datetime.fromisoformat('2020-02-03T00:00')
    period = IntervalType.day
    assert round_timestamp(timestamp, period) == rounded
    period = IntervalType.hour
    rounded = datetime(2020, 2, 3, 4, 0)
    assert round_timestamp(timestamp, period) == rounded

def test_next_timestamp():
    t = datetime.fromisoformat('2020-02-03T04:05')
    T = IntervalType
    assert next_timestamp(t, T.hour) == datetime(2020, 2, 3, 5, 5)
    assert next_timestamp(t, T.day) == datetime(2020, 2, 4, 4, 5)
    assert next_timestamp(t, T.month) == datetime(2020, 3, 3, 4, 5)
    assert next_timestamp(t, T.year) == datetime(2021, 2, 3, 4, 5)
    assert next_timestamp(datetime(2020, 12, 31, 23, 55), T.hour) == datetime(2021, 1, 1, 0, 55)
    assert next_timestamp(datetime(2020, 12, 31, 23, 55), T.month) == datetime(2021, 1, 31, 23, 55)
    with pytest.raises(ValueError):
        assert next_timestamp(datetime(2020, 1, 31, 23, 55), T.month) == datetime(2021, 2, 28, 23, 55)

def test_get_download_count(auth_client, public_channel, package_version, db, dao: Dao):
    timestamps = ['2020-01-05T21:01', '2020-01-06T22:10', '2020-02-18T10:10']
    month_day = []
    for t in timestamps:
        dt = datetime.fromisoformat(t)
        dao.incr_download_count(public_channel.name, package_version.filename, package_version.platform, timestamp=dt)
        month_day.append((dt.month, dt.day))
    endpoint_url = f'/metrics/channels/{public_channel.name}/packages/{package_version.package_name}/versions/{package_version.platform}/{package_version.filename}'
    response = auth_client.get(endpoint_url)
    assert response.status_code == 200
    assert response.json() == {'server_timestamp': ANY, 'period': 'D', 'metric_name': 'download', 'total': 3, 'series': [{'timestamp': f'2020-{m:02}-{d:02}T00:00:00', 'count': 1} for (m, d) in month_day]}
    response = auth_client.get(endpoint_url + '?start=2020-01-05T10:00')
    assert response.status_code == 200
    assert response.json() == {'server_timestamp': ANY, 'period': 'D', 'metric_name': 'download', 'total': 2, 'series': [{'timestamp': f'2020-{m:02}-{d:02}T00:00:00', 'count': 1} for (m, d) in month_day[1:]]}
    response = auth_client.get(endpoint_url + '?start=2020-01-05T20:00&end=2020-01-05T22:00&period=H&fill_zeros=true')
    assert response.status_code == 200
    assert response.json() == {'server_timestamp': ANY, 'period': 'H', 'metric_name': 'download', 'total': 1, 'series': [{'timestamp': '2020-01-05T20:00:00', 'count': 0}, {'timestamp': '2020-01-05T21:00:00', 'count': 1}, {'timestamp': '2020-01-05T22:00:00', 'count': 0}]}
    response = auth_client.get(endpoint_url + '?period=M')
    assert response.status_code == 200
    assert response.json() == {'server_timestamp': ANY, 'period': 'M', 'metric_name': 'download', 'total': 3, 'series': [{'timestamp': f'2020-{m:02}-01T00:00:00', 'count': c} for (m, c) in [(1, 2), (2, 1)]]}

@pytest.fixture
def package_version_factory(channel_name, user, dao, public_package, db):
    package_format = 'tarbz2'
    package_info = '{}'
    package_name = public_package.name
    versions = []

    def factory(version, build_str=0, platform='linux-64'):
        filename = f'{package_name}-{version}-{build_str}.tar.bz2'
        version = dao.create_version(channel_name, package_name, package_format, 'linux-64', version, build_str, str(build_str), str(filename), package_info, user.id, size=11)
        versions.append(version)
        return version
    yield factory
    for version in versions:
        db.delete(version)
    db.commit()

def test_get_channel_download_count(auth_client, public_channel, package_version_factory, db, dao: Dao):
    versions = [package_version_factory(str(i)) for i in range(3)]
    now = datetime.utcnow()
    for v in versions:
        dao.incr_download_count(public_channel.name, v.filename, v.platform, timestamp=now)
    endpoint_url = f'/metrics/channels/{public_channel.name}'
    response = auth_client.get(endpoint_url)
    assert response.status_code == 200
    expected = {'server_timestamp': ANY, 'metric_name': 'download', 'period': 'D', 'packages': {v.platform + '/' + v.filename: {'series': [{'timestamp': now.replace(minute=0, second=0, microsecond=0, hour=0).isoformat(), 'count': 1}]} for v in versions}}
    assert response.json() == expected

@pytest.fixture
def channel_mirror(public_channel, dao: Dao):
    mirror_url = 'http://mirror_server/get/my-mirror'
    api_endpoint = 'http://mirror_server/api/my-mirror'
    metrics_endpoint = 'http://mirror_server/metrics/channels/my-mirror'
    return dao.create_channel_mirror(public_channel.name, mirror_url, api_endpoint, metrics_endpoint)

def test_synchronize_metrics_without_mirrors(public_channel, package_version, dao: Dao):
    session = Mock()
    synchronize_metrics_from_mirrors(public_channel.name, dao, session)
    metrics = dao.get_package_version_metrics(package_version.id, IntervalType.hour, 'download')
    assert not metrics
    session.get.assert_not_called()

def test_synchronize_metrics_with_mirrors(public_channel, package_version, channel_mirror, dao: Dao):
    timestamp = datetime(2020, 10, 1, 5, 0)
    first_sync_time = timestamp - timedelta(days=1)
    sync_time = timestamp + timedelta(hours=1)
    session = Mock()
    session.get.return_value.json.return_value = {'server_timestamp': first_sync_time.isoformat(), 'packages': {}}
    session.get.return_value.status_code = 200
    synchronize_metrics_from_mirrors(public_channel.name, dao, session, now=first_sync_time)
    metrics = dao.get_package_version_metrics(package_version.id, IntervalType.hour, 'download')
    assert not metrics
    session.get.assert_called_with(f'http://mirror_server/metrics/channels/my-mirror?period=H&end={first_sync_time.isoformat()}')
    session.reset_mock()
    session.get.return_value.json.return_value = {'server_timestamp': sync_time.isoformat(), 'packages': {f'{package_version.platform}/{package_version.filename}': {'series': [{'timestamp': timestamp.isoformat(), 'count': 2}]}}}
    synchronize_metrics_from_mirrors(public_channel.name, dao, session, sync_time)
    for p in IntervalType:
        metrics = dao.get_package_version_metrics(package_version.id, p, 'download')
        assert len(metrics) == 1
        assert metrics[0].count == 2
    session.get.assert_called_with(f'http://mirror_server/metrics/channels/my-mirror?period=H&start={first_sync_time.isoformat()}&end={sync_time.isoformat()}')
    session.reset_mock()
    hour = timedelta(hours=1)
    session.get.return_value.json.return_value = {'server_timestamp': sync_time.replace(minute=5).isoformat(), 'packages': {f'{package_version.platform}/{package_version.filename}': {'series': [{'timestamp': (timestamp + hour).isoformat(), 'count': 1}]}}}
    third_sync_time = sync_time + hour
    synchronize_metrics_from_mirrors(public_channel.name, dao, session, third_sync_time)
    session.get.assert_called_with(f'http://mirror_server/metrics/channels/my-mirror?period=H&start={sync_time.isoformat()}&end={third_sync_time.isoformat()}')
    metrics = dao.get_package_version_metrics(package_version.id, IntervalType.day, 'download')
    assert len(metrics) == 1
    assert metrics[0].count == 3