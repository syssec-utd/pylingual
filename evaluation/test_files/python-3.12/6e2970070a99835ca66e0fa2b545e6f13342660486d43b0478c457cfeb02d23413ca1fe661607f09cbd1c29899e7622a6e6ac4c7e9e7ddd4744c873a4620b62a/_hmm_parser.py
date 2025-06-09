import os
from glam.parsing._base_parser import BaseParser
from glam.parsing.hmm import _hmm_model

class HMMParser(BaseParser):

    def __init__(self, model='default_model'):
        raise ValueError('Not implemented')
        self.type = 'HMMParser'
        self.model_path = os.path.join(os.path.dirname(__file__), model)
        self.model = self.load_model()