import shutil
import sys
from sys import version_info
if version_info.major < 3 or (version_info.major == 3 and version_info.minor < 3):
    from collections import Callable
else:
    from collections.abc import Callable
from functools import lru_cache
from typing import List, Optional
from zipfile import ZipFile
from pims.api.exceptions import NoMatchingFormatProblem
from pims.files.file import Path

class ArchiveError(OSError):
    pass

class ArchiveFormat:

    def __init__(self, name: str, description: str, match: Callable):
        self.name = name
        self.description = description
        self.match = match

    def get_identifier(self, uppercase: bool=True) -> str:
        if uppercase:
            return self.name.upper()
        return self.name

    def get_name(self) -> str:
        return self.get_identifier(False)

    def get_remarks(self) -> str:
        return self.description

def zip_match(signature: bytearray) -> bool:
    return len(signature) > 3 and signature[0] == 80 and (signature[1] == 75) and (signature[2] == 3 or signature[2] == 5 or signature[2] == 7) and (signature[3] == 4 or signature[3] == 6 or signature[3] == 8)

def tar_match(signature: bytearray) -> bool:
    return len(signature) > 261 and signature[257] == 117 and (signature[258] == 115) and (signature[259] == 116) and (signature[260] == 97) and (signature[261] == 114)

def gztar_match(signature: bytearray) -> bool:
    return len(signature) > 2 and signature[0] == 31 and (signature[1] == 139) and (signature[2] == 8)

def bztar_match(signature: bytearray) -> bool:
    return len(signature) > 2 and signature[0] == 66 and (signature[1] == 90) and (signature[2] == 104)

def xztar_match(signature: bytearray) -> bool:
    return len(signature) > 5 and signature[0] == 253 and (signature[1] == 55) and (signature[2] == 122) and (signature[3] == 88) and (signature[4] == 90) and (signature[5] == 0)

@lru_cache
def _build_archive_format_list() -> List[ArchiveFormat]:
    formats = []
    extensions = shutil.get_archive_formats()
    for name, description in extensions:
        match_fn_name = f'{name}_match'
        match = getattr(sys.modules[__name__], match_fn_name, None)
        if match is not None:
            formats.append(ArchiveFormat(name, description, match))
    return formats
ARCHIVE_FORMATS = _build_archive_format_list()

class Archive(Path):

    def __init__(self, *pathsegments, format: Optional[ArchiveFormat]=None):
        super().__init__(pathsegments)
        _format = None
        if format:
            _format = format
        else:
            signature = self.signature()
            for possible_format in ARCHIVE_FORMATS:
                if possible_format.match(signature):
                    _format = possible_format
                    break
        if _format is None:
            raise NoMatchingFormatProblem(self)
        else:
            self._format = _format

    def extract(self, path: Path, clean: bool=True):
        """
        Extract the archive content.

        Parameters
        ----------
        path : Path
            A non-existing directory path where the archive content is extracted
        clean : bool (default: True)
            Whether the archive content has to be cleaned from Mac OS hidden
            files (.DS_STORE, __MACOSX).
        """
        if path.exists() and (not path.is_dir()):
            raise ArchiveError(f'{self} cannot be extracted in {path} because it already exists or it is not a directory')
        try:
            shutil.unpack_archive(self.absolute(), path, self._format.name)
        except shutil.ReadError as e:
            raise ArchiveError(str(e))
        if clean:
            bad_filenames = ['.DS_STORE', '__MACOSX']
            for bad_filename in bad_filenames:
                for bad_path in path.rglob(bad_filename):
                    bad_path.unlink(missing_ok=True)

    @classmethod
    def from_path(cls, path):
        try:
            return cls(path)
        except NoMatchingFormatProblem:
            return None

    @property
    def format(self) -> ArchiveFormat:
        return self._format

def make_zip_archive(archive_path: Path, content_path: Path) -> ZipFile:
    """
    Make a zip archive at `archive_path` location with `content_path`
    inside.

    Note: cannot use `shutil` to write archives as it is not thread safe !
    """

    def walk(path):
        for p in Path(path).iterdir():
            if p.is_dir():
                yield from walk(p)
                continue
            yield p.resolve()
    with ZipFile(archive_path, 'w') as zipf:
        for file in walk(content_path):
            zipf.write(file, file.relative_to(content_path))
    return zipf