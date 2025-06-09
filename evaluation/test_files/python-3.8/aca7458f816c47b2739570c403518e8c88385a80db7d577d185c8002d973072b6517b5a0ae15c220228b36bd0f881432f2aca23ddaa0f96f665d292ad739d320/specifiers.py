import abc
import functools
import itertools
import re
import warnings
from typing import Callable, Dict, Iterable, Iterator, List, Optional, Pattern, Set, Tuple, TypeVar, Union
from .utils import canonicalize_version
from .version import LegacyVersion, Version, parse
ParsedVersion = Union[Version, LegacyVersion]
UnparsedVersion = Union[Version, LegacyVersion, str]
VersionTypeVar = TypeVar('VersionTypeVar', bound=UnparsedVersion)
CallableOperator = Callable[[ParsedVersion, str], bool]

class InvalidSpecifier(ValueError):
    """
    An invalid specifier was found, users should refer to PEP 440.
    """

class BaseSpecifier(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __str__(self) -> str:
        """
        Returns the str representation of this Specifier like object. This
        should be representative of the Specifier itself.
        """

    @abc.abstractmethod
    def __hash__(self) -> int:
        """
        Returns a hash value for this Specifier like object.
        """

    @abc.abstractmethod
    def __eq__(self, other: object) -> bool:
        """
        Returns a boolean representing whether or not the two Specifier like
        objects are equal.
        """

    @abc.abstractmethod
    def __ne__(self, other: object) -> bool:
        """
        Returns a boolean representing whether or not the two Specifier like
        objects are not equal.
        """

    @abc.abstractproperty
    def prereleases(self) -> Optional[bool]:
        """
        Returns whether or not pre-releases as a whole are allowed by this
        specifier.
        """

    @prereleases.setter
    def prereleases(self, value: bool) -> None:
        """
        Sets whether or not pre-releases as a whole are allowed by this
        specifier.
        """

    @abc.abstractmethod
    def contains(self, item: str, prereleases: Optional[bool]=None) -> bool:
        """
        Determines if the given item is contained within this specifier.
        """

    @abc.abstractmethod
    def filter(self, iterable: Iterable[VersionTypeVar], prereleases: Optional[bool]=None) -> Iterable[VersionTypeVar]:
        """
        Takes an iterable of items and filters them so that only items which
        are contained within this specifier are allowed in it.
        """

class _IndividualSpecifier(BaseSpecifier):
    _operators: Dict[str, str] = {}
    _regex: Pattern[str]

    def __init__(self, spec: str='', prereleases: Optional[bool]=None) -> None:
        match = self._regex.search(spec)
        if not match:
            raise InvalidSpecifier(f"Invalid specifier: '{spec}'")
        self._spec: Tuple[str, str] = (match.group('operator').strip(), match.group('version').strip())
        self._prereleases = prereleases

    def __repr__(self) -> str:
        pre = f', prereleases={self.prereleases!r}' if self._prereleases is not None else ''
        return '<{}({!r}{})>'.format(self.__class__.__name__, str(self), pre)

    def __str__(self) -> str:
        return '{}{}'.format(*self._spec)

    @property
    def _canonical_spec(self) -> Tuple[str, str]:
        return (self._spec[0], canonicalize_version(self._spec[1]))

    def __hash__(self) -> int:
        return hash(self._canonical_spec)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            try:
                other = self.__class__(str(other))
            except InvalidSpecifier:
                return NotImplemented
        elif not isinstance(other, self.__class__):
            return NotImplemented
        return self._canonical_spec == other._canonical_spec

    def __ne__(self, other: object) -> bool:
        if isinstance(other, str):
            try:
                other = self.__class__(str(other))
            except InvalidSpecifier:
                return NotImplemented
        elif not isinstance(other, self.__class__):
            return NotImplemented
        return self._spec != other._spec

    def _get_operator(self, op: str) -> CallableOperator:
        operator_callable: CallableOperator = getattr(self, f'_compare_{self._operators[op]}')
        return operator_callable

    def _coerce_version(self, version: UnparsedVersion) -> ParsedVersion:
        if not isinstance(version, (LegacyVersion, Version)):
            version = parse(version)
        return version

    @property
    def operator(self) -> str:
        return self._spec[0]

    @property
    def version(self) -> str:
        return self._spec[1]

    @property
    def prereleases(self) -> Optional[bool]:
        return self._prereleases

    @prereleases.setter
    def prereleases(self, value: bool) -> None:
        self._prereleases = value

    def __contains__(self, item: str) -> bool:
        return self.contains(item)

    def contains(self, item: UnparsedVersion, prereleases: Optional[bool]=None) -> bool:
        if prereleases is None:
            prereleases = self.prereleases
        normalized_item = self._coerce_version(item)
        if normalized_item.is_prerelease and (not prereleases):
            return False
        operator_callable: CallableOperator = self._get_operator(self.operator)
        return operator_callable(normalized_item, self.version)

    def filter(self, iterable: Iterable[VersionTypeVar], prereleases: Optional[bool]=None) -> Iterable[VersionTypeVar]:
        yielded = False
        found_prereleases = []
        kw = {'prereleases': prereleases if prereleases is not None else True}
        for version in iterable:
            parsed_version = self._coerce_version(version)
            if self.contains(parsed_version, **kw):
                if parsed_version.is_prerelease and (not (prereleases or self.prereleases)):
                    found_prereleases.append(version)
                else:
                    yielded = True
                    yield version
        if not yielded and found_prereleases:
            for version in found_prereleases:
                yield version

class LegacySpecifier(_IndividualSpecifier):
    _regex_str = '\n        (?P<operator>(==|!=|<=|>=|<|>))\n        \\s*\n        (?P<version>\n            [^,;\\s)]* # Since this is a "legacy" specifier, and the version\n                      # string can be just about anything, we match everything\n                      # except for whitespace, a semi-colon for marker support,\n                      # a closing paren since versions can be enclosed in\n                      # them, and a comma since it\'s a version separator.\n        )\n        '
    _regex = re.compile('^\\s*' + _regex_str + '\\s*$', re.VERBOSE | re.IGNORECASE)
    _operators = {'==': 'equal', '!=': 'not_equal', '<=': 'less_than_equal', '>=': 'greater_than_equal', '<': 'less_than', '>': 'greater_than'}

    def __init__(self, spec: str='', prereleases: Optional[bool]=None) -> None:
        super().__init__(spec, prereleases)
        warnings.warn('Creating a LegacyVersion has been deprecated and will be removed in the next major release', DeprecationWarning)

    def _coerce_version(self, version: UnparsedVersion) -> LegacyVersion:
        if not isinstance(version, LegacyVersion):
            version = LegacyVersion(str(version))
        return version

    def _compare_equal(self, prospective: LegacyVersion, spec: str) -> bool:
        return prospective == self._coerce_version(spec)

    def _compare_not_equal(self, prospective: LegacyVersion, spec: str) -> bool:
        return prospective != self._coerce_version(spec)

    def _compare_less_than_equal(self, prospective: LegacyVersion, spec: str) -> bool:
        return prospective <= self._coerce_version(spec)

    def _compare_greater_than_equal(self, prospective: LegacyVersion, spec: str) -> bool:
        return prospective >= self._coerce_version(spec)

    def _compare_less_than(self, prospective: LegacyVersion, spec: str) -> bool:
        return prospective < self._coerce_version(spec)

    def _compare_greater_than(self, prospective: LegacyVersion, spec: str) -> bool:
        return prospective > self._coerce_version(spec)

def _require_version_compare(fn: Callable[['Specifier', ParsedVersion, str], bool]) -> Callable[['Specifier', ParsedVersion, str], bool]:

    @functools.wraps(fn)
    def wrapped(self: 'Specifier', prospective: ParsedVersion, spec: str) -> bool:
        if not isinstance(prospective, Version):
            return False
        return fn(self, prospective, spec)
    return wrapped

class Specifier(_IndividualSpecifier):
    _regex_str = "\n        (?P<operator>(~=|==|!=|<=|>=|<|>|===))\n        (?P<version>\n            (?:\n                # The identity operators allow for an escape hatch that will\n                # do an exact string match of the version you wish to install.\n                # This will not be parsed by PEP 440 and we cannot determine\n                # any semantic meaning from it. This operator is discouraged\n                # but included entirely as an escape hatch.\n                (?<====)  # Only match for the identity operator\n                \\s*\n                [^\\s]*    # We just match everything, except for whitespace\n                          # since we are only testing for strict identity.\n            )\n            |\n            (?:\n                # The (non)equality operators allow for wild card and local\n                # versions to be specified so we have to define these two\n                # operators separately to enable that.\n                (?<===|!=)            # Only match for equals and not equals\n\n                \\s*\n                v?\n                (?:[0-9]+!)?          # epoch\n                [0-9]+(?:\\.[0-9]+)*   # release\n                (?:                   # pre release\n                    [-_\\.]?\n                    (a|b|c|rc|alpha|beta|pre|preview)\n                    [-_\\.]?\n                    [0-9]*\n                )?\n                (?:                   # post release\n                    (?:-[0-9]+)|(?:[-_\\.]?(post|rev|r)[-_\\.]?[0-9]*)\n                )?\n\n                # You cannot use a wild card and a dev or local version\n                # together so group them with a | and make them optional.\n                (?:\n                    (?:[-_\\.]?dev[-_\\.]?[0-9]*)?         # dev release\n                    (?:\\+[a-z0-9]+(?:[-_\\.][a-z0-9]+)*)? # local\n                    |\n                    \\.\\*  # Wild card syntax of .*\n                )?\n            )\n            |\n            (?:\n                # The compatible operator requires at least two digits in the\n                # release segment.\n                (?<=~=)               # Only match for the compatible operator\n\n                \\s*\n                v?\n                (?:[0-9]+!)?          # epoch\n                [0-9]+(?:\\.[0-9]+)+   # release  (We have a + instead of a *)\n                (?:                   # pre release\n                    [-_\\.]?\n                    (a|b|c|rc|alpha|beta|pre|preview)\n                    [-_\\.]?\n                    [0-9]*\n                )?\n                (?:                                   # post release\n                    (?:-[0-9]+)|(?:[-_\\.]?(post|rev|r)[-_\\.]?[0-9]*)\n                )?\n                (?:[-_\\.]?dev[-_\\.]?[0-9]*)?          # dev release\n            )\n            |\n            (?:\n                # All other operators only allow a sub set of what the\n                # (non)equality operators do. Specifically they do not allow\n                # local versions to be specified nor do they allow the prefix\n                # matching wild cards.\n                (?<!==|!=|~=)         # We have special cases for these\n                                      # operators so we want to make sure they\n                                      # don't match here.\n\n                \\s*\n                v?\n                (?:[0-9]+!)?          # epoch\n                [0-9]+(?:\\.[0-9]+)*   # release\n                (?:                   # pre release\n                    [-_\\.]?\n                    (a|b|c|rc|alpha|beta|pre|preview)\n                    [-_\\.]?\n                    [0-9]*\n                )?\n                (?:                                   # post release\n                    (?:-[0-9]+)|(?:[-_\\.]?(post|rev|r)[-_\\.]?[0-9]*)\n                )?\n                (?:[-_\\.]?dev[-_\\.]?[0-9]*)?          # dev release\n            )\n        )\n        "
    _regex = re.compile('^\\s*' + _regex_str + '\\s*$', re.VERBOSE | re.IGNORECASE)
    _operators = {'~=': 'compatible', '==': 'equal', '!=': 'not_equal', '<=': 'less_than_equal', '>=': 'greater_than_equal', '<': 'less_than', '>': 'greater_than', '===': 'arbitrary'}

    @_require_version_compare
    def _compare_compatible(self, prospective: ParsedVersion, spec: str) -> bool:
        prefix = '.'.join(list(itertools.takewhile(_is_not_suffix, _version_split(spec)))[:-1])
        prefix += '.*'
        return self._get_operator('>=')(prospective, spec) and self._get_operator('==')(prospective, prefix)

    @_require_version_compare
    def _compare_equal(self, prospective: ParsedVersion, spec: str) -> bool:
        if spec.endswith('.*'):
            prospective = Version(prospective.public)
            split_spec = _version_split(spec[:-2])
            split_prospective = _version_split(str(prospective))
            shortened_prospective = split_prospective[:len(split_spec)]
            (padded_spec, padded_prospective) = _pad_version(split_spec, shortened_prospective)
            return padded_prospective == padded_spec
        else:
            spec_version = Version(spec)
            if not spec_version.local:
                prospective = Version(prospective.public)
            return prospective == spec_version

    @_require_version_compare
    def _compare_not_equal(self, prospective: ParsedVersion, spec: str) -> bool:
        return not self._compare_equal(prospective, spec)

    @_require_version_compare
    def _compare_less_than_equal(self, prospective: ParsedVersion, spec: str) -> bool:
        return Version(prospective.public) <= Version(spec)

    @_require_version_compare
    def _compare_greater_than_equal(self, prospective: ParsedVersion, spec: str) -> bool:
        return Version(prospective.public) >= Version(spec)

    @_require_version_compare
    def _compare_less_than(self, prospective: ParsedVersion, spec_str: str) -> bool:
        spec = Version(spec_str)
        if not prospective < spec:
            return False
        if not spec.is_prerelease and prospective.is_prerelease:
            if Version(prospective.base_version) == Version(spec.base_version):
                return False
        return True

    @_require_version_compare
    def _compare_greater_than(self, prospective: ParsedVersion, spec_str: str) -> bool:
        spec = Version(spec_str)
        if not prospective > spec:
            return False
        if not spec.is_postrelease and prospective.is_postrelease:
            if Version(prospective.base_version) == Version(spec.base_version):
                return False
        if prospective.local is not None:
            if Version(prospective.base_version) == Version(spec.base_version):
                return False
        return True

    def _compare_arbitrary(self, prospective: Version, spec: str) -> bool:
        return str(prospective).lower() == str(spec).lower()

    @property
    def prereleases(self) -> bool:
        if self._prereleases is not None:
            return self._prereleases
        (operator, version) = self._spec
        if operator in ['==', '>=', '<=', '~=', '===']:
            if operator == '==' and version.endswith('.*'):
                version = version[:-2]
            if parse(version).is_prerelease:
                return True
        return False

    @prereleases.setter
    def prereleases(self, value: bool) -> None:
        self._prereleases = value
_prefix_regex = re.compile('^([0-9]+)((?:a|b|c|rc)[0-9]+)$')

def _version_split(version: str) -> List[str]:
    result: List[str] = []
    for item in version.split('.'):
        match = _prefix_regex.search(item)
        if match:
            result.extend(match.groups())
        else:
            result.append(item)
    return result

def _is_not_suffix(segment: str) -> bool:
    return not any((segment.startswith(prefix) for prefix in ('dev', 'a', 'b', 'rc', 'post')))

def _pad_version(left: List[str], right: List[str]) -> Tuple[List[str], List[str]]:
    (left_split, right_split) = ([], [])
    left_split.append(list(itertools.takewhile(lambda x: x.isdigit(), left)))
    right_split.append(list(itertools.takewhile(lambda x: x.isdigit(), right)))
    left_split.append(left[len(left_split[0]):])
    right_split.append(right[len(right_split[0]):])
    left_split.insert(1, ['0'] * max(0, len(right_split[0]) - len(left_split[0])))
    right_split.insert(1, ['0'] * max(0, len(left_split[0]) - len(right_split[0])))
    return (list(itertools.chain(*left_split)), list(itertools.chain(*right_split)))

class SpecifierSet(BaseSpecifier):

    def __init__(self, specifiers: str='', prereleases: Optional[bool]=None) -> None:
        split_specifiers = [s.strip() for s in specifiers.split(',') if s.strip()]
        parsed: Set[_IndividualSpecifier] = set()
        for specifier in split_specifiers:
            try:
                parsed.add(Specifier(specifier))
            except InvalidSpecifier:
                parsed.add(LegacySpecifier(specifier))
        self._specs = frozenset(parsed)
        self._prereleases = prereleases

    def __repr__(self) -> str:
        pre = f', prereleases={self.prereleases!r}' if self._prereleases is not None else ''
        return '<SpecifierSet({!r}{})>'.format(str(self), pre)

    def __str__(self) -> str:
        return ','.join(sorted((str(s) for s in self._specs)))

    def __hash__(self) -> int:
        return hash(self._specs)

    def __and__(self, other: Union['SpecifierSet', str]) -> 'SpecifierSet':
        if isinstance(other, str):
            other = SpecifierSet(other)
        elif not isinstance(other, SpecifierSet):
            return NotImplemented
        specifier = SpecifierSet()
        specifier._specs = frozenset(self._specs | other._specs)
        if self._prereleases is None and other._prereleases is not None:
            specifier._prereleases = other._prereleases
        elif self._prereleases is not None and other._prereleases is None:
            specifier._prereleases = self._prereleases
        elif self._prereleases == other._prereleases:
            specifier._prereleases = self._prereleases
        else:
            raise ValueError('Cannot combine SpecifierSets with True and False prerelease overrides.')
        return specifier

    def __eq__(self, other: object) -> bool:
        if isinstance(other, (str, _IndividualSpecifier)):
            other = SpecifierSet(str(other))
        elif not isinstance(other, SpecifierSet):
            return NotImplemented
        return self._specs == other._specs

    def __ne__(self, other: object) -> bool:
        if isinstance(other, (str, _IndividualSpecifier)):
            other = SpecifierSet(str(other))
        elif not isinstance(other, SpecifierSet):
            return NotImplemented
        return self._specs != other._specs

    def __len__(self) -> int:
        return len(self._specs)

    def __iter__(self) -> Iterator[_IndividualSpecifier]:
        return iter(self._specs)

    @property
    def prereleases(self) -> Optional[bool]:
        if self._prereleases is not None:
            return self._prereleases
        if not self._specs:
            return None
        return any((s.prereleases for s in self._specs))

    @prereleases.setter
    def prereleases(self, value: bool) -> None:
        self._prereleases = value

    def __contains__(self, item: UnparsedVersion) -> bool:
        return self.contains(item)

    def contains(self, item: UnparsedVersion, prereleases: Optional[bool]=None) -> bool:
        if not isinstance(item, (LegacyVersion, Version)):
            item = parse(item)
        if prereleases is None:
            prereleases = self.prereleases
        if not prereleases and item.is_prerelease:
            return False
        return all((s.contains(item, prereleases=prereleases) for s in self._specs))

    def filter(self, iterable: Iterable[VersionTypeVar], prereleases: Optional[bool]=None) -> Iterable[VersionTypeVar]:
        if prereleases is None:
            prereleases = self.prereleases
        if self._specs:
            for spec in self._specs:
                iterable = spec.filter(iterable, prereleases=bool(prereleases))
            return iterable
        else:
            filtered: List[VersionTypeVar] = []
            found_prereleases: List[VersionTypeVar] = []
            item: UnparsedVersion
            parsed_version: Union[Version, LegacyVersion]
            for item in iterable:
                if not isinstance(item, (LegacyVersion, Version)):
                    parsed_version = parse(item)
                else:
                    parsed_version = item
                if isinstance(parsed_version, LegacyVersion):
                    continue
                if parsed_version.is_prerelease and (not prereleases):
                    if not filtered:
                        found_prereleases.append(item)
                else:
                    filtered.append(item)
            if not filtered and found_prereleases and (prereleases is None):
                return found_prereleases
            return filtered