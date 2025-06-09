"""smartwatch_gestures dataset."""
import tensorflow_datasets.public_api as tfds
from tensorflow_datasets.time_series.smartwatch_gestures import smartwatch_gestures

class SmartwatchGesturesTest(tfds.testing.DatasetBuilderTestCase):
    """Tests for smartwatch_gestures dataset."""
    DATASET_CLASS = smartwatch_gestures.SmartwatchGestures
    SPLITS = {'train': 3}
if __name__ == '__main__':
    tfds.testing.test_main()