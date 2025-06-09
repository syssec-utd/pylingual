from __future__ import annotations
from fastapi import status
from greatapi.core.users.query import create_new_user
from greatapi.core.users.query import get_user_by_id
from greatapi.core.users.schemas import ShowUserSchema
from greatapi.core.users.schemas import UserSchema
from greatapi.db.database import SessionLocal
from greatapi.utils.cbv import cbv
from greatapi.utils.inferring_router import InferringRouter
user_router = InferringRouter(tags=['Users'])

@cbv(user_router)
class UserSite:
    db = SessionLocal()

    @user_router.post('/user', response_model=UserSchema, status_code=status.HTTP_201_CREATED)
    def create_user(self, request: UserSchema) -> UserSchema:
        return create_new_user(request, self.db)

    @user_router.get('/user/{id}', response_model=ShowUserSchema)
    def get_user(self, id: int) -> ShowUserSchema:
        return get_user_by_id(id, self.db)