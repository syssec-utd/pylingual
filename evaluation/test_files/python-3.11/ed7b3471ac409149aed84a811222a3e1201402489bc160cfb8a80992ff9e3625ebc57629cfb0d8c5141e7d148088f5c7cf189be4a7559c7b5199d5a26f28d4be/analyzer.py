"""Analyze authorization for MongoDB.

Database users:
Users are defined in the project level.
Type of users:
    Local users - users who are defined in the Atlas.
    LDAP users - users who are defined in the LDAP.
    X.509 users - users who are defined in the X.509.
Roles have scope:
    Database - All databases in the cluster
    Collection - All collections in the database.
"""
from dataclasses import dataclass
from logging import Logger
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union
from pymongo import MongoClient
from authz_analyzer.datastores.mongodb.atlas.model import OrganizationUser
from authz_analyzer.datastores.mongodb.model import AdminRole, AdminUser, Privilege, Role
from authz_analyzer.datastores.mongodb.resolvers import get_permission_level, get_permission_level_cluster, get_permission_level_privilege
from authz_analyzer.datastores.mongodb.service import MongoDBService
from authz_analyzer.datastores.mongodb.service_model import UserEntry
from authz_analyzer.models.model import Asset, AssetType, AuthzEntry, AuthzNote, AuthzPathElement, AuthzPathElementType, Identity, IdentityType, PermissionLevel
from authz_analyzer.utils.logger import get_logger
from authz_analyzer.writers import BaseWriter, OutputFormat
from authz_analyzer.writers.base_writers import DEFAULT_OUTPUT_FILE
from authz_analyzer.writers.get_writers import get_writer
PermissionOrganizationUserMap = Dict[PermissionLevel, Set[OrganizationUser]]

@dataclass
class MongoDBAuthzAnalyzer:
    """Analyze authorization for MongoDB.
    MongoDB Python client doesn't support Atlas admin API.
    Need to access MongoDB Atlas REST directly.
    Need to enable it https://www.mongodb.com/docs/atlas/configure-api-access/
    https://www.mongodb.com/docs/atlas/configure-api-access/#std-label-create-org-api-key
    Organization read only.
    """
    client: MongoDBService
    writer: BaseWriter
    logger: Logger

    @classmethod
    def connect(cls, host: str, username: str, password: str, output_format: OutputFormat=OutputFormat.CSV, output_path: Union[Path, str]=Path.cwd() / DEFAULT_OUTPUT_FILE, logger: Optional[Logger]=None, ssl: bool=True, **kwargs: Any):
        """Connect to MongoDB.

        Args:
            host (str): hostname of the mongodb server
            username (str): username
            password (str): password
            output_format (OutputFormat, optional): Output format. Defaults to OutputFormat.CSV.
            output_path (Union[Path, str], optional): Output path. Defaults to Path.cwd()/DEFAULT_OUTPUT_FILE.
            logger (Optional[Logger], optional): Logger. Defaults to None.

        Raises:
            ConnectionError: Unable to connect

        Returns:
            MongoDBAuthzAnalyzer: Analyzer
        """
        writer = get_writer(filename=output_path, output_format=output_format)
        try:
            client = MongoDBService(MongoClient(host, username=username, password=password, tls=ssl, **kwargs))
        except Exception as err:
            raise ConnectionError(f'Could not connect to {host} with the provided credentials') from err
        if logger is None:
            logger = get_logger(False)
        return cls(writer=writer, logger=logger, client=client)

    def run(self):
        """Analyze authorization for a user and resource."""
        admin_users = self._handle_admin_users()
        for database_name, db_connection in self.client.iter_database_connections():
            if database_name == 'admin':
                continue
            users = self.client.get_users(db_connection)
            collections = db_connection.list_collection_names()
            custom_roles = self.client.get_custom_roles(db_connection)
            self._report_users(database_name=database_name, users=users, collections=collections, admin_users=admin_users, custom_roles=custom_roles)

    def _handle_admin_users(self) -> Set[AdminUser]:
        """Get admin users."""
        admin_db = self.client.client['admin']
        admin_users = self.client.get_users(admin_db)
        custom_roles = self.client.get_custom_roles(admin_db)
        fileted_admin_users: Set[AdminUser] = set()
        for user in admin_users:
            relevant_admin_user = MongoDBAuthzAnalyzer._get_relevant_admin_user(user, custom_roles)
            if relevant_admin_user is not None:
                fileted_admin_users.add(relevant_admin_user)
        collections = admin_db.list_collection_names()
        self._report_users(database_name='admin', users=admin_users, collections=collections, admin_users=fileted_admin_users, custom_roles=custom_roles)
        return fileted_admin_users

    @staticmethod
    def _get_relevant_admin_user(user: UserEntry, custom_roles: Dict[str, Role]) -> Optional[AdminUser]:
        """If None, the user is not relevant to us."""
        roles: Set[AdminRole] = set()
        for role in user['roles']:
            permission_level = get_permission_level_cluster(role['role'])
            custom_role = custom_roles.get(role['role'])
            role_path_element = AuthzPathElement(id=role['role'], name=role['role'], type=AuthzPathElementType.ROLE)
            if permission_level is not None:
                role_path_element.notes.append(AuthzNote.to_generic_note(MongoDBAuthzAnalyzer._generate_note_user(user['user'], role['role'], permission_level, 'all databases')))
                roles.add(AdminRole(permission_level=permission_level, name=role['role'], path=[role_path_element]))
            elif custom_role is not None:
                role_path_element.notes.append(AuthzNote.to_generic_note(MongoDBAuthzAnalyzer._generate_note_user(user['user'], role['role'])))
                for admin_role in MongoDBAuthzAnalyzer._iter_admin_custom_role(custom_roles, custom_role, path=[role_path_element]):
                    roles.add(admin_role)
        if len(roles) != 0:
            return AdminUser(name=user['user'], roles=roles, id=user['user'])
        return None

    @staticmethod
    def _iter_admin_custom_role(custom_roles: Dict[str, Role], role: Role, path: List[AuthzPathElement]):
        """Looks on the role permissions, if it permits access on all databases it will yield the role.
        if not will look in inherited roles, if they are built in roles which provides access to all databases it will yield the role.
        if the inherited role is a custom role, it will do a recursive.

        Args:
            custom_roles (Dict[str, Role]): role name to custom role map
            role (Role): custom role

        Returns:
            None: None

        Yields:
            AdminRole: a single admin role
        """
        for priv in role.privileges:
            permission_level = MongoDBAuthzAnalyzer._get_highest_permission(privilege=priv, collection='')
            if permission_level is not None:
                if len(path[-1].notes) > 0:
                    path[-1].notes[0].note += f' which grants permission {permission_level} on all databases'
                else:
                    path[-1].notes = [AuthzNote.to_generic_note(f' which grants permission {permission_level} on all databases')]
                yield AdminRole(permission_level=permission_level, name=role.name, path=path)
        for inherited_role in role.inherited_roles:
            permission_level = get_permission_level_cluster(inherited_role.name)
            custom_role = custom_roles.get(inherited_role.name)
            role_path_element = AuthzPathElement(id=inherited_role.name, name=inherited_role.name, type=AuthzPathElementType.ROLE)
            if permission_level is not None:
                role_path_element.notes.append(AuthzNote.to_generic_note(f'role {role.name} inherits role {inherited_role.name} which grants permission {permission_level} on all databases'))
                path.append(role_path_element)
                yield AdminRole(permission_level=permission_level, name=role.name, path=path)
            if custom_role is not None:
                role_path_element.notes.append(AuthzNote.to_generic_note(f'role {role.name} inherits role {inherited_role.name}'))
                path.append(role_path_element)
                MongoDBAuthzAnalyzer._iter_admin_custom_role(custom_roles, custom_role, path=path)

    def _report_users(self, database_name: str, users: List[UserEntry], collections: List[str], admin_users: Set[AdminUser], custom_roles: Dict[str, Role]):
        for collection in collections:
            asset = Asset(type=AssetType.COLLECTION, name=[database_name, collection])
            for user in users:
                self._report_user(user=user, asset=asset, custom_roles=custom_roles, database_name=database_name, collection=collection)
            for admin_user in admin_users:
                self._report_admin_user(user=admin_user, asset=asset)

    def _report_user(self, user: UserEntry, asset: Asset, custom_roles: Dict[str, Role], database_name: str, collection: str):
        for role in user['roles']:
            custom_role = custom_roles.get(role['role'])
            if custom_role is not None:
                self._handle_custom_role_privileges(custom_role, user=user, asset=asset, database_name=database_name, collection=collection, custom_roles=custom_roles, path=[])
            permission = get_permission_level(role['role'])
            if permission is not None:
                notes = [AuthzNote.to_generic_note(MongoDBAuthzAnalyzer._generate_note_user(user['user'], role['role'], permission, database_name + '.' + collection))]
                path = [AuthzPathElement(type=AuthzPathElementType.ROLE, name=role['role'], id=role['role'], notes=notes)]
                self._write_entry(user_id=user['user'], username=user['user'], asset=asset, permission=permission, path=path)

    def _handle_custom_role_privileges(self, custom_role: Role, user: UserEntry, asset: Asset, database_name: str, collection: str, custom_roles: Dict[str, Role], path: List[AuthzPathElement]):
        path.append(AuthzPathElement(type=AuthzPathElementType.ROLE, name=custom_role.name, id=custom_role.name))
        highest_permission_level: Optional[PermissionLevel] = None
        for inherited_role in custom_role.inherited_roles:
            role = custom_roles.get(inherited_role.name)
            if role is None:
                permission = get_permission_level(inherited_role.name)
                if permission is not None:
                    path.append(AuthzPathElement(type=AuthzPathElementType.ROLE, name=inherited_role.name, id=inherited_role.name))
                    self._write_entry(user_id=user['user'], username=user['user'], asset=asset, permission=permission, path=path)
                    path.pop()
            else:
                self._handle_custom_role_privileges(role, user=user, asset=asset, database_name=database_name, collection=collection, custom_roles=custom_roles, path=path)
        for privilege in custom_role.privileges:
            if privilege.resource.database == database_name:
                highest_permission_level = MongoDBAuthzAnalyzer._get_highest_permission(privilege, collection)
                path[-1].db_permissions = privilege.actions
                if highest_permission_level is not None:
                    self._write_entry(user_id=user['user'], username=user['user'], asset=asset, permission=highest_permission_level, path=path)
        path.pop()

    @staticmethod
    def _get_highest_permission(privilege: Privilege, collection: str):
        highest_permission_level: Optional[PermissionLevel] = None
        if privilege.resource.collection in ('', collection):
            for action in privilege.actions:
                permission = get_permission_level_privilege(action)
                if permission is not None:
                    if highest_permission_level is None or permission > highest_permission_level:
                        highest_permission_level = permission
        return highest_permission_level

    def _report_admin_user(self, user: AdminUser, asset: Asset):
        for role in user.roles:
            self._write_entry(user_id=user.id, username=user.name, asset=asset, permission=role.permission_level, path=role.path)

    def _write_entry(self, user_id: str, username: str, asset: Asset, permission: PermissionLevel, path: List[AuthzPathElement]):
        """Writes the entry to the writer.

        Args:
            user_id (str): User ID
            username (str): Name of the user
            asset (Asset): The asset as required by the base writer, usually a collection
            permission (PermissionLevel): Permission level, enum
            path (List[AuthzPathElement]): Path from identity to asset
            original_role (str): Original role name, the role which grants the permission to the asset
        """
        identity = Identity(id=user_id, type=IdentityType.USER, name=username)
        self.writer.write_entry(AuthzEntry(identity=identity, asset=asset, permission=permission, path=path))

    @staticmethod
    def _generate_note_user(user: str, role: str, permission_level: Optional[PermissionLevel]=None, resource: Optional[str]=None):
        note = f'user {user} has role {role}'
        if resource is not None and permission_level is not None:
            note += f' which grants permission {permission_level} on {resource}'
        return note