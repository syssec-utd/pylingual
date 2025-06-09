from __future__ import annotations
import attr
import os
import re
from contextlib import contextmanager
from dataclasses import dataclass
from typing import List, Optional, Union, cast
_SPLIT_VERSION_FROM_COMMENT_PATTERN = re.compile('(?:\\s*)(!)?(?:\\s*)([^\\s]+)(?:\\s*#\\s*(.*))?')
_SEMANTIC_VERSION_PATTERN = re.compile('(\\d+).(\\d+).(\\d+)([^\\s]*)')

@dataclass(frozen=True, repr=False, order=False)
class NonSemanticVersion:
    supported: bool
    version: str
    comment: str

    def __eq__(self, other):
        if not isinstance(other, NonSemanticVersion):
            return False
        return self.version == other.version

    def __lt__(self, other):
        if not isinstance(other, NonSemanticVersion):
            return False
        return self.version < other.version

    def __repr__(self):
        return f"{('' if self.supported else '!')}{self.version}{(' # ' + self.comment if self.comment else '')}"

@dataclass(frozen=True, repr=False, order=False)
class SemanticVersion:
    supported: bool
    version: str
    major: int
    minor: int
    patch: int
    suffix: str
    comment: str

    def __eq__(self, other):
        if not isinstance(other, SemanticVersion):
            return False
        return self.major == other.major and self.minor == other.minor and (self.patch == other.patch) and (self.suffix == other.suffix)

    def __lt__(self, other):
        if not isinstance(other, SemanticVersion):
            return True
        if self.major < other.major:
            return True
        if self.major > other.major:
            return False
        if self.minor < other.minor:
            return True
        if self.minor > other.minor:
            return False
        if self.patch < other.patch:
            return True
        if self.patch > other.patch:
            return False
        if not self.suffix and other.suffix:
            return True
        if self.suffix and (not other.suffix):
            return False
        return self.suffix < other.suffix

    def __repr__(self):
        return f"{('' if self.supported else '!')}{self.version}{(' # ' + self.comment if self.comment else '')}"

def parse_version(version: str) -> Union[SemanticVersion, NonSemanticVersion]:
    res = re.search(_SPLIT_VERSION_FROM_COMMENT_PATTERN, version)
    if not res:
        raise Exception(f'Version does not parse as non-semantic: {version}')
    (supported_string, version_string, comment) = res.groups()
    supported = not bool(supported_string)
    res = re.search(_SEMANTIC_VERSION_PATTERN, version_string)
    if res:
        (major, minor, patch, suffix) = res.groups()
        return SemanticVersion(supported=supported, version=version_string, major=int(major), minor=int(minor), patch=int(patch), suffix=suffix, comment=comment)
    return NonSemanticVersion(supported=supported, version=version_string, comment=comment)

@attr.s(frozen=True)
class TestedVersions:
    versions: List[Union[SemanticVersion, NonSemanticVersion]] = attr.ib(converter=sorted)

    @staticmethod
    def _add_version_to_file(directory: str, dependency_name: str, dependency_version: str, supported: bool):
        dependency_file_path = TestedVersions.get_file_path(directory, dependency_name)
        TestedVersions.add_version_to_file(dependency_file_path, dependency_version, supported)

    @staticmethod
    def add_version_to_file(path: str, version: str, supported: bool):
        tested_versions = TestedVersions.from_file(path)
        parsed_version = parse_version(('' if supported else '!') + version)
        previous_version: Optional[Union[SemanticVersion, NonSemanticVersion]] = None
        try:
            previous_version = next(filter(lambda v: v.version == parsed_version.version, tested_versions.versions))
        except StopIteration:
            pass
        tested_versions.versions.append(parsed_version)
        if previous_version:
            tested_versions.versions.remove(previous_version)
            print(f"Updating '{previous_version}' to '{parsed_version}' in {path}")
            if previous_version.supported and (not parsed_version.supported):
                print(f'DANGER! Removing support for {previous_version.version}!')
            if not previous_version.supported and parsed_version.supported:
                print(f'COOL! Adding support for {previous_version.version}!')
        else:
            print(f"Adding '{parsed_version}' to {path}")
        with open(path, 'w') as f:
            for tested_version in sorted(tested_versions.versions):
                if not tested_version.supported:
                    f.write('!')
                f.write(tested_version.version)
                if tested_version.comment:
                    f.write(' # ' + tested_version.comment)
                f.write('\n')

    @staticmethod
    @contextmanager
    def save_tests_result(directory: str, dependency_name: str, dependency_version: str):
        if should_test_only_untested_versions():
            try:
                yield
            except Exception:
                TestedVersions._add_version_to_file(directory, dependency_name, dependency_version, False)
                raise
            TestedVersions._add_version_to_file(directory, dependency_name, dependency_version, True)
        else:
            yield

    @staticmethod
    def get_file_path(directory: str, dependency_name: str) -> str:
        return os.path.dirname(os.path.dirname(__file__)) + f'/test/integration/{directory}/tested_versions/{dependency_name}'

    @staticmethod
    def from_file(path: str) -> TestedVersions:
        with open(path, 'r') as f:
            return TestedVersions([parse_version(line) for line in f])

    @property
    def supported_versions(self) -> List[str]:
        """Return all supported versions, sorted"""
        return [tested_version.version for tested_version in self.versions if tested_version.supported]

    @property
    def unsupported_versions(self) -> List[str]:
        """Return all unsupported versions, sorted"""
        return [tested_version.version for tested_version in self.versions if not tested_version.supported]

    @property
    def all_versions(self) -> List[str]:
        """Return all versions, sorted"""
        return [tested_version.version for tested_version in self.versions]

def should_test_only_untested_versions() -> bool:
    return os.getenv('TEST_ONLY_UNTESTED_NEW_VERSIONS', '').lower() == 'true'

def generate_support_matrix_markdown(src_root=None, package_url_template='https://pypi.org/project/{}') -> List[str]:
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    if src_root:
        project_root = os.path.join(project_root, src_root)
    package_support_version_directories = []
    for (root, directories, files) in os.walk(project_root):
        for directory in directories:
            if os.path.basename(directory) == 'tested_versions':
                package_support_version_directories += [os.path.join(root, directory)]
    res = ['| Instrumentation | Package | Supported Versions |', '| --- | --- | --- |']
    for package_support_version_directory in sorted(package_support_version_directories):
        res += _generate_support_matrix_markdown_row(package_support_version_directory, package_url_template)
    return res

def _generate_support_matrix_markdown_row(tested_versions_directory, package_url_template) -> List[str]:
    """Generate the markdown row for an instrumentation"""
    instrumentation = os.path.basename(os.path.dirname(tested_versions_directory))
    packages = sorted(os.listdir(tested_versions_directory))
    res = []
    if len(packages) == 1:
        package = packages[0]
        supported_version_ranges = _get_supported_version_ranges(TestedVersions.from_file(os.path.join(tested_versions_directory, packages[0])))
        res.append(f'| {instrumentation} | [{package}]({package_url_template.format(package)}) | {supported_version_ranges[0]} |')
        for supported_version_range in supported_version_ranges[1:]:
            res.append(f'| | | {supported_version_range} |')
    else:
        first_package = packages[0]
        supported_version_ranges_first_package = _get_supported_version_ranges(TestedVersions.from_file(os.path.join(tested_versions_directory, first_package)))
        res.append(f'| {instrumentation} | [{first_package}]({package_url_template.format(first_package)}) | {supported_version_ranges_first_package[0]} |')
        for supported_version_range in supported_version_ranges_first_package[1:]:
            res.append(f'| | | {supported_version_range} |')
        for package in packages[1:]:
            supported_version_ranges = _get_supported_version_ranges(TestedVersions.from_file(os.path.join(tested_versions_directory, package)))
            res.append(f'| | [{package}]({package_url_template.format(package)}) | {supported_version_ranges[0]} |')
            for supported_version_range in supported_version_ranges[1:]:
                res.append(f'| | | {supported_version_range} |')
    return res

def _get_supported_version_ranges(tested_versions: TestedVersions) -> List[str]:
    version_ranges = []
    current_range: List[Union[NonSemanticVersion, SemanticVersion]] = []
    for current_version in tested_versions.versions:
        if not current_range:
            if current_version.supported:
                current_range = [current_version]
                continue
            else:
                continue
        if not current_version.supported:
            version_ranges.append(_version_range_to_string(current_range))
            current_range = []
            continue
        if isinstance(current_version, NonSemanticVersion):
            version_ranges.append(_version_range_to_string(current_range))
            current_range = [current_version]
            continue
        if cast(SemanticVersion, current_range[0]).major < current_version.major:
            version_ranges.append(_version_range_to_string(current_range))
            current_range = [current_version]
            continue
        current_range.append(current_version)
    if current_range:
        version_ranges.append(_version_range_to_string(current_range))
    return version_ranges

def _version_range_to_string(version_range: List[Union[NonSemanticVersion, SemanticVersion]]) -> str:
    if len(version_range) == 1:
        return version_range[0].version
    first_version = cast(SemanticVersion, version_range[0])
    last_version = cast(SemanticVersion, version_range[len(version_range) - 1])
    return f'{first_version.major}.{first_version.minor}.{first_version.patch}{first_version.suffix}~{last_version.major}.{last_version.minor}.{last_version.patch}{last_version.suffix}'