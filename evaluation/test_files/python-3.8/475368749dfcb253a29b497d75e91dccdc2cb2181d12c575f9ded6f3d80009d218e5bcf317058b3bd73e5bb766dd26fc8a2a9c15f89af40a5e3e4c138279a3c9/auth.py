"""Authorization ruleset handling.

The :class:`UserScopes` class handles whether a dataset, table or field can be accessed.
The other classes in this module ease to retrieval of permission objects.
"""
from __future__ import annotations
from typing import Iterable, Iterator
import methodtools
from schematools.types import DatasetFieldSchema, DatasetSchema, DatasetTableSchema, Permission, PermissionLevel, ProfileDatasetSchema, ProfileSchema, ProfileTableSchema
PUBLIC_SCOPE = 'OPENBAAR'
__all__ = ('UserScopes',)

class UserScopes:
    """A request-like object that tells what the current user may access.

    A UserScopes encapsulates the scopes on a request and the profiles that apply,
    and performs permission checks against a schema.

    All ``has_...()`` functions are used for permission checks.
    Internally, these read the schema and profile data for the authorization matrix.

    * By default, all fields can be read unless the schema defines an "auth" field.
    * The "auth" flags in schema files act as a blacklist: no access, except for some roles.
    * The "profile" rules open up certain fields, hence whitelist features.
    """

    def __init__(self, query_params: dict[str, object], request_scopes: Iterable[str], all_profiles: Iterable[ProfileSchema] | None=None):
        """Initialize the user scopes object.

        Args:
            query_params: The search query filter (e.g. request.GET).
            request_scopes: The scopes granted to a request.
                Presence of the public scope "OPENBAAR" is implied.
            all_profiles: All profiles that need to be loaded.
                If not None, this iterable is stored and converted to list
                the first time it is needed.
        """
        self._query_param_names = [param for (param, value) in query_params.items() if value]
        self._all_profiles = all_profiles
        self._scopes = set(request_scopes) | {PUBLIC_SCOPE}

    def __repr__(self):
        return f'<UserScopes: {self._scopes!r}>'

    def __iter__(self) -> Iterator[str]:
        return iter(self._scopes)

    def add_query_params(self, params: list[str]):
        """Tell that the request has extra (implicit) parameters that are satisfied.

        For example, the detail URL of a resource already implicitly passes the
        identifier of a resource. Hence, this parameter no longer needs to be given
        found in any additional search filters or query string.
        """
        self._query_param_names.extend(params)

    @methodtools.lru_cache()
    def has_all_scopes(self, *needed_scopes: str) -> bool:
        """Check whether the request has all scopes.

        This performs an AND check: all scopes should be present.
        """
        return self._scopes.issuperset(needed_scopes)

    @methodtools.lru_cache()
    def has_any_scope(self, *needed_scopes: str) -> bool:
        """Check whether the request grants one of the given scopes.

        This performs an OR check: having one of the scopes gives access.
        """
        needed_scopes = set(needed_scopes)
        return any((scope in needed_scopes for scope in self._scopes))

    def has_dataset_access(self, dataset: DatasetSchema) -> Permission:
        """Tell whether a dataset can be accessed."""
        return self._has_dataset_auth_access(dataset) or self._has_dataset_profile_access(dataset.id)

    def has_table_access(self, table: DatasetTableSchema) -> Permission:
        """Tell whether a table can be accessed, and return the permission level."""
        return self._has_table_auth_access(table) or self._has_table_profile_access(table)

    def has_field_access(self, field: DatasetFieldSchema) -> Permission:
        """Tell whether a field may be read."""
        return self._has_field_auth_access(field) or self._has_field_profile_access(field)

    def _has_dataset_auth_access(self, dataset: DatasetSchema) -> Permission:
        """Tell whether the 'auth' rules give access to the dataset."""
        if self.has_any_scope(*dataset.auth):
            return Permission(PermissionLevel.highest, source='dataset.auth')
        else:
            return Permission.none

    def _has_table_auth_access(self, table: DatasetTableSchema) -> Permission:
        """Tell whether the 'auth' rules give access to the table."""
        if self.has_any_scope(*table.auth) and self.has_any_scope(*table.dataset.auth):
            return Permission(PermissionLevel.highest, source='table.auth' if table.auth else 'dataset.auth')
        else:
            return Permission.none

    def _has_field_auth_access(self, field: DatasetFieldSchema) -> Permission:
        """Tell whether the 'auth' rules give access to the table."""
        if self.has_any_scope(*field.auth) and self.has_any_scope(*field.table.auth) and self.has_any_scope(*field.table.dataset.auth):
            return Permission(PermissionLevel.highest, source='field.auth' if field.auth else 'table.auth' if field.table.auth else 'dataset.auth')
        else:
            return Permission.none

    @methodtools.lru_cache()
    def _has_dataset_profile_access(self, dataset_id: str) -> Permission:
        """Give the permission access level for a dataset, as defined by the profile."""
        return max((profile_dataset.permissions for profile_dataset in self.get_active_profile_datasets(dataset_id)), default=Permission.none)

    @methodtools.lru_cache()
    def _has_table_profile_access(self, table: DatasetTableSchema) -> Permission:
        """Give the permission level for a table.

        When a dataset defines global permissions without explicitly mentioning the table,
        these permissions are "inherited" and used.
        """
        dataset_id = table.dataset.id
        table_id = table.id
        max_permission = Permission.none
        for profile_dataset in self.get_active_profile_datasets(dataset_id):
            if max_permission.level == PermissionLevel.highest:
                break
            profile_table = profile_dataset.tables.get(table_id, None)
            if profile_table is None:
                if (dataset_permission := profile_dataset.permissions):
                    max_permission = max(max_permission, dataset_permission)
            elif self._may_include_profile_table(profile_table):
                max_permission = max(max_permission, profile_table.permissions)
        return max_permission

    def _has_field_profile_access(self, field: DatasetFieldSchema) -> Permission:
        """Give the permission level for a field based on a profile.

        Fields have a special case: if a specific permission is defined, use that.
        This may "limit" the actual permission. For example, the table gives "read" permission,
        but the field may state "encoded" as the level. Since a default is defined for the field,
        that's being used.
        """
        field_id = field.id
        table_id = field.table.id
        max_permission = Permission.none
        for profile_dataset in self.get_active_profile_datasets(field.table.dataset.id):
            if max_permission.level == PermissionLevel.highest:
                break
            profile_table = profile_dataset.tables.get(table_id, None)
            if profile_table is None:
                if (dataset_permission := profile_dataset.permissions):
                    max_permission = max(max_permission, dataset_permission)
                continue
            if not self._may_include_profile_table(profile_table):
                continue
            try:
                field_permission = profile_table.fields[field_id]
            except KeyError:
                table_permission = profile_table.permissions
                if table_permission and table_permission.level > PermissionLevel.SUBOBJECTS_ONLY:
                    max_permission = max(max_permission, table_permission)
                continue
            max_permission = max(max_permission, field_permission)
        return max_permission

    @methodtools.lru_cache()
    def get_active_profile_datasets(self, dataset_id: str) -> list[ProfileDatasetSchema]:
        """Find all profiles that mention a dataset and match the scopes.

        This already checks whether the mandatory user scopes are set.
        """
        if self._all_profiles is None:
            self._all_profiles = []
        elif not isinstance(self._all_profiles, list):
            self._all_profiles = list(self._all_profiles)
        return [profile_dataset for profile in self._all_profiles if self.has_all_scopes(*profile.scopes) and (profile_dataset := profile.datasets.get(dataset_id)) is not None]

    @methodtools.lru_cache()
    def get_active_profile_tables(self, dataset_id: str, table_id: str) -> list[ProfileTableSchema]:
        """Find all profiles that mention a particular table and give access.

        This already checks whether the table passes the `mandatoryFilterSets` check,
        and whether the scopes of the dataset match.
        """
        return [profile_table for profile_dataset in self.get_active_profile_datasets(dataset_id) if (profile_table := profile_dataset.tables.get(table_id)) is not None and self._may_include_profile_table(profile_table)]

    def _may_include_profile_table(self, profile_table: ProfileTableSchema):
        """Check whether the table rules are applicable to the current user.

        This checks whether any of the mandatory filtersets from a ProfileTableSchema were queried.
        """
        mandatory_filtersets = profile_table.mandatory_filtersets
        return not mandatory_filtersets or any((_match_filter_rule(rule, self._query_param_names) for rule in mandatory_filtersets))

def _match_filter_rule(rule: Iterable[str], query_param_names: Iterable[str]) -> bool:
    """Tell whether a mandatory filter rule is matched.

    This happens when ALL required filters are present in the query string.
    """
    return all((filter_name in query_param_names for filter_name in rule))