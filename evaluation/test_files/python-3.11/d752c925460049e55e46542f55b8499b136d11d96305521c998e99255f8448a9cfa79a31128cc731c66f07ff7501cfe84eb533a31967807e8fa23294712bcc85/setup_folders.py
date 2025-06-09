from evdspy.EVDSlocal.common.common_imports import *
from evdspy.EVDSlocal.utils.utils_general import *
from evdspy.EVDSlocal.initial.start_options import *
from ..common.colors import *
from evdspy.EVDSlocal.initial.start_options import default_data_folder_name
dirs = ('pickles', default_data_folder_name)
cur_folder = Path()
import time

def check_folders_setup_necessary():
    for item in dirs:
        folder_ = cur_folder.absolute() / item
        if not folder_.is_dir():
            return True
    return False

def check_setup():
    return not check_folders_setup_necessary()

def setup_folders():
    if not check_folders_setup_necessary():
        deb(f'initial folders checked...{dirs} ')
        return
    for item in dirs:
        folder_ = cur_folder.absolute() / item
        print_with_creating_style(f'Creating directory...{folder_}')
        create_directory(str(folder_))
        time.sleep(0.8)