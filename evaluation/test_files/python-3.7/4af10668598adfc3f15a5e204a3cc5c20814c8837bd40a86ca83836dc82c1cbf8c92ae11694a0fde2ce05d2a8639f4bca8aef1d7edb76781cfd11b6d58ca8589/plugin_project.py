from inspect import iscoroutinefunction
from recc.plugin.errors import PluginCallbackNotCoroutineError, PluginCallbackNotFoundError, PluginCallbackRuntimeError
from recc.plugin.mixin._plugin_base import PluginBase
from recc.variables.plugin import NAME_ON_CREATE_PROJECT, NAME_ON_DELETE_PROJECT

class PluginProject(PluginBase):

    @property
    def has_on_create_project(self) -> bool:
        return self.has(NAME_ON_CREATE_PROJECT)

    @property
    def has_on_delete_project(self) -> bool:
        return self.has(NAME_ON_DELETE_PROJECT)

    async def on_create_project(self, uid: int) -> None:
        callback = self.get(NAME_ON_CREATE_PROJECT)
        if callback is None:
            raise PluginCallbackNotFoundError(self.module_name, NAME_ON_CREATE_PROJECT)
        if not iscoroutinefunction(callback):
            raise PluginCallbackNotCoroutineError(self.module_name, NAME_ON_CREATE_PROJECT)
        try:
            await callback(uid)
        except BaseException as e:
            raise PluginCallbackRuntimeError(self.module_name, NAME_ON_CREATE_PROJECT) from e

    async def on_delete_project(self, uid: int) -> None:
        callback = self.get(NAME_ON_DELETE_PROJECT)
        if callback is None:
            raise PluginCallbackNotFoundError(self.module_name, NAME_ON_DELETE_PROJECT)
        if not iscoroutinefunction(callback):
            raise PluginCallbackNotCoroutineError(self.module_name, NAME_ON_DELETE_PROJECT)
        try:
            await callback(uid)
        except BaseException as e:
            raise PluginCallbackRuntimeError(self.module_name, NAME_ON_DELETE_PROJECT) from e