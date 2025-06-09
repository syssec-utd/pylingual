import os
import pyprocessors_afp_entities
project = 'pyprocessors_afp_entities'
copyright = '2021, Olivier Terrier'
author = 'Olivier Terrier'
version = pyprocessors_afp_entities.__version__
release = pyprocessors_afp_entities.__version__
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.autosummary', 'sphinx.ext.autosectionlabel', 'sphinx.ext.viewcode', 'sphinx.ext.napoleon', 'sphinxcontrib.apidoc', 'jupyter_sphinx.execute', 'm2r2']
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
default_role = 'autolink'
napoleon_google_docstring = False
autosummary_generate = True
apidoc_module_dir = os.path.dirname(pyprocessors_afp_entities.__file__)
apidoc_output_dir = 'reference'
apidoc_separate_modules = True
apidoc_toc_file = False
apidoc_module_first = True
apidoc_extra_args = ['--force']
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_extra_path = ['LICENSE']