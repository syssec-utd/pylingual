from typing import Dict
from watchmen_model.admin import Topic
from watchmen_model.common import TopicId
from watchmen_storage import UnexpectedStorageException
object_directory: Dict[TopicId, str] = {}

def register_directory(topic: Topic) -> None:
    object_directory[topic.topicId] = topic.name

def find_directory(name: str) -> str:
    directory = object_directory.get(name)
    if directory is None:
        raise UnexpectedStorageException(f'Table[{name}] definition not found.')
    return directory