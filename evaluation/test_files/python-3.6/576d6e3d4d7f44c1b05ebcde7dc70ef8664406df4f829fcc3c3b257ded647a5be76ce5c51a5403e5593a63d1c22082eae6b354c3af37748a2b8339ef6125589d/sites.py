from __future__ import annotations
from typing import List
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session
from greatapi.core.history.schemas import HistorySchema
from greatapi.db.database import get_db
from greatapi.db.database import SessionLocal
from greatapi.db.models.default import History
from greatapi.utils.cbv import cbv
from greatapi.utils.inferring_router import InferringRouter
history_router = InferringRouter(tags=['History'])

@cbv(history_router)
class HistorySite:
    db = SessionLocal()

    @history_router.get('/get_all_history', response_model=List[HistorySchema], status_code=200)
    def get_all_history(self, db: Session=Depends(get_db)) -> list[HistorySchema]:
        items = db.query(History).all()
        return items

    @history_router.post('/create_history', response_model=HistorySchema, status_code=status.HTTP_201_CREATED)
    def create_an_item(self, item: HistorySchema) -> HistorySchema:
        history_item = self.db.query(History).filter(History.name == item.name).first()
        if history_item is not None:
            raise HTTPException(status_code=400, detail='History item already exists')
        new_history_item = History(name=item.name, type=item.type)
        self.db.add(new_history_item)
        self.db.commit()
        return new_history_item