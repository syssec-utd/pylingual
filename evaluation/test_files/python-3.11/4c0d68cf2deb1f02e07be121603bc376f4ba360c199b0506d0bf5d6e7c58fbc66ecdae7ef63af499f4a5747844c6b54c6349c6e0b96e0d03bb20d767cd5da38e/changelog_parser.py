import logging
from pathlib import Path
LOGGER = logging.getLogger(__name__)

def get_latest_changelog_sections(changelog_file_path: Path, count: int=3) -> str:
    LOGGER.debug('finding latest %i section contents from changelog %s', count, changelog_file_path.resolve())
    lines = []
    found = 0
    for line in changelog_file_path.read_text(encoding='utf-8').splitlines():
        if found == 0 and (not line.startswith('## ')):
            continue
        if line.startswith('## '):
            found += 1
        if found > count:
            break
        if line.startswith('#'):
            orig_len = len(line)
            line = line.lstrip('#')
            line = ''.join(['-'] * (orig_len - len(line))) + line
        lines.append(line)
    return '\n'.join(lines).rstrip()

def get_latest_changelog_version_identifier(changelog_file_path: Path) -> str:
    LOGGER.debug('finding latest version tag from changelog %s', changelog_file_path.resolve())
    for line in changelog_file_path.read_text(encoding='utf-8').splitlines():
        if line.startswith('## '):
            return line.split(' ', maxsplit=2)[1]
    raise ValueError('latest version could not be parsed from changelog')