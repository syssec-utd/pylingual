import pytest

@pytest.mark.tolerate(max_failures=1)
@pytest.mark.parametrize('i', range(1))
def test_marker_only(i):
    assert False

@pytest.fixture(scope='function', params=[0, pytest.param(1, marks=pytest.mark.xfail), 2])
def data(request):
    yield request.param

@pytest.mark.tolerate(max_failures=1)
def test_marker_only_with_data_fixture(data):
    assert False

@pytest.mark.parametrize('i', [1, pytest.param(2, marks=pytest.mark.xfail)])
def test_fixture_only(tolerate, i):
    for _ in range(i):
        with tolerate(max_failures=1):
            assert False

@pytest.mark.xfail(reason='This should fail because we should pass arguments when calling the tolerate fixture')
def test_fixture_call_no_arguments(tolerate):
    for _ in range(1):
        with tolerate():
            assert False

@pytest.mark.tolerate(max_failures=1)
@pytest.mark.parametrize('i', [1, pytest.param(2, marks=pytest.mark.xfail)])
def test_marker_and_fixture(tolerate, i):
    for _ in range(i):
        with tolerate:
            assert False

@pytest.mark.xfail(reason='This should fail because the tolerate marker expects arguments', raises=ValueError)
@pytest.mark.tolerate()
def test_failure():
    pass

@pytest.mark.tolerate(max_failures=0, exceptions_to_ignore=TypeError)
@pytest.mark.parametrize('i', range(5))
def test_marker_ignore_exception(i):
    raise TypeError