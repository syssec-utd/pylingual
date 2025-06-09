"""
Pattern matching for filesystem trees
"""
import os
import fnmatch
from pathlib import Path

def match_path_prefix(prefix, path):
    """
    Match path prefix for two paths with fnmatch applied to path components
    """
    if isinstance(prefix, str):
        prefix = prefix.split(os.sep)
    if isinstance(path, str):
        path = Path(path)
    if isinstance(path, list):
        path = Path(*path)
    parts = [parent.name for parent in list(reversed(path.parents))]
    parts.append(path.name)
    if prefix[0] not in ('', os.sep) and parts[0] == '':
        parts = parts[1:]
    for index, path_pattern in enumerate(prefix):
        if index > len(parts) - 1:
            return False
        if not fnmatch.fnmatch(parts[index], path_pattern):
            return False
    return True

def match_path_patterns(patterns, root, path):
    """
    Match specified path to filename patterns compared to root directory
    """
    if not isinstance(path, Path):
        path = Path(path)
    try:
        relative_path = str(Path(path).relative_to(root))
    except ValueError:
        relative_path = None
    for pattern in patterns:
        if pattern.endswith('/'):
            pattern = pattern.rstrip('/')
        if relative_path == pattern or fnmatch.fnmatch(path.name, pattern):
            return True
        if relative_path is not None and fnmatch.fnmatch(relative_path, pattern):
            return True
        if relative_path and match_path_prefix(pattern, relative_path):
            return True
    return False