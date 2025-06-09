"""Functions for batching input files by extension."""
from dataclasses import dataclass
from itertools import groupby
import os
from pathlib import Path
import typing as t

@dataclass
class Batch:
    """Batch of input files with the same file extension."""
    extension: str
    paths: t.Sequence[Path]

def group_by_file_extension(files: t.Iterable[Path]) -> t.Iterable[Batch]:
    """Batch input files by file extension.

    Files with no extension belong to their own batch.
    """

    def key(filename: t.Union[str, Path]) -> t.Tuple[str, str]:
        (root, ext) = os.path.splitext(filename)
        return (ext, '') if ext else ('', root)
    groups = groupby(sorted(files, key=key), key=key)
    for (_key, paths) in groups:
        yield Batch(_key[0] or _key[1], tuple(paths))