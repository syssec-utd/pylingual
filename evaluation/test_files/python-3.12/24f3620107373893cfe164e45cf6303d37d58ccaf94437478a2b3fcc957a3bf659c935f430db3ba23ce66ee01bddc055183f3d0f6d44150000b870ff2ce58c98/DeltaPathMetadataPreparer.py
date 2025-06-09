from featurestorebundle.delta.PathCreator import PathCreator
from featurestorebundle.delta.metadata.schema import get_metadata_schema, get_metadata_pk_columns

class DeltaPathMetadataPreparer:

    def __init__(self, path_creator: PathCreator):
        self.__path_creator = path_creator

    def prepare(self, path: str):
        self.__path_creator.create_if_not_exists(path, get_metadata_schema(), get_metadata_pk_columns()[0].name)