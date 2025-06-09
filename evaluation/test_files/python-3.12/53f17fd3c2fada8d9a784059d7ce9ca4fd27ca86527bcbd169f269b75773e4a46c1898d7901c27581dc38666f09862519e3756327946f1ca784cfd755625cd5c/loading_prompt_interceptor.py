from asyncio import create_task, sleep, shield, Task
from typing import Callable, Optional
from nonebot import logger
from nonebot_plugin_pixivbot.config import Config
from nonebot_plugin_pixivbot.context import Inject
from nonebot_plugin_pixivbot.protocol_dep.post_dest import PostDestination
from .base import Interceptor, T_UID, T_GID
from ..pkg_context import context

@context.inject
@context.register_singleton()
class LoadingPromptInterceptor(Interceptor):
    conf = Inject(Config)

    async def send_delayed_loading_prompt(self, post_dest: PostDestination[T_UID, T_GID]):
        await sleep(self.conf.pixiv_loading_prompt_delayed_time)
        logger.debug(f'send delayed loading to {post_dest.identifier}')
        await shield(self.post_plain_text('努力加载中', post_dest))

    async def intercept(self, wrapped_func: Callable, *args, post_dest: PostDestination[T_UID, T_GID], silently: bool, **kwargs):
        task: Optional[Task] = None
        if not silently:
            task = create_task(self.send_delayed_loading_prompt(post_dest))
        try:
            await wrapped_func(*args, post_dest=post_dest, silently=silently, **kwargs)
        finally:
            if task and (not task.done()):
                task.cancel()