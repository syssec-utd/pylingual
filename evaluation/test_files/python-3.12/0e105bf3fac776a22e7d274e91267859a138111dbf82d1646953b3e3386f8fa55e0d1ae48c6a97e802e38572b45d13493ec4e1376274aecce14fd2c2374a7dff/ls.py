import pathlib
Here = pathlib.Path(__file__).parent
import numpy as np
from pydub import AudioSegment
from pydub.playback import play
import sys
from . import hotword as ht
import argparse
from tensorflow.keras.models import Model, load_model

def detect_triggerword_spectrum(x):
    """
    Function to predict the location of the trigger word.
    
    Argument:
    x -- spectrum of shape (freqs, Tx)
    i.e. (Number of frequencies, The number time steps)

    Returns:
    predictions -- flattened numpy array to shape (number of output time steps)
    """
    x = x.swapaxes(0, 1)
    x = np.expand_dims(x, axis=0)
    predictions = model.predict(x, verbose=0)
    return predictions.reshape(-1)

def has_new_triggerword(predictions, chunk_duration, feed_duration, threshold=0.5):
    """
    Function to detect new trigger word in the latest chunk of input audio.
    It is looking for the rising edge of the predictions data belongs to the
    last/latest chunk.
    
    Argument:
    predictions -- predicted labels from model
    chunk_duration -- time in second of a chunk
    feed_duration -- time in second of the input to model
    threshold -- threshold for probability above a certain to be considered positive

    Returns:
    True if new trigger word detected in the latest chunk
    """
    predictions = predictions > threshold
    chunk_predictions_samples = int(len(predictions) * chunk_duration / feed_duration)
    chunk_predictions = predictions[-chunk_predictions_samples:]
    level = chunk_predictions[0]
    for pred in chunk_predictions:
        if pred > level:
            return True
        else:
            level = pred
    return False
chunk_duration = 0.5
fs = 44100
chunk_samples = int(fs * chunk_duration)
mic_index = 0
feed_duration = 10
feed_samples = int(fs * feed_duration)
assert feed_duration / chunk_duration == int(feed_duration / chunk_duration)

def get_audio_input_stream(callback):
    stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=fs, input=True, frames_per_buffer=chunk_samples, input_device_index=mic_index, stream_callback=callback)
    return stream
import pyaudio
from queue import Queue
import sys
import time
silence_threshold = 150
q = Queue()
data = np.zeros(feed_samples, dtype='int16')

def callback(in_data, frame_count, time_info, status):
    global data, silence_threshold
    data0 = np.frombuffer(in_data, dtype='int16')
    if np.abs(data0).mean() < silence_threshold:
        return (in_data, pyaudio.paContinue)
    data = np.append(data, data0)
    if len(data) > feed_samples:
        data = data[-feed_samples:]
        q.put(data)
    return (in_data, pyaudio.paContinue)

def lsHotword_loop(mpath, silence_thres=100, chimePath=Here / 'chime.wav', chimeOnWake=True, mic_idx=0, sampling_rate=44100):
    global silence_threshold, mic_index, model, chime, fs
    fs = sampling_rate
    mic_index = mic_idx
    chime = AudioSegment.from_wav(chimePath)
    silence_threshold = silence_thres
    model = load_model(mpath)
    stream = get_audio_input_stream(callback)
    stream.start_stream()
    try:
        while True:
            print('<<Waiting for Hotword>>')
            data = q.get()
            spectrum = ht.get_spectrogram(data)
            preds = detect_triggerword_spectrum(spectrum)
            new_trigger = has_new_triggerword(preds, chunk_duration, feed_duration)
            if new_trigger:
                sys.stdout.write('<<Activated>>')
                if chimeOnWake:
                    play(chime)
                stream.stop_stream()
                stream.close()
                return True
    except (KeyboardInterrupt, SystemExit):
        stream.stop_stream()
        stream.close()
        return False

class Hotword:

    def __init__(self, mpath, silence_thres=100, chimePath=Here / 'chime.wav', chimeOnWake=True, mic_idx=0, sampling_rate=44100):
        global silence_threshold, mic_index, model, chime, fs
        fs = sampling_rate
        mic_index = mic_idx
        chime = AudioSegment.from_wav(chimePath)
        silence_threshold = silence_thres
        self.chimeOnWake = chimeOnWake
        model = load_model(mpath)

    def HotwordLoop(self, chimeOnWake=True):
        self.chimeOnWake = chimeOnWake
        stream = get_audio_input_stream(callback)
        stream.start_stream()
        try:
            while True:
                print('<<Waiting for Hotword>>\n')
                data = q.get()
                spectrum = ht.get_spectrogram(data)
                preds = detect_triggerword_spectrum(spectrum)
                new_trigger = has_new_triggerword(preds, chunk_duration, feed_duration)
                if new_trigger:
                    print('<<Activated>>\n')
                    if self.chimeOnWake:
                        play(chime)
                    stream.stop_stream()
                    stream.close()
                    return True
        except (KeyboardInterrupt, SystemExit):
            stream.stop_stream()
            stream.close()
            return False

def HTest():
    parser = argparse.ArgumentParser(description='Model path e.g. "--model ./model.h5"')
    parser.add_argument('--model', action='store', type=str, required=True)
    args = parser.parse_args()
    print(lsHotword_loop(args.model))