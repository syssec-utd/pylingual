from uvirun import *
import nltk
from nltk.corpus import wordnet

@app.get('/nltk/tokenize', tags=['nltk'])
def nltk_tokenize(snt: str='i hate study on monday. Jim like rabbit.', aslist: bool=True):
    arr = nltk.word_tokenize(snt)
    return arr if aslist else ' '.join(arr)

@app.get('/nltk/postag', tags=['nltk'])
def nltk_postag(snt: str='i hate study on monday. Jim like rabbit.'):
    words = nltk.word_tokenize(snt)
    pos_tags = nltk.pos_tag(words)
    return pos_tags

@app.get('/nltk/synset/pos', tags=['nltk'])
def nltk_synset_pos(word: str='consider'):
    """ v: verb, n:noun, a:adj, r:adv """
    return wordnet.synsets(word)[0].pos()
_wn_pos = {'VERB': wordnet.VERB, 'NOUN': wordnet.NOUN, 'ADJ': wordnet.ADJ, 'ADV': wordnet.ADV}

@app.get('/nltk/synset/synonyms', tags=['nltk'])
def nltk_synset_synonyms(word: str='overcome', pos: str=None):
    """ pos:  VERB/NOUN/ADJ/ADV """
    pos = _wn_pos.get(pos, None)
    _synsets = wordnet.synsets(word, pos) if pos else wordnet.synsets(word)
    return set([l.name() for syn in _synsets for l in syn.lemmas()])

@app.get('/nltk/synset/antonyms', tags=['nltk'])
def nltk_synset_antonyms(word: str='increase'):
    return set([l.antonyms()[0].name() for syn in wordnet.synsets(word) for l in syn.lemmas() if l.antonyms()])

@app.get('/nltk/ngrams', tags=['nltk'])
def nltk_ngrams(snt: str='The quick fox jumped over the lazy dog.', n: int=3, tokenized: bool=False):
    """ # ['The quick fox', 'quick fox jumped', 'fox jumped over', 'jumped over the', 'over the lazy', 'the lazy dog', 'lazy dog .'] """
    from nltk import ngrams
    n_grams = ngrams(snt.split() if tokenized else nltk_tokenize(snt), n)
    return [' '.join(grams) for grams in n_grams]
if __name__ == '__main__':
    print(nltk_synset_synonyms())
'\nhttps://www.nltk.org/howto/wordnet.html\n>>> wn.synsets(\'dog\')\n[Synset(\'dog.n.01\'), Synset(\'frump.n.01\'), Synset(\'dog.n.03\'), Synset(\'cad.n.01\'),\nSynset(\'frank.n.02\'), Synset(\'pawl.n.01\'), Synset(\'andiron.n.01\'), Synset(\'chase.v.01\')]\n>>> wn.synsets(\'dog\', pos=wn.VERB)\n[Synset(\'chase.v.01\')]\n\nThe other parts of speech are NOUN, ADJ and ADV. A synset is identified with a 3-part name of the form: word.pos.nn:\n\n>>> wn.synset(\'dog.n.01\')\nSynset(\'dog.n.01\')\n>>> print(wn.synset(\'dog.n.01\').definition())\na member of the genus Canis (probably descended from the common wolf) that has been domesticated by man since prehistoric times; occurs in many breeds\n>>> len(wn.synset(\'dog.n.01\').examples())\n1\n>>> print(wn.synset(\'dog.n.01\').examples()[0])\nthe dog barked all night\n>>> wn.synset(\'dog.n.01\').lemmas()\n[Lemma(\'dog.n.01.dog\'), Lemma(\'dog.n.01.domestic_dog\'), Lemma(\'dog.n.01.Canis_familiaris\')]\n>>> [str(lemma.name()) for lemma in wn.synset(\'dog.n.01\').lemmas()]\n[\'dog\', \'domestic_dog\', \'Canis_familiaris\']\n>>> wn.lemma(\'dog.n.01.dog\').synset()\nSynset(\'dog.n.01\')\n\nhttps://www.educba.com/nltk-wordnet/\nfrom nltk.corpus import wordnet\npy_arr = wordnet.synsets("python")\nprint (py_arr[0].name())\nprint (py_arr[0].lemmas()[0].name())\nprint (py_arr[0].definition())\nprint (py_arr[0].examples())\n\nhttps://www.cnblogs.com/chen8023miss/p/11458571.html\n\nsynonyms = []\nantonyms = []\n\nfor syn in wordnet.synsets("good"):\n    for l in syn.lemmas():\n        synonyms.append(l.name())\n        if l.antonyms():\n            antonyms.append(l.antonyms()[0].name())\n\nprint(set(synonyms))\nprint(set(antonyms))\n\n{\'beneficial\', \'just\', \'upright\', \'thoroughly\', \'in_force\', \'well\', \'skilful\', \'skillful\', \'sound\', \'unspoiled\',\n\nw1 = wordnet.synset(\'ship.n.01\')\nw2 = wordnet.synset(\'boat.n.01\')\nprint(w1.wup_similarity(w2))\n\n# 0.9090909090909091\n\nw1 = wordnet.synset(\'ship.n.01\')\nw2 = wordnet.synset(\'car.n.01\')\nprint(w1.wup_similarity(w2))\n\n# 0.6956521739130435\n\nw1 = wordnet.synset(\'ship.n.01\')\nw2 = wordnet.synset(\'cat.n.01\')\nprint(w1.wup_similarity(w2))\n\n# 0.38095238095238093\n'