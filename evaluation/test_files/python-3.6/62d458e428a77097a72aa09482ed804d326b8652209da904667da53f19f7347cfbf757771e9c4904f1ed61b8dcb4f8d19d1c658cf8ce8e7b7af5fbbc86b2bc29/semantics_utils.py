import os
from collections import OrderedDict
import igibson
from igibson.utils.constants import MAX_CLASS_COUNT, SemanticClass

def get_class_name_to_class_id(starting_class_id=SemanticClass.SCENE_OBJS + 1):
    """
    Get mapping from semantic class name to class id

    :param starting_class_id: starting class id for scene objects
    """
    category_txt = os.path.join(igibson.ig_dataset_path, 'metadata', 'categories.txt')
    class_name_to_class_id = OrderedDict()
    class_name_to_class_id['agent'] = SemanticClass.ROBOTS
    if os.path.isfile(category_txt):
        with open(category_txt) as f:
            for line in f.readlines():
                assert starting_class_id < SemanticClass.DIRT, 'Class ID overflow'
                class_name_to_class_id[line.strip()] = starting_class_id
                starting_class_id += 1
    return class_name_to_class_id

def get_room_name_to_room_id(starting_room_id=1):
    """
    Get mapping from room name to room id
    """
    category_txt = os.path.join(igibson.ig_dataset_path, 'metadata', 'room_categories.txt')
    room_name_to_room_id = OrderedDict()
    if os.path.isfile(category_txt):
        with open(category_txt) as f:
            for line in f.readlines():
                room_name_to_room_id[line.strip()] = starting_room_id
                starting_room_id += 1
    return room_name_to_room_id
CLASS_NAME_TO_CLASS_ID = get_class_name_to_class_id()
ROOM_NAME_TO_ROOM_ID = get_room_name_to_room_id()