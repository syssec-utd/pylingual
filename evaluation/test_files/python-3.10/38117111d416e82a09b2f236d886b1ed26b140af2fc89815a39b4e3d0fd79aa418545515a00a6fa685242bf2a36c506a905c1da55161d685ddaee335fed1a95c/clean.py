from mio import cfg
from mio import cmp
from mio import cov
from mio import dox
from mio import elab
from mio import history
from mio import results
from mio import sim
from mio import vivado
import shutil
import os

def do_clean():
    if cfg.dbg:
        print('Call to do_clean()')
    print('\x1b[1;31m********')
    print('Cleaning')
    print('********\x1b[0m')
    if os.path.exists(cfg.sim_results_dir + '/xsim.dir'):
        shutil.rmtree(cfg.sim_results_dir + '/xsim.dir')
    if os.path.exists(cfg.sim_results_dir + '/out'):
        shutil.rmtree(cfg.sim_results_dir + '/out')
    if os.path.exists(cfg.history_file_path):
        os.remove(cfg.history_file_path)
    history.create_history_log()