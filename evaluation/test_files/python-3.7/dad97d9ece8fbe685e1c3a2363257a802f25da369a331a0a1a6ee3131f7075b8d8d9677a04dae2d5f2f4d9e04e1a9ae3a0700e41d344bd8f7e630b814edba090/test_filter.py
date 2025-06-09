import logging
from typing import List
import pytest
from bomf.filter import Filter

class _FooFilter(Filter):

    async def predicate(self, candidate: dict) -> bool:
        return 'foo' in candidate and candidate['foo'] == 'bar'

class TestFilter:

    @pytest.mark.parametrize('filter_under_test,candidates,survivors', [pytest.param(_FooFilter(), [{'foo': 'baz'}, {'foo': 'bar'}], [{'foo': 'bar'}])])
    async def test_filter(self, filter_under_test: Filter, candidates: List[dict], survivors: List[dict], caplog):
        caplog.set_level(logging.DEBUG, logger=self.__module__)
        actual = await filter_under_test.apply(candidates)
        assert actual == survivors
        assert '1 out of 2 candidates have been removed by the filter' in caplog.messages