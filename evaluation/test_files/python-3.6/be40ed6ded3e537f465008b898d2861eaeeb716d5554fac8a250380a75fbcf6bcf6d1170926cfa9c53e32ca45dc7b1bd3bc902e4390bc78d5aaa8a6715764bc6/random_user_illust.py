from typing import TypeVar, Union, Sequence
from nonebot_plugin_pixivbot.global_context import context
from nonebot_plugin_pixivbot.protocol_dep.post_dest import PostDestination
from .common import CommonHandler
from ..interceptor.record_req_interceptor import RecordReqInterceptor
UID = TypeVar('UID')
GID = TypeVar('GID')

@context.root.register_singleton()
class RandomUserIllustHandler(CommonHandler):

    def __init__(self):
        super().__init__()
        self.add_interceptor(context.require(RecordReqInterceptor))

    @classmethod
    def type(cls) -> str:
        return 'random_user_illust'

    def enabled(self) -> bool:
        return self.conf.pixiv_random_user_illust_query_enabled

    async def parse_args(self, args: Sequence[str], post_dest: PostDestination[UID, GID]) -> dict:
        try:
            user_id = int(args[0])
            return {'user': user_id}
        except ValueError:
            user = await self.service.get_user(args[0])
            return {'user': user.id}

    async def actual_handle(self, *, user: Union[str, int], count: int=1, post_dest: PostDestination[UID, GID], silently: bool=False):
        (userinfo, illusts) = await self.service.random_user_illust(user, count=count)
        await self.post_illusts(illusts, header=f'这是您点的{userinfo.name}({userinfo.id})老师的图', post_dest=post_dest)