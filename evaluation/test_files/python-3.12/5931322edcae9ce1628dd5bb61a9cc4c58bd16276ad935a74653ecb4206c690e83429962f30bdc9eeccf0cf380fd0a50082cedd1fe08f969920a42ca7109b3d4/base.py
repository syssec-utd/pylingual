from abc import ABC
from nonebot_plugin_pixivbot.context import Inject
from nonebot_plugin_pixivbot.service.pixiv_service import PixivService
from ..base import MatcherEntryHandler
from ..interceptor.cooldown_interceptor import CooldownInterceptor
from ..interceptor.loading_prompt_interceptor import LoadingPromptInterceptor
from ..interceptor.record_req_interceptor import RecordReqInterceptor
from ..interceptor.timeout_interceptor import TimeoutInterceptor
from ..pkg_context import context

@context.inject
class CommonHandler(MatcherEntryHandler, ABC):
    service = Inject(PixivService)

    def __init__(self):
        super().__init__()
        self.add_interceptor(context.require(CooldownInterceptor))
        self.add_interceptor(context.require(TimeoutInterceptor))
        self.add_interceptor(context.require(LoadingPromptInterceptor))

class RecordCommonHandler(CommonHandler, ABC):

    def __init__(self):
        super().__init__()
        self.add_interceptor(context.require(RecordReqInterceptor))