from src.DAJIN2.core.classification import classify
from importlib import reload
reload(classify)

def test_calc_match_perfect():
    test = classify.calc_match('=A,=C,=G,=T')
    answer = 1.0
    assert test == answer

def test_calc_match_insertion():
    test = classify.calc_match('=A,=C,+T|+T|=G,=T')
    answer = 0.5
    assert test == answer

def test_calc_match_deletion():
    test = classify.calc_match('=A,-C,-G,=T')
    answer = 0.5
    assert test == answer

def test_calc_match_substitution():
    test = classify.calc_match('=A,*CT,=G,=T')
    answer = 0.75
    assert test == answer

def test_calc_match_unknown():
    test = classify.calc_match('=A,N,=G,=T')
    answer = 0.75
    assert test == answer