from __future__ import annotations
from typing import TYPE_CHECKING, Mapping, Any, Optional
if TYPE_CHECKING:
    from ..client_ASYNC import Client
from .comment import Comment as BaseComment, LooseComment as BaseLooseComment

class Comment(BaseComment):

    def __init__(self, d: Mapping[str, Any], client: Client) -> None:
        super().__init__(d)
        self.client: Client = client

    async def reply(self, text: str) -> Comment:
        return await self.client.p.comment.reply(self.id, text)

    async def edit_body(self, text: str) -> Comment:
        return await self.client.p.comment.edit_body(self.id, text)

    async def delete(self) -> None:
        await self.client.p.comment.delete(self.id)

    async def lock(self) -> None:
        await self.client.p.comment.lock(self.id)

    async def unlock(self) -> None:
        await self.client.p.comment.unlock(self.id)

    async def distinguish(self) -> Comment:
        return await self.client.p.comment.distinguish(self.id)

    async def distinguish_and_sticky(self) -> Comment:
        return await self.client.p.comment.distinguish_and_sticky(self.id)

    async def undistinguish(self) -> Comment:
        return await self.client.p.comment.undistinguish(self.id)

    async def approve(self) -> None:
        await self.client.p.comment.approve(self.id)

    async def remove(self) -> None:
        await self.client.p.comment.remove(self.id)

    async def remove_spam(self) -> None:
        await self.client.p.comment.remove_spam(self.id)

    async def apply_removal_reason(self, reason_id: Optional[str], note: Optional[str]=None) -> None:
        await self.client.p.comment.apply_removal_reason(self.id, reason_id, note)

    async def send_removal_comment(self, title: str, message: str) -> Comment:
        return await self.client.p.comment.send_removal_comment(self.id, title, message)

    async def send_removal_message(self, title: str, message: str, *, exposed: bool=False) -> None:
        await self.client.p.comment.send_removal_message(self.id, title, message, exposed=exposed)

class LooseComment(Comment, BaseLooseComment):
    pass