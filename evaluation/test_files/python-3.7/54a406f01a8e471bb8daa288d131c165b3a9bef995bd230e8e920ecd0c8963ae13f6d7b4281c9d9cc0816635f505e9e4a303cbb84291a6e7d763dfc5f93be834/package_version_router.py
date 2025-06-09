from typing import Callable, Optional
from fastapi import APIRouter, Depends
import re
from watchmen_auth import PrincipalService
from watchmen_meta.common import ask_meta_storage, ask_snowflake_generator, PackageVersionService
from watchmen_model.admin import UserRole
from watchmen_model.system import PackageVersion
from watchmen_rest import get_admin_principal
from watchmen_rest.util import raise_403, validate_tenant_id
from watchmen_rest_doll.util import trans
router = APIRouter()

@router.post('/package_version', tags=[UserRole.ADMIN], response_model=PackageVersion)
async def save_topic(package_version: PackageVersion, principal_service: PrincipalService=Depends(get_admin_principal)) -> PackageVersion:
    validate_tenant_id(package_version, principal_service)
    package_version_service = get_package_version_service(principal_service)
    action = ask_save_version_action(package_version_service, principal_service)
    return trans(package_version_service, lambda : action(package_version))

def get_package_version_service(principal_service: PrincipalService) -> PackageVersionService:
    return PackageVersionService(ask_meta_storage(), ask_snowflake_generator(), principal_service)

def ask_save_version_action(package_version_service: PackageVersionService, principal_service: PrincipalService) -> Callable[[PackageVersion], PackageVersion]:

    def action(package_version: PackageVersion) -> PackageVersion:

        def is_invalid_package_version(version: str) -> bool:
            pattern = '^([1-9]\\d|[1-9])(\\.([1-9]\\d|\\d)){2}$'
            if re.match(pattern, version):
                return False
            else:
                return True
        if is_invalid_package_version(package_version.currVersion) or is_invalid_package_version(package_version.preVersion):
            raise ValueError(f'package version is invalid, current version is {package_version.currVersion}, previous version is {package_version.preVersion}')
        if package_version_service.is_storable_id_faked(package_version.versionId):
            package_version_service.redress_storable_id(package_version)
            package_version: PackageVersion = package_version_service.insert_one(package_version)
        else:
            existing_version: Optional[PackageVersion] = package_version_service.get_package_version_by_id(package_version.versionId)
            if existing_version is not None:
                if existing_version.tenantId != package_version.tenantId:
                    raise_403()
            package_version: PackageVersion = package_version_service.update(package_version)
        return package_version
    return action