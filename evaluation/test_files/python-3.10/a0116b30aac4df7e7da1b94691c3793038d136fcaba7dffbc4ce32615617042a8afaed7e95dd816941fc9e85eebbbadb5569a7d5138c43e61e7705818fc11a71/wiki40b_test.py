"""Tests for wiki40b dataset module."""
import os
from tensorflow_datasets import testing
from tensorflow_datasets.text import wiki40b
_EXAMPLE_DIR = os.path.join(os.path.normpath(os.path.dirname(__file__) + '/../'), 'testing', 'test_data', 'fake_examples', 'wiki40b')

class Wiki40bTest(testing.DatasetBuilderTestCase):

    @classmethod
    def setUpClass(cls):
        super(Wiki40bTest, cls).setUpClass()
        wiki40b._DATA_DIRECTORY = _EXAMPLE_DIR
    DATASET_CLASS = wiki40b.Wiki40b
    BUILDER_CONFIG_NAMES_TO_TEST = ['en']
    SPLITS = {'train': 3, 'validation': 2, 'test': 1}
if __name__ == '__main__':
    testing.test_main()