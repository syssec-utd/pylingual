"""Unit tests for the AudioClassifier wrapper."""
import csv
import unittest
from Mx.audio_classifier import AudioClassifier
from Mx.audio_classifier import AudioClassifierOptions
from Mx.audio_classifier import Category
import numpy as np
from scipy.io import wavfile
_MODEL_FILE = 'file/Mx/model.tflite'
_GROUND_TRUTH_FILE = 'ground_truth.csv'
_AUDIO_FILE = 'file/Mx/sound.wav'
_ACCEPTABLE_ERROR_RANGE = 0.01

class AudioClassifierTest(unittest.TestCase):

    def setUp(self):
        """Initialize the shared variables."""
        super().setUp()
        classifier = AudioClassifier(_MODEL_FILE)
        tensor = classifier.create_input_tensor_audio()
        input_size = len(tensor.buffer)
        input_sample_rate = tensor.format.sample_rate
        channels = tensor.format.channels
        original_sample_rate, wav_data = wavfile.read(_AUDIO_FILE, True)
        self.assertEqual(original_sample_rate, input_sample_rate, "The test audio's sample rate does not match with the model's requirement.")
        wav_data = (wav_data / np.iinfo(wav_data.dtype).max).astype(np.float32)
        wav_data = np.reshape(wav_data[:input_size], [input_size, channels])
        tensor.load_from_array(wav_data)
        self._input_tensor = tensor

    def test_max_results_option(self):
        """Test the max_results option."""
        max_results = 3
        option = AudioClassifierOptions(max_results=max_results)
        classifier = AudioClassifier(_MODEL_FILE, options=option)
        categories = classifier.classify(self._input_tensor)
        print(categories)
        self.assertLessEqual(len(categories), max_results, 'Too many results returned.')
if __name__ == '__main__':
    unittest.main()