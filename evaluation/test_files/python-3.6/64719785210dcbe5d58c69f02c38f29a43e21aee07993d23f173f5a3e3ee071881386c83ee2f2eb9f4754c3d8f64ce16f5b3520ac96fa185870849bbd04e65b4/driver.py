from __future__ import annotations
from contextlib import asynccontextmanager
from typing import AsyncGenerator, List, Optional
TXNID = '/internal/worker/{worker}'
DEFAULT_SCAN_LIMIT = 10
DEFAULT_BATCH_SCAN_LIMIT = 100

class Transaction:
    driver: Driver
    open: bool

    async def abort(self):
        raise NotImplementedError()

    async def commit(self, worker: Optional[str]=None, tid: Optional[int]=None, resource: bool=True):
        raise NotImplementedError()

    async def batch_get(self, keys: List[str]):
        raise NotImplementedError()

    async def get(self, key: str) -> Optional[bytes]:
        raise NotImplementedError()

    async def set(self, key: str, value: bytes):
        raise NotImplementedError()

    async def delete(self, key: str):
        raise NotImplementedError()

    def keys(self, match: str, count: int=DEFAULT_SCAN_LIMIT, include_start: bool=True) -> AsyncGenerator[str, None]:
        raise NotImplementedError()

class Driver:
    initialized = False

    async def last_seqid(self, worker: str) -> Optional[int]:
        txn = await self.begin()
        key = TXNID.format(worker=worker)
        last_seq = await txn.get(key)
        await txn.abort()
        if last_seq is None:
            return None
        else:
            return int(last_seq)

    async def initialize(self):
        raise NotImplementedError()

    async def finalize(self):
        raise NotImplementedError()

    async def begin(self) -> Transaction:
        raise NotImplementedError()

    async def keys(self, match: str, count: int=DEFAULT_SCAN_LIMIT, include_start: bool=True) -> AsyncGenerator[str, None]:
        raise NotImplementedError()
        yield

    @asynccontextmanager
    async def transaction(self) -> AsyncGenerator[Transaction, None]:
        """
        Use to make sure transaction is always aborted
        """
        txn: Optional[Transaction] = None
        try:
            txn = await self.begin()
            yield txn
        finally:
            if txn is not None and txn.open:
                await txn.abort()