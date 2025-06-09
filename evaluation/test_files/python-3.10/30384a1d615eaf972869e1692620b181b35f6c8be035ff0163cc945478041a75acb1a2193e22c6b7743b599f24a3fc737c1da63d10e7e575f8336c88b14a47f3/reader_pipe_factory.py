from tellius_data_manager.pipes.pipe_factory import PipeFactory
from tellius_data_manager.pipes.readers.reader_pipe import ReaderPipe
from tellius_data_manager.pipes.transformers.transformer_pipe import TransformerPipe

class ReaderPipeFactory(PipeFactory):
    """Factory abstraction designed to generate Pipe objects given the class name and the configuration (as a dict)."""
    _cls_type = ReaderPipe