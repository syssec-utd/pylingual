import typing
from dataclasses import dataclass
from typing import Callable
from injector import inject
from mob.GitCli.BranchName import BranchName
from mob.GitCli.GitCliInterface import GitCliInterface
from mob.GitCli.UndoCommands.ComposedUndoCommand import ComposedUndoCommand
from mob.GitCli.UndoCommands.UndoCallable import UndoCallable
from mob.GitCli.UndoCommands.UndoCommand import UndoCommand

@inject
@dataclass(frozen=True)
class GitCliWithAutoRollback(GitCliInterface, UndoCommand):
    git: GitCliInterface
    __undo_command: ComposedUndoCommand = ComposedUndoCommand()

    def fail_if_dirty(self, *args, **kwargs) -> None:
        return self.__call(self.git.fail_if_dirty, *args, **kwargs)

    def push(self, *args, **kwargs) -> UndoCommand:
        return self.__call(self.git.push, *args, **kwargs)

    def current_branch(self, *args, **kwargs) -> typing.Optional[BranchName]:
        return self.__call(self.git.current_branch, *args, **kwargs)

    def branch_exists(self, *args, **kwargs) -> bool:
        return self.__call(self.git.branch_exists, *args, **kwargs)

    def checkout(self, *args, **kwargs) -> UndoCommand:
        return self.__call(self.git.checkout, *args, **kwargs)

    def fetch_all(self, *args, **kwargs) -> None:
        return self.__call(self.git.fetch_all, *args, **kwargs)

    def squash_all(self, *args, **kwargs) -> UndoCommand:
        return self.__call(self.git.squash_all, *args, **kwargs)

    def create_new_branch_from_main_and_checkout(self, *args, **kwargs) -> UndoCommand:
        return self.__call(self.git.create_new_branch_from_main_and_checkout, *args, **kwargs)

    def add_to_git_info_exclude(self, *args, **kwargs) -> UndoCommand:
        return self.__call(self.git.add_to_git_info_exclude, *args, **kwargs)

    def commit_all_and_push(self, *args, **kwargs) -> UndoCommand:
        return self.__call(self.git.commit_all_and_push, *args, **kwargs)

    def undo(self):
        if self.__undo_command.has_commands:
            self.__undo_command.undo()

    def commit_all(self, *args, **kwargs) -> UndoCommand:
        return self.__call(self.git.commit_all, *args, **kwargs)

    def add_undo_command(self, undo_command: UndoCommand):
        self.__undo_command.add_command(undo_command)

    def add_undo_callable(self, c: callable):
        self.__undo_command.add_command(UndoCallable(c))

    @property
    def undo_commands(self) -> ComposedUndoCommand:
        return self.__undo_command

    def __call(self, method: Callable, *args, **kwargs):
        result = method(*args, **kwargs)
        if isinstance(result, UndoCommand):
            self.__undo_command.add_command(result)
        return result