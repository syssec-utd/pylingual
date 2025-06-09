import os
import sys
import paver
from paver.easy import options, Bunch
import paver.setuputils
from runestone import build
paver.setuputils.install_distutils_tasks()
sys.path.append(os.getcwd())
home_dir = os.getcwd()
master_url = '{{master_url}}'
master_app = '{{master_app}}'
serving_dir = '{{build_dir}}'
dest = '{{dest}}'
options(sphinx=Bunch(docroot='.'), build=Bunch(builddir='{{build_dir}}', sourcedir='_sources', outdir='{{build_dir}}', confdir='.', project_name='{{project_name}}', template_args={}))