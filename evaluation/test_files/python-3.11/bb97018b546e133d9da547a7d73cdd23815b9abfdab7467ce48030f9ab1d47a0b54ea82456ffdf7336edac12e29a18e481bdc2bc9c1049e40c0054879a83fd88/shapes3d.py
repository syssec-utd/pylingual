"""Dataset definition for shapes3d.

DEPRECATED!
If you want to use the Shapes3d dataset builder class, use:
tfds.builder_cls('shapes3d')
"""
from tensorflow_datasets.core import lazy_builder_import
Shapes3d = lazy_builder_import.LazyBuilderImport('shapes3d')