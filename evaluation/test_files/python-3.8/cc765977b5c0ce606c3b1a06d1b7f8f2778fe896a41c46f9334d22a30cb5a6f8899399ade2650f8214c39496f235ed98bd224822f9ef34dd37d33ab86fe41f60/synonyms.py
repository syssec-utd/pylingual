from typing import Optional
from nucliadb_protos.knowledgebox_pb2 import Synonyms as PBSynonyms
from nucliadb.ingest.maindb.driver import Transaction
KB_SYNONYMS = '/kbs/{kbid}/synonyms'

class Synonyms:

    def __init__(self, txn: Transaction, kbid: str):
        self.txn = txn
        self.kbid = kbid

    @property
    def key(self) -> str:
        return KB_SYNONYMS.format(kbid=self.kbid)

    async def set(self, synonyms: PBSynonyms):
        body = synonyms.SerializeToString()
        await self.txn.set(self.key, body)

    async def get(self) -> Optional[PBSynonyms]:
        try:
            payload = await self.txn.get(self.key)
        except KeyError:
            return None
        if payload is None:
            return None
        body = PBSynonyms()
        body.ParseFromString(payload)
        return body

    async def clear(self):
        await self.txn.delete(self.key)