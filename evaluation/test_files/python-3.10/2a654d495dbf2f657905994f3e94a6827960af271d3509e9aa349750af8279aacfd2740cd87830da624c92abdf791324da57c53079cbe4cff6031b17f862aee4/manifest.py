import abc
from typing import FrozenSet, Generic
from micropy.stubs.package import AnyStubPackage, StubPackage
from micropy.stubs.repository_info import RepositoryInfo
from pydantic import Field
from pydantic.generics import GenericModel
from typing_extensions import Annotated

class StubsManifest(GenericModel, Generic[AnyStubPackage], abc.ABC):

    class Config:
        frozen = True
    repository: RepositoryInfo
    packages: Annotated[FrozenSet[AnyStubPackage], Field(repr=False)]

    @abc.abstractmethod
    def resolve_package_url(self, package: StubPackage) -> str:
        """Resolve package to a stub source."""

    def resolve_package_absolute_name(self, package: StubPackage) -> str:
        """Resolve package absolute name."""
        return '/'.join([self.repository.name, package.name])

    def resolve_package_versioned_name(self, package: StubPackage) -> str:
        """Resolve package versioned absolute name."""
        return '-'.join([package.name, package.version])

    def resolve_package_absolute_versioned_name(self, package: StubPackage) -> str:
        """Resolve package versioned absolute name."""
        return '-'.join([self.resolve_package_absolute_name(package), package.version])