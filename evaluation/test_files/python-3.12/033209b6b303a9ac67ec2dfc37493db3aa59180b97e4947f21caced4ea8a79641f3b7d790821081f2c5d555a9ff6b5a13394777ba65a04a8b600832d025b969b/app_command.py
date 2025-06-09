from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, ClassVar, TypeVar
from hikari import UNDEFINED, CommandOption, Permissions, Snowflakeish
from hikari.api import EntityFactory
from crescent.context.utils import support_custom_context
from crescent.locale import LocaleBuilder, str_or_build_locale
if TYPE_CHECKING:
    from typing import Any, Sequence, Type
    from hikari import CommandType, Snowflake, UndefinedOr, UndefinedType
    from crescent.commands.groups import Group, SubGroup
    from crescent.internal.includable import Includable
    from crescent.typedefs import CommandCallbackT, HookCallbackT, TransformedAutocompleteCallbackT, TransformedHookCallbackT
    Self = TypeVar('Self')

@dataclass(frozen=True)
class Unique:
    name: str
    type: CommandType
    guild_id: Snowflakeish | None
    group: str | None
    sub_group: str | None

    @classmethod
    def from_meta_struct(cls: Type[Unique], command: Includable[AppCommandMeta]) -> Unique:
        return cls(name=str_or_build_locale(command.metadata.app_command.name)[0], type=command.metadata.app_command.type, guild_id=command.metadata.app_command.guild_id, group=str_or_build_locale(command.metadata.group.name)[0] if command.metadata.group else None, sub_group=str_or_build_locale(command.metadata.sub_group.name)[0] if command.metadata.sub_group else None)

    @classmethod
    def from_app_command_meta(cls: Type[Unique], command: AppCommandMeta) -> Unique:
        return cls(name=str_or_build_locale(command.app_command.name)[0], type=command.app_command.type, guild_id=command.app_command.guild_id, group=str_or_build_locale(command.group.name)[0] if command.group else None, sub_group=str_or_build_locale(command.sub_group.name)[0] if command.sub_group else None)
__all__: Sequence[str] = ('AppCommandMeta', 'AppCommand')

@dataclass
class AppCommand:
    """Local representation of an Application Command"""
    type: CommandType
    name: str | LocaleBuilder
    guild_id: Snowflakeish | None
    description: str | LocaleBuilder | None = None
    options: Sequence[CommandOption] | None = None
    default_member_permissions: UndefinedType | int | Permissions = UNDEFINED
    is_dm_enabled: bool = True
    nsfw: bool | None = None
    id: UndefinedOr[Snowflake] = UNDEFINED
    __eq__props: ClassVar[Sequence[str]] = ('type', 'name', 'description', 'guild_id', 'options', 'default_member_permissions', 'is_dm_enabled')

    def __eq__(self, __o: object) -> bool:
        """
        Compares properties or class. Any two attributes that are `False` when
        converted to a bool with be considered equal so different methods of
        saying an attribute doesn't exist won't cause issues.
        """
        for prop in self.__eq__props:
            my_attr = getattr(self, prop)
            o_attr = getattr(__o, prop)
            if my_attr != o_attr and (my_attr or o_attr):
                return False
        return True

    def is_same_command(self, o: AppCommand) -> bool:
        return self.guild_id == o.guild_id and self.name == o.name and (self.type == o.type)

    def build(self, encoder: EntityFactory) -> dict[str, Any]:
        name, name_localizations = str_or_build_locale(self.name)
        out: dict[str, Any] = {'name': name, 'name_localizations': name_localizations, 'type': self.type}
        if self.description:
            description, description_localizations = str_or_build_locale(self.description)
            out['description'] = description
            out['description_localizations'] = description_localizations
        if self.options:
            out['options'] = [encoder.serialize_command_option(option) for option in self.options]
        if isinstance(self.default_member_permissions, Permissions):
            perms = str(self.default_member_permissions.value)
        elif not self.default_member_permissions:
            perms = None
        else:
            perms = str(self.default_member_permissions)
        if self.nsfw is not None:
            out['nsfw'] = self.nsfw
        out['default_member_permissions'] = perms
        out['dm_permission'] = self.is_dm_enabled
        return out

@dataclass
class AppCommandMeta:
    app_command: AppCommand
    owner: Any
    'The function or class that was used to create the command'
    callback: CommandCallbackT
    autocomplete: dict[str, TransformedAutocompleteCallbackT] = field(default_factory=dict)
    group: Group | None = None
    sub_group: SubGroup | None = None
    hooks: list[TransformedHookCallbackT] = field(default_factory=list)
    after_hooks: list[TransformedHookCallbackT] = field(default_factory=list)

    def add_hooks(self, hooks: Sequence[HookCallbackT], prepend: bool=False, *, after: bool) -> None:
        transformed_hooks: list[TransformedHookCallbackT] = [support_custom_context(hook) for hook in hooks]

        def extend_or_prepend(list_to_edit: list[TransformedHookCallbackT]) -> None:
            if prepend:
                list_to_edit[:0] = transformed_hooks
            else:
                list_to_edit.extend(transformed_hooks)
        if not after:
            extend_or_prepend(self.hooks)
        else:
            extend_or_prepend(self.after_hooks)

    @property
    def unique(self) -> Unique:
        return Unique(str_or_build_locale(self.app_command.name)[0], self.app_command.type, self.app_command.guild_id, str_or_build_locale(self.group.name)[0] if self.group else None, str_or_build_locale(self.sub_group.name)[0] if self.sub_group else None)