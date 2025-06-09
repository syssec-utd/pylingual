from drain3.persistence_handler import PersistenceHandler

class MemoryBufferPersistence(PersistenceHandler):

    def __init__(self):
        self.state = None

    def save_state(self, state):
        self.state = state

    def load_state(self):
        return self.state