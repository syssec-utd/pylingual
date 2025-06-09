__all__ = ['AppDirPath']
'\nModule Docstring\nDocstrings: http://www.python.org/dev/peps/pep-0257/\n'
__author__ = 'ButenkoMS <gtalk@butenkoms.space>'
__copyright__ = 'Copyright © 2012-2023 ButenkoMS. All rights reserved. Contacts: <gtalk@butenkoms.space>'
__credits__ = ['ButenkoMS <gtalk@butenkoms.space>']
__license__ = 'Apache License, Version 2.0'
__version__ = '3.1.18'
__maintainer__ = 'ButenkoMS <gtalk@butenkoms.space>'
__email__ = 'gtalk@butenkoms.space'
__status__ = 'Development'
import os
from cengal.file_system.directory_manager import ensure_dir as ensure_dir_exists
from .app_directory_types import AppDirectoryType
from .app_dir_path_base import AppDirPathBase, DirTypeMappingItem, DirTypeMappingItem, BaseDirID, DirNameOrPath, norm_dir_name_or_path
from typing import Optional, Tuple, Dict
from functools import lru_cache
from enum import Enum

class LinuxDirectoryType(Enum):
    local_data = 0
    local_cache = 1
    local_config = 2
    local_log = 3
    local_temp = 4
    local_runtime = 5
    program_data = 6
    program_cache = 7
    program_config = 8
    program_log = 9
    program_temp = 10
    program_runtime = 11
    program_files = 12
    user_profile_data = 13
    user_profile_program_files = 14
    user_profile_program_files_common = 15
    local_static_data = 16
    program_static_data = 17
dir_type_mapping: Dict[AppDirectoryType, Tuple[LinuxDirectoryType, Optional[DirNameOrPath], Optional[DirNameOrPath]]] = {AppDirectoryType.local_data: (LinuxDirectoryType.local_data, None, ('local', 'data')), AppDirectoryType.local_static_data: (LinuxDirectoryType.local_static_data, None, ('local', 'static_data')), AppDirectoryType.local_cache: (LinuxDirectoryType.local_cache, None, ('local', 'cache')), AppDirectoryType.local_config: (LinuxDirectoryType.local_config, None, ('local', 'config')), AppDirectoryType.local_log: (LinuxDirectoryType.local_log, None, ('local', 'log')), AppDirectoryType.local_temp: (LinuxDirectoryType.local_temp, None, ('local', 'temp')), AppDirectoryType.local_runtime: (LinuxDirectoryType.local_runtime, None, ('local', 'runtime')), AppDirectoryType.local_low_data: (LinuxDirectoryType.local_data, None, ('local_low', 'data')), AppDirectoryType.local_low_static_data: (LinuxDirectoryType.local_static_data, None, ('local_low', 'static_data')), AppDirectoryType.local_low_cache: (LinuxDirectoryType.local_cache, None, ('local_low', 'cache')), AppDirectoryType.local_low_config: (LinuxDirectoryType.local_config, None, ('local_low', 'config')), AppDirectoryType.local_low_log: (LinuxDirectoryType.local_log, None, ('local_low', 'log')), AppDirectoryType.local_low_temp: (LinuxDirectoryType.local_temp, None, ('local_low', 'temp')), AppDirectoryType.local_low_runtime: (LinuxDirectoryType.local_runtime, None, ('local_low', 'runtime')), AppDirectoryType.roaming_data: (LinuxDirectoryType.local_data, None, ('roaming', 'data')), AppDirectoryType.roaming_static_data: (LinuxDirectoryType.local_static_data, None, ('roaming', 'static_data')), AppDirectoryType.roaming_cache: (LinuxDirectoryType.local_cache, None, ('roaming', 'cache')), AppDirectoryType.roaming_config: (LinuxDirectoryType.local_config, None, ('roaming', 'config')), AppDirectoryType.roaming_log: (LinuxDirectoryType.local_log, None, ('roaming', 'log')), AppDirectoryType.roaming_temp: (LinuxDirectoryType.local_temp, None, ('roaming', 'temp')), AppDirectoryType.roaming_runtime: (LinuxDirectoryType.local_runtime, None, ('roaming', 'runtime')), AppDirectoryType.program_data: (LinuxDirectoryType.program_data, None, 'data'), AppDirectoryType.program_static_data: (LinuxDirectoryType.program_static_data, None, 'static_data'), AppDirectoryType.program_cache: (LinuxDirectoryType.program_cache, None, 'cache'), AppDirectoryType.program_config: (LinuxDirectoryType.program_config, None, 'config'), AppDirectoryType.program_log: (LinuxDirectoryType.program_log, None, 'log'), AppDirectoryType.program_temp: (LinuxDirectoryType.program_temp, None, 'temp'), AppDirectoryType.program_runtime: (LinuxDirectoryType.program_runtime, None, 'runtime'), AppDirectoryType.program_files: (LinuxDirectoryType.program_files, None, None), AppDirectoryType.program_files_common: (LinuxDirectoryType.program_files, None, None), AppDirectoryType.user_profile_data: (LinuxDirectoryType.user_profile_data, None, None), AppDirectoryType.user_profile_program_files: (LinuxDirectoryType.local_data, None, None), AppDirectoryType.user_profile_program_files_common: (LinuxDirectoryType.local_data, None, None)}

class AppDirPath(AppDirPathBase):

    def __init__(self, max_cache_size: Optional[int]=None) -> None:
        super().__init__(max_cache_size)

    def dir_type_mapping(self, dir_type: AppDirectoryType) -> DirTypeMappingItem:
        return dir_type_mapping[dir_type]

    def base_dir_id_to_path(self, base_dir_id: BaseDirID) -> str:
        result_path = None
        if LinuxDirectoryType.local_data == base_dir_id:
            result_path = os.environ.get('XDG_STATE_HOME', os.path.join(os.path.expanduser('~'), '.local', 'state'))
        elif LinuxDirectoryType.local_static_data == base_dir_id:
            result_path = os.environ.get('XDG_DATA_HOME', os.path.join(os.path.expanduser('~'), '.local', 'share'))
        elif LinuxDirectoryType.local_cache == base_dir_id:
            result_path = os.environ.get('XDG_CACHE_HOME', os.path.join(os.path.expanduser('~'), '.cache'))
        elif LinuxDirectoryType.local_config == base_dir_id:
            result_path = os.environ.get('XDG_CONFIG_HOME', os.path.join(os.path.expanduser('~'), '.config'))
        elif LinuxDirectoryType.local_log == base_dir_id:
            result_path = os.environ.get('XDG_STATE_HOME', os.path.join(os.path.expanduser('~'), '.local', 'state'))
        elif LinuxDirectoryType.local_temp == base_dir_id:
            result_path = os.environ.get('XDG_RUNTIME_DIR', os.path.join(os.path.expanduser('~'), '.tmp'))
        elif LinuxDirectoryType.local_runtime == base_dir_id:
            result_path = os.environ.get('XDG_RUNTIME_DIR', os.path.join(os.path.expanduser('~'), '.tmp'))
        elif LinuxDirectoryType.program_data == base_dir_id:
            result_path = '/var/lib'
        elif LinuxDirectoryType.program_static_data == base_dir_id:
            result_path = '/usr/share'
        elif LinuxDirectoryType.program_cache == base_dir_id:
            result_path = '/var/cache'
        elif LinuxDirectoryType.program_config == base_dir_id:
            result_path = '/etc'
        elif LinuxDirectoryType.program_log == base_dir_id:
            result_path = '/var/log'
        elif LinuxDirectoryType.program_temp == base_dir_id:
            result_path = '/tmp'
        elif LinuxDirectoryType.program_runtime == base_dir_id:
            result_path = '/var/run'
        elif LinuxDirectoryType.program_files == base_dir_id:
            result_path = '/opt'
        elif LinuxDirectoryType.user_profile_data == base_dir_id:
            result_path = os.path.expanduser('~')
        elif LinuxDirectoryType.user_profile_program_files == base_dir_id:
            result_path = os.environ.get('XDG_DATA_HOME', os.path.join(os.path.expanduser('~'), '.local', 'share'))
        elif LinuxDirectoryType.user_profile_program_files_common == base_dir_id:
            result_path = os.environ.get('XDG_DATA_HOME', os.path.join(os.path.expanduser('~'), '.local', 'share'))
        return result_path