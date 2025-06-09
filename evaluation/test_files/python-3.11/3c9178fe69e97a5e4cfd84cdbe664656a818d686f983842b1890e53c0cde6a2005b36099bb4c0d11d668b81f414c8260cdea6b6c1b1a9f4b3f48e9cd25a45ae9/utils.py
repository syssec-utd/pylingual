from __future__ import absolute_import, division, print_function
import re
from ._typing import TYPE_CHECKING, cast
from .tags import Tag, parse_tag
from .version import InvalidVersion, Version
if TYPE_CHECKING:
    from typing import FrozenSet, NewType, Tuple, Union
    BuildTag = Union[Tuple[()], Tuple[int, str]]
    NormalizedName = NewType('NormalizedName', str)
else:
    BuildTag = tuple
    NormalizedName = str

class InvalidWheelFilename(ValueError):
    """
    An invalid wheel filename was found, users should refer to PEP 427.
    """

class InvalidSdistFilename(ValueError):
    """
    An invalid sdist filename was found, users should refer to the packaging user guide.
    """
_canonicalize_regex = re.compile('[-_.]+')
_build_tag_regex = re.compile('(\\d+)(.*)')

def canonicalize_name(name):
    value = _canonicalize_regex.sub('-', name).lower()
    return cast(NormalizedName, value)

def canonicalize_version(version):
    """
    This is very similar to Version.__str__, but has one subtle difference
    with the way it handles the release segment.
    """
    if not isinstance(version, Version):
        try:
            version = Version(version)
        except InvalidVersion:
            return version
    parts = []
    if version.epoch != 0:
        parts.append('{0}!'.format(version.epoch))
    parts.append(re.sub('(\\.0)+$', '', '.'.join((str(x) for x in version.release))))
    if version.pre is not None:
        parts.append(''.join((str(x) for x in version.pre)))
    if version.post is not None:
        parts.append('.post{0}'.format(version.post))
    if version.dev is not None:
        parts.append('.dev{0}'.format(version.dev))
    if version.local is not None:
        parts.append('+{0}'.format(version.local))
    return ''.join(parts)

def parse_wheel_filename(filename):
    if not filename.endswith('.whl'):
        raise InvalidWheelFilename("Invalid wheel filename (extension must be '.whl'): {0}".format(filename))
    filename = filename[:-4]
    dashes = filename.count('-')
    if dashes not in (4, 5):
        raise InvalidWheelFilename('Invalid wheel filename (wrong number of parts): {0}'.format(filename))
    parts = filename.split('-', dashes - 2)
    name_part = parts[0]
    if '__' in name_part or re.match('^[\\w\\d._]*$', name_part, re.UNICODE) is None:
        raise InvalidWheelFilename('Invalid project name: {0}'.format(filename))
    name = canonicalize_name(name_part)
    version = Version(parts[1])
    if dashes == 5:
        build_part = parts[2]
        build_match = _build_tag_regex.match(build_part)
        if build_match is None:
            raise InvalidWheelFilename("Invalid build number: {0} in '{1}'".format(build_part, filename))
        build = cast(BuildTag, (int(build_match.group(1)), build_match.group(2)))
    else:
        build = ()
    tags = parse_tag(parts[-1])
    return (name, version, build, tags)

def parse_sdist_filename(filename):
    if not filename.endswith('.tar.gz'):
        raise InvalidSdistFilename("Invalid sdist filename (extension must be '.tar.gz'): {0}".format(filename))
    name_part, sep, version_part = filename[:-7].rpartition('-')
    if not sep:
        raise InvalidSdistFilename('Invalid sdist filename: {0}'.format(filename))
    name = canonicalize_name(name_part)
    version = Version(version_part)
    return (name, version)