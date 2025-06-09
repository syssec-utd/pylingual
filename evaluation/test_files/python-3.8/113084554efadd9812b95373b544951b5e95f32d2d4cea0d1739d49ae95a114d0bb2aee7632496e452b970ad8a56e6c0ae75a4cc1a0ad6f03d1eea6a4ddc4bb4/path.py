"""Shorthands for paths for templates, static assets, etc."""
from pinnwand import configuration
import pathlib
base = pathlib.Path(__file__).parent
template = base / 'template'
static = base / 'static'
if configuration.page_path:
    page = pathlib.Path(configuration.page_path)
else:
    page = base / 'page'