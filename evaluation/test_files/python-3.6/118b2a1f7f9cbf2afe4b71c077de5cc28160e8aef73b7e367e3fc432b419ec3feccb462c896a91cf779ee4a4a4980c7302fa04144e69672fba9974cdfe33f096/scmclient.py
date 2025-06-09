"""Base class for interfacing with source code management tools.

Version Added:
    4.0
"""
import argparse
import logging
import re
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union, cast
from typing_extensions import NotRequired, TypedDict, final
from rbtools.api.capabilities import Capabilities
from rbtools.api.resource import ItemResource, ListResource, ReviewRequestResource
from rbtools.clients.base.patch import PatchAuthor, PatchResult
from rbtools.clients.base.repository import RepositoryInfo
from rbtools.clients.errors import SCMClientDependencyError, SCMError
from rbtools.deprecation import RemovedInRBTools50Warning, deprecate_non_keyword_only_args
from rbtools.diffs.tools.base import BaseDiffTool
from rbtools.diffs.tools.registry import diff_tools_registry
from rbtools.utils.process import execute

class SCMClientRevisionSpec(TypedDict):
    """A revision specification parsed from command line arguments.

    This class helps provide type hinting to results from
    :py:meth:`BaseSCMClient.parse_revision_spec`.

    The dictionary may include other arbitrary keys.

    Version Added:
        4.0
    """
    base: Optional[object]
    tip: Optional[object]
    parent_base: NotRequired[Optional[object]]
    commit_id: NotRequired[Optional[str]]
    extra: NotRequired[Optional[Mapping[str, Any]]]

class SCMClientDiffResult(TypedDict):
    """The result of a diff operation.

    This class helps provide type hinting to results from
    :py:meth:`BaseSCMClient.diff`.

    Version Added:
        4.0
    """
    diff: Optional[bytes]
    parent_diff: NotRequired[Optional[bytes]]
    changenum: NotRequired[Optional[str]]
    commit_id: NotRequired[Optional[str]]
    base_commit_id: NotRequired[Optional[str]]
    review_request_extra_data: NotRequired[Optional[Dict[str, Any]]]

class SCMClientCommitHistoryItem(TypedDict):
    """A commit in a commit history.

    This class helps provide type hinting to results from
    :py:meth:`BaseSCMClient.get_commit_history`.

    Version Added:
        4.0
    """
    commit_id: str
    parent_id: Optional[str]
    commit_message: Optional[str]
    author_name: Optional[str]
    author_email: Optional[str]
    author_date: Optional[str]
    committer_name: NotRequired[Optional[str]]
    committer_email: NotRequired[Optional[str]]
    committer_date: NotRequired[Optional[str]]

class SCMClientCommitMessage(TypedDict):
    """A commit message from a local repository.

    This class helps provide type hinting to results from
    :py:meth:`BaseSCMClient.get_commit_message`.

    Version Added:
        4.0
    """
    summary: Optional[str]
    description: NotRequired[Optional[str]]

class BaseSCMClient(object):
    """A base class for interfacing with a source code management tool.

    These are used for fetching repository information and generating diffs.

    Callers must run :py:meth:`setup` or :py:meth:`has_dependencies` before
    calling methods on this tool.

    Version Changed:
        4.0:
        * Moved from :py:mod:`rbtools.clients` into
          :py:mod:`rbtools.clients.base.scmclient` and renamed from
          ``SCMClient`` to ``BaseSCMClient``.

        * A call to :py:meth:`setup` or :py:meth:`has_dependencies` will be
          required starting in RBTools 5.0.
    """
    scmclient_id: str = ''
    name: str = ''
    server_tool_names: Optional[str] = None
    requires_diff_tool: Union[bool, List[str]] = False
    supports_changesets: bool = False
    supports_commit_history: bool = False
    supports_diff_extra_args: bool = False
    supports_diff_exclude_patterns: bool = False
    supports_no_renames: bool = False
    supports_parent_diffs: bool = False
    supports_patch_revert: bool = False
    can_amend_commit: bool = False
    can_merge: bool = False
    can_push_upstream: bool = False
    can_delete_branch: bool = False
    can_branch: bool = False
    can_bookmark: bool = False
    can_squash_merges: bool = False
    capabilities: Optional[Capabilities]
    config: Dict[str, Any]
    options: Optional[argparse.Namespace]
    is_setup: bool

    def __init__(self, config: Optional[Dict[str, Any]]=None, options: Optional[argparse.Namespace]=None) -> None:
        """Initialize the client.

        Args:
            config (dict, optional):
                The loaded user config.

            options (argparse.Namespace, optional):
                The parsed command line arguments.
        """
        self.config = config or {}
        self.options = options
        self.capabilities = None
        self.is_setup = False
        self._diff_tool: Optional[BaseDiffTool] = None
        self._has_deps: Optional[bool] = None

    @property
    def entrypoint_name(self) -> str:
        """An alias for the SCMClient ID.

        This is here for backwards-compatibility purposes.

        Deprecated:
            4.0:
            Callers should use :py:attr:`scmclient_id`. This attribute will
            be removed in RBTools 5.0.
        """
        cls_name = type(self).__name__
        RemovedInRBTools50Warning.warn('%s.entrypoint_name is deprecated. Please use %s.scmclient_id instead. This will be removed in RBTools 5.0.' % (cls_name, cls_name))
        return self.scmclient_id

    @final
    def setup(self) -> None:
        """Set up the client.

        This will perform checks to ensure the client can be used. Callers
        should make sure to either call this method or
        :py:meth:`has_dependencies` before performing any other operations
        on this client.

        If checks succeed, :py:attr:`is_setup` will be ``True``, and operations
        using this client can be performed.

        If checks fail, an exception may be raised, and :py:attr:`is_setup`
        will be ``False``.

        Note that this will not check :py:attr:`requires_diff_tool`, as that
        is only required for certain operations. Checking for a compatible
        diff tool is the responsibility of the caller whenever working with
        diffs.

        Version Added:
            4.0

        Raises:
            rbtools.clients.errors.SCMClientDependencyError:
                One or more required dependencies are missing.
        """
        if self.is_setup:
            return
        try:
            self.check_dependencies()
            self._has_deps = True
        except SCMClientDependencyError:
            self._has_deps = False
            raise
        self.is_setup = True

    def has_dependencies(self, expect_checked: bool=False) -> bool:
        """Return whether all dependencies for the client are available.

        Either this or :py:meth:`setup` must be called before any operations
        are performed with this client.

        Version Added:
            4.0

        Args:
            expect_checked (bool, optional):
                Whether the caller expects that dependency checking has
                already been done.

                If ``True``, and dependencies have not yet been checked via
                :py:meth:`check_dependencies`, this will raise a deprecation
                warning.

                Starting in RBTools 4.0, this will raise an exception if
                :py:meth:`check_dependencies` hasn't yet been called.

        Returns:
            bool:
            ``True`` if dependencies are all available. ``False`` if one or
            more are not.
        """
        if self._has_deps is None:
            if expect_checked:
                RemovedInRBTools50Warning.warn('Either %(cls_name)s.setup() or %(cls_name)s.has_dependencies() must be called before other functions are used. This will be required starting in RBTools 5.0.' % {'cls_name': type(self).__name__})
            try:
                self.setup()
            except SCMClientDependencyError:
                pass
        return cast(bool, self._has_deps)

    def check_dependencies(self) -> None:
        """Check whether the base dependencies needed are available.

        This is responsible for checking for any command line tools or Python
        modules required to consider this client as an option when scanning
        repositories or selecting a specific client.

        This should not check for diff implementations or anything specific
        about a local filesystem. It's merely a first-pass dependency check.

        This function is normally called via :py:meth:`setup` (which will
        re-raise any exceptions here) or :py:meth:`has_dependencies`. It
        doesn't need to be called manually unless attempting to re-generate
        the exception.

        Subclasses can log any failed checks in the debug log, to help with
        debugging missing tools. If checking against multiple possible names,
        they may also record information needed to locate the matching
        executable for future operations.

        It's recommended to use :py:meth:`rbtools.utils.checks.check_install`
        to help with executable dependency checks.

        Version Added:
            4.0

        Raises:
            rbtools.clients.errors.SCMClientDependencyError:
                One or more required dependencies are missing.
        """
        pass

    def is_remote_only(self) -> bool:
        """Return whether this repository is operating in remote-only mode.

        For some SCMs and some operations, it may be possible to operate
        exclusively with a remote server and have no working directory.

        Version Added:
            3.0

        Returns:
            bool:
            Whether this repository is operating in remote-only mode.
        """
        return False

    def get_local_path(self) -> Optional[str]:
        """Return the local path to the working tree.

        This is expected to be overridden by subclasses.

        Version Added:
            3.0

        Returns:
            str:
            The filesystem path of the repository on the client system.
        """
        logging.warning('%s should implement a get_local_path method', self.__class__)
        info = self.get_repository_info()
        if info:
            return info.local_path
        return None

    def get_repository_info(self) -> Optional[RepositoryInfo]:
        """Return repository information for the current working tree.

        This is expected to be overridden by subclasses.

        Version Added:
            3.0

        Returns:
            rbtools.clients.base.repository.RepositoryInfo:
            The repository info structure.
        """
        return None

    def get_diff_tool(self) -> Optional[BaseDiffTool]:
        """Return a diff tool for use with this client.

        This can be used by subclasses, and by callers that want to check if
        a compatible diff tool is available before calling :py:meth:`diff`.

        The value is cached for the client.

        Version Added:
            4.0

        Returns:
            rbtools.diffs.tools.base.BaseDiffTool:
            The diff instance, if a compatible instance is found.

            This will be ``None`` if :py:attr:`requires_diff_tool` is
            ``False``.

        Raises:
            TypeError:
                :py:attr:`requires_diff_tool` was an unsupported type.

            rbtools.diffs.tools.errors.MissingDiffToolError:
                No compatible diff tool could be found.
        """
        diff_tool = self._diff_tool
        if diff_tool is None:
            if self.requires_diff_tool is True:
                diff_tool = diff_tools_registry.get_available()
            elif self.requires_diff_tool is False:
                diff_tool = None
            elif isinstance(self.requires_diff_tool, list):
                diff_tool = diff_tools_registry.get_available(compatible_diff_tool_ids=self.requires_diff_tool)
            else:
                raise TypeError('Unexpected type %s for %s.requires_diff_tool.' % (type(self.requires_diff_tool), type(self).__name__))
            self._diff_tool = diff_tool
        return diff_tool

    def find_matching_server_repository(self, repositories: ListResource) -> Tuple[Optional[ItemResource], Optional[ItemResource]]:
        """Find a match for the repository on the server.

        Version Added:
            3.0

        Args:
            repositories (rbtools.api.resource.ListResource):
                The fetched repositories.

        Returns:
            tuple:
            A 2-tuple of matching repository information:

            Tuple:
                0 (rbtools.api.resource.ItemResource):
                    The matching repository resource, if found.

                    If not found, this will be ``None``.

                1 (rbtools.api.resource.ItemResource):
                    The matching repository information resource, if found.

                    If not found, this will be ``None``.
        """
        return (None, None)

    def get_repository_name(self) -> Optional[str]:
        """Return any repository name configured in the repository.

        This is used as a fallback from the standard config options, for
        repository types that support configuring the name in repository
        metadata.

        Version Added:
            3.0

        Returns:
            str:
            The configured repository name, or None.
        """
        return None

    def check_options(self) -> None:
        """Verify the command line options.

        This is expected to be overridden by subclasses, if they need to do
        specific validation of the command line.

        Raises:
            rbtools.clients.errors.OptionsCheckError:
                The supplied command line options were incorrect. In
                particular, if a file has history scheduled with the commit,
                the user needs to explicitly choose what behavior they want.
        """
        pass

    def get_changenum(self, revisions: SCMClientRevisionSpec) -> Optional[str]:
        """Return the change number for the given revisions.

        This is only used when the client is supposed to send a change number
        to the server (such as with Perforce).

        Args:
            revisions (dict):
                A revisions dictionary as returned by
                :py:meth:`parse_revision_spec`.

        Returns:
            str:
            The change number to send to the Review Board server.
        """
        return None

    def scan_for_server(self, repository_info: RepositoryInfo) -> Optional[str]:
        """Find the server path.

        This will search for the server name in the .reviewboardrc config
        files. These are loaded with the current directory first, and searching
        through each parent directory, and finally $HOME/.reviewboardrc last.

        Args:
            repository_info (rbtools.clients.base.repository.RepositoryInfo):
                The repository information structure.

        Returns:
            str:
            The Review Board server URL, if available.
        """
        return None

    def parse_revision_spec(self, revisions: List[str]=[]) -> SCMClientRevisionSpec:
        """Parse the given revision spec.

        The 'revisions' argument is a list of revisions as specified by the
        user. Items in the list do not necessarily represent a single revision,
        since the user can use SCM-native syntaxes such as "r1..r2" or "r1:r2".
        SCMTool-specific overrides of this method are expected to deal with
        such syntaxes.

        Args:
            revisions (list of str, optional):
                A list of revisions as specified by the user. Items in the list
                do not necessarily represent a single revision, since the user
                can use SCM-native syntaxes such as ``r1..r2`` or ``r1:r2``.
                SCMTool-specific overrides of this method are expected to deal
                with such syntaxes.

        Returns:
            dict:
            A dictionary containing keys found in
            :py:class:`SCMClientRevisionSpec`.

            Additional keys may be included by subclasses for their own
            internal use.

            These will be used to generate the diffs to upload to Review Board
            (or print). The diff for review will include the changes in (base,
            tip], and the parent diff (if necessary) will include (parent,
            base].

            If a single revision is passed in, this will return the parent of
            that revision for "base" and the passed-in revision for "tip".

            If zero revisions are passed in, this will return revisions
            relevant for the "current change". The exact definition of what
            "current" means is specific to each SCMTool backend, and documented
            in the implementation classes.

        Raises:
            rbtools.clients.errors.InvalidRevisionSpecError:
                The given revisions could not be parsed.

            rbtools.clients.errors.TooManyRevisionsError:
                The specified revisions list contained too many revisions.
        """
        return {'base': None, 'tip': None}

    @deprecate_non_keyword_only_args(RemovedInRBTools50Warning)
    def get_tree_matches_review_request(self, review_request: ReviewRequestResource, *, revisions: SCMClientRevisionSpec, **kwargs) -> Optional[bool]:
        """Return whether a review request matches revisions or tree state.

        This works along with review request matching in tools like
        :command:`rbt post` to match state in a review request (such as in
        ``extra_data``) with the state in the local tree (such as the local
        branch or SCM-specific identifiers other than a commit ID).

        Subclasses can override this to implement their own matching logic.
        By default, no additional logic is implemented.

        Version Added:
            3.1

        Args:
            review_request (rbtools.api.resource.ReviewRequestResource):
                The review request being matched.

            revisions (dict):
                A dictionary of revisions, as returned by
                :py:meth:`parse_revision_spec`.

            **kwargs (dict, unused):
                Additional keyword arguments, for future expansion.

        Returns:
            bool:
            ``True`` if the review request is considered an exact match.

            ``False`` if the review request should be explicitly discarded
            as a possible match.

            ``None`` if a match could not be determined based on available
            information.
        """
        return None

    @deprecate_non_keyword_only_args(RemovedInRBTools50Warning)
    def diff(self, revisions: SCMClientRevisionSpec, *, include_files: List[str]=[], exclude_patterns: List[str]=[], no_renames: bool=False, repository_info: Optional[RepositoryInfo]=None, extra_args: List[str]=[], with_parent_diff: bool=True) -> SCMClientDiffResult:
        """Perform a diff using the given revisions.

        Callers should make sure that the appropriate diff tool is installed
        by calling :py:func:`rbtools.diffs.tools.registry.get_diff_tool` and
        passing :py:attr:`requires_diff_tool` if it's a list.

        This is expected to be overridden by subclasses, which should:

        1. Set :py:attr:`requires_diff_tool` based on the client's needs.
        2. Optionally use :py:attr:`options` for any client-specific diff
           functionality.
        3. Call :py:meth:`get_diff_tool` early, if needed.

        Subclasses that need to support special arguments should use
        :py:attr:`options`.

        Version Changed:
            4.0:
            * All arguments except ``revisions`` must be specified as keyword
              arguments.
            * Subclasses should now use :py:attr:`requires_diff_tool` and
              :py:meth:`get_diff_tool` instead of manually invoking
              :command:`diff` tools.

        Args:
            revisions (dict):
                A dictionary of revisions, as returned by
                :py:meth:`parse_revision_spec`.

            include_files (list of str, optional):
                A list of files to whitelist during the diff generation.

            exclude_patterns (list of str, optional):
                A list of shell-style glob patterns to blacklist during diff
                generation.

            no_renames (bool, optional):
                Whether to avoid rename detection.

            repository_info (rbtools.clients.base.repository.RepositoryInfo,
                             optional):
                The repository info structure.

            extra_args (list, unused):
                Additional arguments to be passed to the diff generation.

            with_parent_diff (bool, optional):
                Whether or not to compute a parent diff.

        Returns:
            dict:
            A dictionary containing keys documented in
            :py:class:`SCMClientDiffResult`.
        """
        return {'diff': None, 'parent_diff': None, 'commit_id': None, 'base_commit_id': None, 'review_request_extra_data': None}

    def get_commit_history(self, revisions: SCMClientRevisionSpec) -> List[SCMClientCommitHistoryItem]:
        """Return the commit history between the given revisions.

        Derived classes must override this method if they support posting with
        history.

        Args:
            revisions (dict):
                The parsed revision spec to use to generate the history.

        Returns:
            list of dict:
            The history entries.
        """
        raise NotImplementedError

    def _get_p_number(self, base_path: str, base_dir: str) -> int:
        """Return the appropriate value for the -p argument to patch.

        This function returns an integer. If the integer is -1, then the -p
        option should not be provided to patch. Otherwise, the return value is
        the argument to :command:`patch -p`.

        Args:
            base_path (str):
                The relative path beetween the repository root and the
                directory that the diff file was generated in.

            base_dir (str):
                The current relative path between the repository root and the
                user's working directory.

        Returns:
            int:
            The prefix number to pass into the :command:`patch` command.
        """
        if base_path and base_dir.startswith(base_path):
            return base_path.count('/') + 1
        else:
            return -1

    def _strip_p_num_slashes(self, files: List[str], p_num: int) -> List[str]:
        """Strip the smallest prefix containing p_num slashes from filenames.

        To match the behavior of the :command:`patch -pX` option, adjacent
        slashes are counted as a single slash.

        Args:
            files (list of str):
                The filenames to process.

            p_num (int):
                The number of prefixes to strip.

        Returns:
            list of str:
            The processed list of filenames.
        """
        if p_num > 0:
            regex = re.compile('[^/]*/+')
            return [regex.sub('', f, p_num) for f in files]
        else:
            return files

    def has_pending_changes(self) -> bool:
        """Return whether there are changes waiting to be committed.

        Derived classes should override this method if they wish to support
        checking for pending changes.

        Returns:
            bool:
            ``True`` if the working directory has been modified or if changes
            have been staged in the index.
        """
        raise NotImplementedError

    @deprecate_non_keyword_only_args(RemovedInRBTools50Warning)
    def apply_patch(self, patch_file: str, *, base_path: str, base_dir: str, p: Optional[str]=None, revert: bool=False) -> PatchResult:
        """Apply the patch and return a PatchResult indicating its success.

        Args:
            patch_file (str):
                The name of the patch file to apply.

            base_path (str):
                The base path that the diff was generated in.

            base_dir (str):
                The path of the current working directory relative to the root
                of the repository.

            p (str, optional):
                The prefix level of the diff.

            revert (bool, optional):
                Whether the patch should be reverted rather than applied.

        Returns:
            rbtools.clients.base.patch.PatchResult:
            The result of the patch operation.
        """
        p_num = p or self._get_p_number(base_path, base_dir)
        cmd = ['patch']
        if revert:
            cmd.append('-R')
        try:
            p_num = int(p_num)
        except ValueError:
            p_num = 0
            logging.warning('Invalid -p value: %s; assuming zero.', p_num)
        if p_num is not None:
            if p_num >= 0:
                cmd.append('-p%d' % p_num)
            else:
                logging.warning('Unsupported -p value: %d; assuming zero.', p_num)
        cmd.extend(['-i', patch_file])
        (rc, patch_output) = execute(cmd, extra_ignore_errors=(2,), return_error_code=True)
        only_garbage_in_patch = 'patch: **** Only garbage was found in the patch input.\n'
        if patch_output and patch_output.startswith('patch: **** ') and (patch_output != only_garbage_in_patch):
            raise SCMError('Failed to execute command: %s\n%s' % (cmd, patch_output))
        if self.supports_empty_files():
            try:
                with open(patch_file, 'rb') as f:
                    patch = f.read()
            except IOError as e:
                raise SCMError('Failed to read patch file "%s": %s' % (patch_file, e))
            patched_empty_files = self.apply_patch_for_empty_files(patch, p_num=str(p_num), revert=revert)
            if patch_output == only_garbage_in_patch and (not patched_empty_files):
                raise SCMError('Failed to execute command: %s\n%s' % (cmd, patch_output))
        return PatchResult(applied=rc == 0, patch_output=patch_output)

    @deprecate_non_keyword_only_args(RemovedInRBTools50Warning)
    def create_commit(self, *, message: str, author: PatchAuthor, run_editor: bool, files: List[str]=[], all_files: bool=False) -> None:
        """Create a commit based on the provided message and author.

        Derived classes should override this method if they wish to support
        committing changes to their repositories.

        Args:
            message (str):
                The commit message to use.

            author (rbtools.clients.base.patch.PatchAuthor):
                The author of the commit.

            run_editor (bool):
                Whether to run the user's editor on the commmit message before
                committing.

            files (list of str, optional):
                The list of filenames to commit.

            all_files (bool, optional):
                Whether to commit all changed files, ignoring the ``files``
                argument.

        Raises:
            NotImplementedError:
                The client does not support creating commits.

            rbtools.clients.errors.CreateCommitError:
                The commit message could not be created. It may have been
                aborted by the user.
        """
        raise NotImplementedError

    def get_commit_message(self, revisions: SCMClientRevisionSpec) -> Optional[SCMClientCommitMessage]:
        """Return the commit message from the commits in the given revisions.

        This pulls out the first line from the commit messages of the given
        revisions. That is then used as the summary.

        Args:
            revisions (dict):
                A dictionary as returned by :py:meth:`parse_revision_spec`.

        Returns:
            dict:
            A dictionary containing keys found in
            :py:class:`SCMClientCommitMessage`.

            This may be ``None``, if no commit message is found.
        """
        commit_message = self.get_raw_commit_message(revisions)
        lines = commit_message.splitlines()
        if not lines:
            return None
        result: SCMClientCommitMessage = {'summary': lines[0]}
        if len(lines) >= 3 and lines[0] and (not lines[1]):
            result['description'] = '\n'.join(lines[2:]).strip()
        else:
            result['description'] = commit_message
        return result

    @deprecate_non_keyword_only_args(RemovedInRBTools50Warning)
    def delete_branch(self, branch_name: str, *, merged_only: bool=True) -> None:
        """Delete the specified branch.

        Args:
            branch_name (str):
                The name of the branch to delete.

            merged_only (bool, optional):
                Whether to limit branch deletion to only those branches which
                have been merged into the current HEAD.
        """
        raise NotImplementedError

    @deprecate_non_keyword_only_args(RemovedInRBTools50Warning)
    def merge(self, *, target: str, destination: str, message: str, author: PatchAuthor, squash: bool=False, run_editor: bool=False, close_branch: bool=True) -> None:
        """Merge the target branch with destination branch.

        Args:
            target (str):
                The name of the branch to merge.

            destination (str):
                The name of the branch to merge into.

            message (str):
                The commit message to use.

            author (rbtools.clients.base.patch.PatchAuthor):
                The author of the commit.

            squash (bool, optional):
                Whether to squash the commits or do a plain merge.

            run_editor (bool, optional):
                Whether to run the user's editor on the commmit message before
                committing.

            close_branch (bool, optional):
                Whether to close/delete the merged branch.

        Raises:
            rbtools.clients.errors.MergeError:
                An error occurred while merging the branch.
        """
        raise NotImplementedError

    def push_upstream(self, remote_branch: str) -> None:
        """Push the current branch to upstream.

        Args:
            remote_branch (str):
                The name of the branch to push to.

        Raises:
            rbtools.client.errors.PushError:
                The branch was unable to be pushed.
        """
        raise NotImplementedError

    def get_raw_commit_message(self, revisions: SCMClientRevisionSpec) -> str:
        """Extract the commit messages on the commits in the given revisions.

        Derived classes should override this method in order to allow callers
        to fetch commit messages. This is needed for description guessing.

        If a derived class is unable to fetch the description, ``None`` should
        be returned.

        Callers that need to differentiate the summary from the description
        should instead use get_commit_message().

        Args:
            revisions (dict):
                A dictionary containing ``base`` and ``tip`` keys.

        Returns:
            str:
            The commit messages of all commits between (base, tip].
        """
        raise NotImplementedError

    def get_current_branch(self) -> str:
        """Return the repository branch name of the current directory.

        Derived classes should override this method if they are able to
        determine the current branch of the working directory.

        Returns:
            str:
            A string with the name of the current branch. If the branch is
            unable to be determined, returns ``None``.
        """
        raise NotImplementedError

    def supports_empty_files(self) -> bool:
        """Return whether the server supports added/deleted empty files.

        Returns:
            bool:
            ``True`` if the Review Board server supports added or deleted empty
            files.
        """
        return False

    @deprecate_non_keyword_only_args(RemovedInRBTools50Warning)
    def apply_patch_for_empty_files(self, patch: bytes, *, p_num: str, revert: bool=False) -> bool:
        """Return whether any empty files in the patch are applied.

        Args:
            patch (bytes):
                The contents of the patch.

            p_num (str):
                The prefix level of the diff.

            revert (bool, optional):
                Whether the patch should be reverted rather than applied.

        Returns:
            bool:
            ``True`` if there are empty files in the patch. ``False`` if there
            were no empty files, or if an error occurred while applying the
            patch.
        """
        raise NotImplementedError

    @deprecate_non_keyword_only_args(RemovedInRBTools50Warning)
    def amend_commit_description(self, message: str, *, revisions: Optional[SCMClientRevisionSpec]=None) -> None:
        """Update a commit message to the given string.

        Args:
            message (str):
                The commit message to use when amending the commit.

            revisions (dict, optional):
                A dictionary of revisions, as returned by
                :py:meth:`parse_revision_spec`. This provides compatibility
                with SCMs that allow modifications of multiple changesets at
                any given time, and will amend the change referenced by the
                ``tip`` key.

        Raises:
            rbtools.clients.errors.AmendError:
                The amend operation failed.
        """
        raise NotImplementedError