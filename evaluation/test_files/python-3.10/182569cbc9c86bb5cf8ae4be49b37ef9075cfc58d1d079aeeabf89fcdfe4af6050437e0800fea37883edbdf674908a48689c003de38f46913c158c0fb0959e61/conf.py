from datetime import date
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))
needs_sphinx = '3.0'
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.doctest', 'sphinx.ext.imgmath', 'sphinx.ext.autosummary', 'sphinx_rtd_theme', 'sphinx.ext.napoleon']
autodoc_mock_imports = ['torchvision', 'wget', 'tensorboard', 'pandas', 'sklearn', 'more_itertools', 'streamlit', 'scipy', 'torch', 'arff', 'prettytable', 'skmultilearn', 'wandb']
source_suffix = '.rst'
source_encoding = 'utf-8'
master_doc = 'index'
project = 'DeepMTP'
copyright = '2022, Dimitrios Iliadis'
author = 'Dimitrios Iliadis'
exclude_patterns = ['_build']
show_authors = False
pygments_style = 'sphinx'
html_theme = 'sphinx_rtd_theme'
htmlhelp_basename = '{}doc'.format(project)
latex_elements = {'papersize': 'a4paper', 'pointsize': '10pt', 'figure_align': 'htbp'}
latex_documents = [(master_doc, '{}.tex'.format(project), '{} Documentation'.format(project), author, 'manual')]
man_pages = [(master_doc, project, '{} Documentation'.format(project), [author], 1)]
texinfo_documents = [(master_doc, project, '{} Documentation'.format(project), author, project, 'DeepMTP: a python framework for multi-target prediction.', 'Miscellaneous')]