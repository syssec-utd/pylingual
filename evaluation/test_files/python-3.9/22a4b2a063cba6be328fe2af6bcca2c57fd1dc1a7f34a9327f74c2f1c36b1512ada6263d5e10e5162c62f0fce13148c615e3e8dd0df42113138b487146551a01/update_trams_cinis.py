from libcnmc.core import UpdateFile

class UpdateCINISTrams(UpdateFile):

    def __init__(self, **kwargs):
        super(UpdateCINISTrams, self).__init__(**kwargs)
        self.header = ['num_tram', 'cini']
        self.search_keys = [('num_tram', 'name')]
        self.object = self.connection.GiscedataAtTram