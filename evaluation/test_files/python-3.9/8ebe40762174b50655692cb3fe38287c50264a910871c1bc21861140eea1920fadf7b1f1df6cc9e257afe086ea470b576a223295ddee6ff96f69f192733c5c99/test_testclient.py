import django
import pytest
from ninja_extra import Router
from ninja_extra.testing import TestAsyncClient, TestClient
router = Router(tags=['Some Tag'])

@router.get('/add')
def add(request, a: int, b: int):
    return dict(result=a + b)
if not django.VERSION < (3, 1):

    @router.get('/add-async')
    async def add_async(request, a: int, b: int):
        return dict(result=a + b)

class TestTestClient:

    def test_add_works(self):
        client = TestClient(router)
        res = client.get('/add', query=dict(a=4, b=6))
        assert res.status_code == 200
        assert res.json() == {'result': 10}

@pytest.mark.skipif(django.VERSION < (3, 1), reason='requires django 3.1 or higher')
class TestTestAsyncClient:
    if not django.VERSION < (3, 1):

        @pytest.mark.asyncio
        async def test_add_async_works(self):
            client = TestAsyncClient(router)
            res = await client.get('/add-async', query=dict(a=4, b=6))
            assert res.status_code == 200
            assert res.json() == {'result': 10}

        def test_add_works(self):
            client = TestClient(router)
            res = client.get('/add', query=dict(a=4, b=6))
            assert res.status_code == 200
            assert res.json() == {'result': 10}