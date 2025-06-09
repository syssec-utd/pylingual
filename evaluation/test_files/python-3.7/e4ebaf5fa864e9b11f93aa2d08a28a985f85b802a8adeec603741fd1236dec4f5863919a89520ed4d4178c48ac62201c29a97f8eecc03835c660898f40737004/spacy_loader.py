from typing import Optional
import spacy
import sys
spacy_models = {}

def get_spacy(lang_model: Optional[str]=None):
    if lang_model is None:
        if len(spacy_models) == 1:
            return list(spacy_models.values())[0]
        else:
            from qasem.end_to_end_pipeline import DEFAULT_SPACY_MODEL
            lang_model = DEFAULT_SPACY_MODEL
    if lang_model not in spacy_models:
        try:
            nlp = spacy.load(lang_model)
        except OSError:
            print(f'Downloading SpaCy model {lang_model} for POS tagging (one-time)...\n', file=sys.stderr)
            spacy.cli.download(lang_model)
            nlp = spacy.load(lang_model)
        spacy_models[lang_model] = nlp
    return spacy_models[lang_model]