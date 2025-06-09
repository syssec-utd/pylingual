from operator import attrgetter
from pathlib import Path
import pytest
from tests.enum_scenarios import scenario_list
from jenkins_jobs.modules import wrappers
fixtures_dir = Path(__file__).parent / 'fixtures'

@pytest.fixture(params=scenario_list(fixtures_dir), ids=attrgetter('name'))
def scenario(request):
    return request.param

def test_yaml_snippet(check_generator):
    check_generator(wrappers.Wrappers)