import numpy as np
import pandas as pd
import os
from vosk import Model, KaldiRecognizer
import wave
import json
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def transcribe(audio_path, lang):
    """
    -----------------------------------------------------------------------------------------
    
    Speech transcribe 
    
    Args:
        path: audio path 
        
    Returns:
        results: Speech transcription (list of JSON dictionaries)
        
    -----------------------------------------------------------------------------------------
    """
    measures = get_config()
    results = get_vosk(audio_path, lang)
    speech_conf, speech_label = filter_speech(measures, results)
    return (speech_conf, speech_label)

def get_vosk(audio_path, lang):
    """
    Recognize speech using vosk model
    """
    model = Model(lang=lang)
    wf = wave.open(audio_path, 'rb')
    recog = KaldiRecognizer(model, wf.getframerate())
    recog.SetWords(True)
    results = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if recog.AcceptWaveform(data):
            partial_result = json.loads(recog.Result())
            results.append(partial_result)
    partial_result = json.loads(recog.FinalResult())
    results.append(partial_result)
    return results

def filter_speech(measures, results):
    result_key = []
    text_key = []
    transcript_dict = {}
    for res in results:
        dict_keys = res.keys()
        if 'result' in dict_keys and 'text' in dict_keys:
            result_key.extend(res['result'])
            text_key.append(res['text'])
    transcript_dict['result'] = result_key
    transcript_dict['text'] = ' '.join(text_key)
    return (result_key, ' '.join(text_key))

def get_config():
    dir_name = os.path.dirname(os.path.abspath(__file__))
    measure_path = os.path.abspath(os.path.join(dir_name, 'config/speech.json'))
    file = open(measure_path)
    measures = json.load(file)
    return measures