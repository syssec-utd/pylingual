from src.Base import _FileGenerator, _generatePng, convertNotes, playNotes, displayNotes, Piece
import os
from IPython.display import Image
import numpy as np
import config
from midiutil import MIDIFile

def test_FileGenerator():
    voices = ["c' d' e' f' g' a' b' c''", "e'"]
    result = _FileGenerator(voices, '4/4')

    def getNextVoice(voicestring):
        start = voicestring.find('{')
        end = voicestring.find('}')
        voice = voicestring[start + 1:end].split(' ')
        voicearr = [a for a in voice if len(a) > 0]
        assert '{' not in voice
        assert '}' not in voice
        return (voicearr, voicestring[end + 1:])
    _, remaining0 = getNextVoice(result)
    voice1, remaining1 = getNextVoice(remaining0)
    voice2, remaining2 = getNextVoice(remaining1)
    assert np.array_equal(voice1, ['\\voiceOne', '\\time', '4/4', "c'", "d'", "e'", "f'", "g'", "a'", "b'", "c''"])
    assert np.array_equal(voice2, ['\\voiceTwo', '\\time', '4/4', "e'"])

def test_generatePng():
    with open('file.ly', 'w') as f:
        f.write('\\version "2.24.1"\n        \\new Staff <<\n    \\new Voice = "0" { \\voiceOne c\' d\' e\' f\' g\'}\n    >>')
    _generatePng('')
    assert os.path.isfile('preview.png')
    os.remove('file.ly')
    os.remove('preview.png')
    if os.path.exists('preview.preview.png'):
        os.remove('preview.preview.png')

def test_displayNotes():
    img = displayNotes(["c' d' e' f' g'"], '4/4')
    assert type(img) == Image

def test_PieceDisplay():
    p1 = Piece(60, '3/4')
    p1.addVoice("c'4 d'4 e'4 f'4 g'4")
    assert type(p1.getScore()) == Image

def test_Midi():
    p1 = Piece(60, '3/4')
    p1.addVoice("c'4 d'4 e'4 f'4 g'4")
    assert type(p1.midi) == MIDIFile

def test_convertNotes():
    assert np.array_equal(np.array(convertNotes(["c a'", "c'"])[0], dtype=object), np.array([[0, 21], [12]], dtype=object))
    result = convertNotes(["c a'", "c'"])[1]
    assert np.linalg.norm(result[0][0] - 130.82) < 1
    assert np.linalg.norm(result[0][1] - 440.01) < 1
    assert np.linalg.norm(result[1][0] - 261.63) < 1

def test_playNotes():
    config.play_audio = False
    freqs = [[261.63, 293.66974569918125, 329.63314428399565]]
    piece, lastnote = playNotes(freqs)
    correct_values = {0: 0.0, 5000: -1.0940858, 10000: 0.97059435, 15000: -0.118024155, 20000: 1.0746915, 25000: -0.4021347, 30000: -0.011225048, 35000: -1.5115523, 40000: 1.273912}
    for i in range(0, 44100, 5000):
        assert np.linalg.norm(piece[i] - correct_values[i]) <= 0.05

def test_voices_to_freq():
    voices = ["c' d' e' f' g' a' b' c''"]
    keys, freqs, _ = convertNotes(voices)
    assert np.array_equal(keys[0], [12, 14, 16, 17, 19, 21, 23, 24])
    arrtest = np.array([260.63, 294.67, 330.633, 350.234, 393.002, 441.007, 494.892, 524.26])
    assert np.linalg.norm(np.array(freqs[0]) - arrtest) < 3

def test_voices_to_notes():
    config.play_audio = False
    voices = ["c' d' e'", "e' f' g'"]
    keys, freqs, _ = convertNotes(voices)
    piece, lastnote = playNotes(freqs)
    correct_values = {0: 0.0, 5000: -0.40214407, 10000: -0.19854277, 15000: 0.7271434, 20000: -0.18083608, 25000: -0.83695495, 30000: 0.92700917, 35000: -3.0091503, 40000: 2.7686481}
    for key in correct_values:
        assert piece[key] - correct_values[key] <= 0.05

def test_pipeline():
    config.play_audio = False
    voices = ["c' d' e'", "e' f' g'"]
    keys, freqs, _ = convertNotes(voices)
    piece, lastnote = playNotes(freqs)
    correct_values = {0: 0.0, 5000: -0.40214407, 10000: -0.19854277, 15000: 0.7271434, 20000: -0.18083608, 25000: -0.83695495, 30000: 0.92700917, 35000: -3.0091503, 40000: 2.7686481}
    for key in correct_values:
        assert piece[key] - correct_values[key] <= 0.05
    img = displayNotes(voices, '4/4')
    assert type(img) == Image

def test_Piece():
    p1 = Piece(60, '3/4')
    p1.addVoice("c'4 d'4 e'4 f'4 g'4 a'4 b'4 c''4 b'4 c''2.")
    p1.addVoice("c' d' e'", 4, instrument=42)
    assert type(p1.getScore()) == Image
    assert type(p1.midi) == MIDIFile