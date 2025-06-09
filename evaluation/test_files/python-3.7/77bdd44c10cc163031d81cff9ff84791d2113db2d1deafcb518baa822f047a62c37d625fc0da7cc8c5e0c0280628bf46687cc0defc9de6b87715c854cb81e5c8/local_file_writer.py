from warnings import warn
from tellius_data_manager.persistence_operators.dataframe_operators.dataframe_writers.dataframe_writer_factory import DataframeWriterFactory
from tellius_data_manager.pipes.writers.file_writer import FileWriter

class LocalFileWriter(FileWriter):

    def __init__(self, **kwargs):
        warn(f'{self.__class__.__name__} will be deprecated.', DeprecationWarning, stacklevel=2)
        super().__init__(**kwargs)
        self._df_writer = DataframeWriterFactory.generate(configuration=kwargs['writer'])