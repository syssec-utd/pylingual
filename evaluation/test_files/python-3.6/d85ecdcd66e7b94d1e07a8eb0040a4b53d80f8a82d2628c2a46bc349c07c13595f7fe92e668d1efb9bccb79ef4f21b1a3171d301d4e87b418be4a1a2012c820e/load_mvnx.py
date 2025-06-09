"""
Script to load an mvnx

"""
import xml.etree.ElementTree as ET
import collections
import numpy as np
from .mvnx_file_accessor import MvnxFileAccessor
from ..src import mvn
ns = {'mvn': 'http://www.xsens.com/mvn/mvnx'}
FOOT_CONTACT_MAP = {'LeftFoot_Heel': {'type': 1, 'segment_index': mvn.SEGMENT_LEFT_FOOT, 'point_index': 2}, 'LeftFoot_Toe': {'type': 1, 'segment_index': mvn.SEGMENT_LEFT_TOE, 'point_index': 1}, 'RightFoot_Heel': {'type': 1, 'segment_index': mvn.SEGMENT_RIGHT_FOOT, 'point_index': 2}, 'RightFoot_Toe': {'type': 1, 'segment_index': mvn.SEGMENT_RIGHT_TOE, 'point_index': 1}}

def load_mvnx(file_name):
    """
    This function opens and reads the file as an mvnx formatted XML file

    :param file_name: Name of the file to open, must have full path and .mvnx extension
    :returns: A dictionary with the data from the mvnx file
    """
    mvnx_file = MvnxFileAccessor()
    init_file_data(mvnx_file)
    tree = ET.parse(file_name)
    root = tree.getroot()
    mvnx_file.file_data['meta_data']['version'] = root.get('version')
    comment_element = root.find('mvn:comment', ns)
    if comment_element is not None:
        mvnx_file.file_data['meta_data']['comments'] = comment_element.text
    subject_element = root.find('mvn:subject', ns)
    mvnx_file.file_data['meta_data']['name'] = subject_element.get('label')
    mvnx_file.file_data['meta_data']['color'] = subject_element.get('torsoColor')
    mvnx_file.file_data['meta_data']['sample_rate'] = subject_element.get('frameRate')
    mvnx_file.file_data['meta_data']['rec_date'] = subject_element.get('recDate')
    mvnx_file.file_data['meta_data']['original_filename'] = subject_element.get('originalFilename')
    mvnx_file.file_data['meta_data']['configuration'] = subject_element.get('configuration')
    mvnx_file.file_data['meta_data']['scenario'] = subject_element.get('userScenario')
    mvnx_file.file_data['meta_data']['quality'] = subject_element.get('processingQuality')
    segments_element = subject_element.find('mvn:segments', ns)
    segment_elements = segments_element.findall('mvn:segment', ns)
    mvnx_file.file_data['segments'] = parse_segments(segment_elements)
    mvnx_file.create_index_to_segment_dict()
    sensors_element = subject_element.find('mvn:sensors', ns)
    if sensors_element is not None:
        mvnx_file.file_data['sensors'] = parse_sensor(sensors_element, mvnx_file.file_data['segments']['names'])
    joints_element = subject_element.find('mvn:joints', ns)
    if joints_element is not None:
        mvnx_file.file_data['joints'] = parse_joints(joints_element, mvnx_file.file_data['segments'])
    ergo_joints_element = subject_element.find('mvn:ergonomicJointAngles', ns)
    if ergo_joints_element is not None:
        mvnx_file.file_data['ergo_joints'] = parse_ergo_joints(ergo_joints_element)
    foot_contact_definitions_element = subject_element.find('mvn:footContactDefinition', ns)
    if foot_contact_definitions_element is not None:
        foot_contact_definition_elements = foot_contact_definitions_element.findall('mvn:contactDefinition', ns)
        for foot_contact_definition_element in foot_contact_definition_elements:
            contact_label = foot_contact_definition_element.get('label')
            contact_index = int(foot_contact_definition_element.get('index'))
            mvnx_file.file_data['foot_contact_def'][contact_index] = FOOT_CONTACT_MAP[contact_label]
    for side in mvnx_file.file_data['finger_segments']['elements']:
        finger_segment_elements = subject_element.find('mvn:fingerTrackingSegments' + side.capitalize(), ns)
        if finger_segment_elements is not None:
            finger_segments = parse_segments(finger_segment_elements)
            mvnx_file.file_data['finger_segments']['elements'][side] = finger_segments['elements']
            mvnx_file.file_data['finger_segments']['names'][side] = finger_segments['names']
    for side in mvnx_file.file_data['finger_joints']['elements']:
        finger_joints_element = subject_element.find('mvn:fingerTrackingJoints' + side.capitalize(), ns)
        if finger_joints_element is not None:
            finger_segments = {'names': mvnx_file.file_data['finger_segments']['names'][side], 'elements': mvnx_file.file_data['finger_segments']['elements'][side]}
            finger_joints = parse_joints(finger_joints_element, finger_segments)
            mvnx_file.file_data['finger_joints']['elements'][side] = finger_joints['elements']
            mvnx_file.file_data['finger_joints']['names'][side] = finger_joints['names']
    frames_element = subject_element.find('mvn:frames', ns)
    (mvnx_file.file_data['frames'], mvnx_file.file_data['tpose'], mvnx_file.file_data['tpose_isb'], mvnx_file.file_data['identity']) = parse_frames(frames_element, mvnx_file)
    mvnx_file.reset_frame_window()
    return mvnx_file

def parse_sensor(sensors_element, segment_names):
    """
    Parse the sensor element

    :param sensors_element: The joint element to parse
    :param segment_names: a list with the segment names
    :return: a dictionary with sensor data indexed by sensor name and a list with the sensor names
    """
    sensor_elements = sensors_element.findall('mvn:sensor', ns)
    sensor_number = 0
    sensors = {}
    sensor_names = []
    for sensor_element in sensor_elements:
        sensor_name = sensor_element.get('label')
        sensor_names.append(sensor_name)
        sensor = {'type': 'Sensor', 'label': sensor_name, 'info': {'sensor_number': sensor_number, 'sensor_location': segment_names.index(sensor_name) + 1}}
        sensors[sensor_name] = sensor
        sensor_number += 1
    return {'names': sensor_names, 'elements': sensors}

def parse_joints(joints_element, segments):
    """
    Parse the joint element

    :param joints_element: The joint element to parse
    :param segments: The dictionary with segment data
    :return: a dictionary with joint data indexed by joint name and a list with the joint names
    """
    joint_elements = joints_element.findall('mvn:joint', ns)
    joints = []
    joint_names = []
    for joint_element in joint_elements:
        joint = {'label': joint_element.get('label')}
        joint_names.append(joint['label'])
        (segment1_index, point1_index) = get_connector_indices(joint_element, 'mvn:connector1', segments)
        (segment2_index, point2_index) = get_connector_indices(joint_element, 'mvn:connector2', segments)
        joint['seg_points'] = np.array([[segment1_index, point1_index], [segment2_index, point2_index]])
        joints.append(joint)
    return {'names': joint_names, 'elements': joints}

def parse_ergo_joints(ergo_joints_element):
    """
    Parse the ergo joint element

    :param ergo_joints_element: The joint element to parse
    :return: a dictionary with ergo joint data indexed by joint name and a list with the ergo joint names
    """
    ergo_joint_elements = ergo_joints_element.findall('mvn:ergonomicJointAngle', ns)
    ergo_joints = []
    ergo_joint_names = []
    for ergo_joint_index in range(len(ergo_joint_elements)):
        ergo_joint_element = ergo_joint_elements[ergo_joint_index]
        ergo_joint = {'label': ergo_joint_element.get('label'), 'index': ergo_joint_index, 'parent_segment': ergo_joint_element.get('parentSegment'), 'child_segment': ergo_joint_element.get('childSegment')}
        ergo_joint_names.append(ergo_joint['label'])
        ergo_joints.append(ergo_joint)
    return {'names': ergo_joint_names, 'elements': ergo_joints}

def parse_segments(segment_elements):
    """
    Parse the segment element

    :param segment_elements: The segment element to parse
    :return: a dictionary a list with the segment names and segment data indexed by segment name
    """
    segments = collections.OrderedDict()
    segment_names = []
    for segment_index in range(len(segment_elements)):
        segment_element = segment_elements[segment_index]
        segment_name = segment_element.get('label')
        segment_names.append(segment_name)
        segment = {'points_mvn': collections.OrderedDict(), 'type': 'Segment', 'info': {}, 'label': segment_name}
        info = {'segment_number': segment_index, 'point_label_from_index': {}, 'point_origin': '', 'adjacent_joints': []}
        points_element = segment_element.find('mvn:points', ns)
        point_elements = points_element.findall('mvn:point', ns)
        point_labels_from_index = {}
        for point_index in range(len(point_elements)):
            point_element = point_elements[point_index]
            point_name = point_element.get('label')
            point_labels_from_index[point_index] = point_name
            pos_b = point_element.find('mvn:pos_b', ns)
            segment['points_mvn'][point_name] = np.array([float(pos) for pos in pos_b.text.split(' ')])
            if np.sqrt(np.sum([sq * sq for sq in segment['points_mvn'][point_name]])) < 1e-05:
                info['point_origin'] = point_name
            if point_name[0] == 'j':
                info['adjacent_joints'].append(point_name)
        info['point_label_from_index'] = point_labels_from_index
        segment['info'] = info
        segments[segment_name] = segment
    return {'names': segment_names, 'elements': segments}

def get_connector_indices(joint_element, connector, segments):
    connector_element = joint_element.find(connector, ns)
    tokens = connector_element.text.split('/')
    segment_index = segments['names'].index(tokens[0])
    point_index = -1
    for (key, value) in segments['elements'][tokens[0]]['info']['point_label_from_index'].items():
        if value == tokens[1]:
            point_index = key
            break
    return (segment_index, point_index)

def parse_frames(frames_element, mvnx_file):
    """
    Parse the frames element

    :param frames_element: The frames element to parse
    :param mvnx_file: a dictionary containing, among others, a list of names
    :return: a dictionary with frames data
    """
    frames = {'time': [], 'segment_data': [], 'sensor_data': [], 'joint_data': [], 'joint_data_xzy': [], 'ergo_joint_data': [], 'ergo_joint_data_xzy': [], 'contacts_data': [], 'finger_segment_data': [], 'finger_joint_data': {'left': [], 'right': []}, 'finger_joint_data_xzy': {'left': [], 'right': []}}
    tpose = {}
    tpose_isb = {}
    identity = {}
    get_count = lambda element: int(element) if element is not None else None
    frames['segment_count'] = get_count(frames_element.get('segmentCount'))
    frames['sensor_count'] = get_count(frames_element.get('sensorCount'))
    frames['joint_count'] = get_count(frames_element.get('jointCount'))
    frames['finger_joint_count'] = get_count(frames_element.get('fingerJointCount'))
    frame_elements = frames_element.findall('mvn:frame', ns)
    for frame_element in frame_elements:
        if frame_element.get('type') == 'normal':
            frames['time'].append(frame_element.get('time'))
            frames['joint_data'].append(get_joint_data_from_frame(frame_element, 'jointAngle', mvnx_file.file_data['joints']['names']))
            frames['joint_data_xzy'].append(get_joint_data_from_frame(frame_element, 'jointAngleXZY', mvnx_file.file_data['joints']['names']))
            frames['ergo_joint_data'].append(get_joint_data_from_frame(frame_element, 'jointAngleErgo', mvnx_file.file_data['ergo_joints']['names']))
            frames['ergo_joint_data_xzy'].append(get_joint_data_from_frame(frame_element, 'jointAngleErgoXZY', mvnx_file.file_data['ergo_joints']['names']))
            frames['segment_data'].append(get_segment_data_from_frame(frame_element, mvnx_file.file_data['segments']['names']))
            frames['sensor_data'].append(get_sensor_data_from_frame(frame_element, mvnx_file.file_data['sensors']['names']))
            frames['contacts_data'].append(get_contact_data_from_frame(frame_element, mvnx_file.file_data['foot_contact_def']))
            frames['finger_segment_data'].append(get_finger_data_from_frame(frame_element, mvnx_file.file_data['finger_segments']['names']))
            for side in frames['finger_joint_data']:
                element_name = 'jointAngleFingers' + side.capitalize()
                frames['finger_joint_data'][side].append(get_joint_data_from_frame(frame_element, element_name, mvnx_file.file_data['finger_joints']['names'][side]))
                element_name = 'jointAngleFingers' + side.capitalize() + 'XZY'
                frames['finger_joint_data_xzy'][side].append(get_joint_data_from_frame(frame_element, element_name, mvnx_file.file_data['finger_joints']['names'][side]))
        elif frame_element.get('type') == 'tpose':
            tpose = get_t_pose_data_from_frame(frame_element, mvnx_file.file_data['segments']['names'])
        elif frame_element.get('type') == 'tpose-isb':
            tpose_isb = get_t_pose_data_from_frame(frame_element, mvnx_file.file_data['segments']['names'])
        elif frame_element.get('type') == 'identity':
            identity = get_t_pose_data_from_frame(frame_element, mvnx_file.file_data['segments']['names'])
    return (frames, tpose, tpose_isb, identity)

def get_joint_data_from_frame(frame_element, joint_element_name, joint_names):
    """
    Extract joint data from a frame

    :param frame_element: The frame element to process
    :param joint_element_name: The name of the frame element to process
    :param joint_names: a list with the joint names
    :return: a dictionary with joint data indexed by joint name
    """
    joint_data = collections.OrderedDict()
    angles = frame_element_as_floats(frame_element, joint_element_name)
    for index in range(len(joint_names)):
        joint_data[joint_names[index]] = get_3d_vector(angles, index)
    return joint_data

def get_t_pose_data_from_frame(frame_element, segment_names):
    """
    Extract segment data from a frame

    :param frame_element: The frame element to process
    :param segment_names: a list with the segment names
    :return: a dictionary with segment data indexed by segment name
    """
    t_pose = {'segments_counts': len(segment_names), 'segments': []}
    orientations = frame_element_as_floats(frame_element, 'orientation')
    offsets = frame_element_as_floats(frame_element, 'position')
    for index in range(len(segment_names)):
        segment = {'pos_g': get_3d_vector(offsets, index), 'q_gb': get_4d_vector(orientations, index)}
        t_pose['segments'].append(segment)
    return t_pose

def get_segment_data_from_frame(frame_element, segment_names):
    """
    Extract segment data from a frame

    :param frame_element: The frame element to process
    :param segment_names: a list with the segment names
    :return: a dictionary with segment data indexed by segment name
    """
    segment_data = collections.OrderedDict()
    orientations = frame_element_as_floats(frame_element, 'orientation')
    offsets = frame_element_as_floats(frame_element, 'position')
    velocities = frame_element_as_floats(frame_element, 'velocity')
    accelerations = frame_element_as_floats(frame_element, 'acceleration')
    angular_velocity = frame_element_as_floats(frame_element, 'angularVelocity')
    angular_acceleration = frame_element_as_floats(frame_element, 'angularAcceleration')
    for index in range(len(segment_names)):
        segment_name = segment_names[index]
        segment_data[segment_name] = collections.OrderedDict()
        segment_data[segment_name]['ori'] = get_4d_vector(orientations, index)
        segment_data[segment_name]['pos'] = get_3d_vector(offsets, index)
        segment_data[segment_name]['vel'] = get_3d_vector(velocities, index)
        segment_data[segment_name]['acc'] = get_3d_vector(accelerations, index)
        segment_data[segment_name]['ang_vel'] = get_3d_vector(angular_velocity, index)
        segment_data[segment_name]['ang_acc'] = get_3d_vector(angular_acceleration, index)
    center_of_mass = frame_element_as_floats(frame_element, 'centerOfMass')
    if center_of_mass:
        segment_data['com'] = {'pos': [], 'vel': [], 'acc': []}
        index = 0
        for com_field in segment_data['com']:
            segment_data['com'][com_field] = get_3d_vector(center_of_mass, index)
            index += 1
    return segment_data

def get_sensor_data_from_frame(frame_element, sensor_names):
    """
    Extract sensor data from a frame

    :param frame_element: The frame element to process
    :param sensor_names: a list with the segment names
    :return: a dictionary with sensor data indexed by sensor name
    """
    sensor_data = collections.OrderedDict()
    orientations = frame_element_as_floats(frame_element, 'sensorOrientation')
    free_accelerations = frame_element_as_floats(frame_element, 'sensorFreeAcceleration')
    magnetic_field = frame_element_as_floats(frame_element, 'sensorMagneticField')
    for index in range(len(sensor_names)):
        sensor_name = sensor_names[index]
        sensor_data[sensor_name] = collections.OrderedDict()
        sensor_data[sensor_name]['ori'] = get_4d_vector(orientations, index)
        sensor_data[sensor_name]['mag'] = get_4d_vector(magnetic_field, index)
        sensor_data[sensor_name]['acc'] = get_3d_vector(free_accelerations, index)
    return sensor_data

def get_finger_data_from_frame(frame_element, finger_segment_names):
    """
    Extract finger data from a frame

    :param frame_element: The frame element to process
    :param finger_segment_names: a list with the finger segment names
    :return: a dictionary with finger data indexed by finger name
    """
    finger_data = {'left': {}, 'right': {}}
    for side in finger_data:
        orientations = frame_element_as_floats(frame_element, 'orientationFingers' + side.capitalize())
        offsets = frame_element_as_floats(frame_element, 'positionFingers' + side.capitalize())
        for index in range(len(finger_segment_names[side])):
            finger_name = finger_segment_names[side][index]
            finger_data[side][finger_name] = collections.OrderedDict()
            finger_data[side][finger_name]['ori'] = get_4d_vector(orientations, index)
            finger_data[side][finger_name]['pos'] = get_3d_vector(offsets, index)
    return finger_data

def get_contact_data_from_frame(frame_element, foot_contact_def):
    """
    Extract contact data from a frame

    :param frame_element: The frame element to process
    :param foot_contact_def: a list with the foot contact definitions
    :return: a list with contacts
    """
    contact_data = []
    element_value = frame_element.find('mvn:footContacts', ns)
    if element_value is not None:
        contacts = [int(value) for value in element_value.text.split(' ')]
        for index in range(len(contacts)):
            if contacts[index] == 1:
                contact_data.append(foot_contact_def[index])
    return contact_data

def frame_element_as_floats(frame_element, element):
    """
    Find a named element in a frame element, extract the text from it, split that and return
    the values as an array of floats

    :param frame_element: The mvnx frame element to process
    :param element: The name of the sub element to find
    :return: an array of floating point values
    """
    element_value = frame_element.find('mvn:' + element, ns)
    return [float(value) for value in element_value.text.split(' ')] if element_value is not None else []

def get_4d_vector(raw_vector, index):
    return np.array(raw_vector[index * 4:index * 4 + 4])

def get_3d_vector(raw_vector, index):
    return np.array(raw_vector[index * 3:index * 3 + 3])

def init_file_data(mvnx_file):
    meta_data = {'version': '', 'original_filename': '', 'rec_date': '', 'name': '', 'color': '', 'comments': '', 'scenario': '', 'quality': '', 'sample_rate': 240}
    mvnx_file.file_data = {'segments': {}, 'finger_segments': {'names': {'left': {}, 'right': {}}, 'elements': {'left': collections.OrderedDict(), 'right': collections.OrderedDict()}}, 'sensors': {'names': [], 'elements': collections.OrderedDict()}, 'joints': {'names': [], 'elements': collections.OrderedDict()}, 'ergo_joints': {'names': [], 'elements': collections.OrderedDict()}, 'finger_joints': {'names': {'left': {}, 'right': {}}, 'elements': {'left': collections.OrderedDict(), 'right': collections.OrderedDict()}}, 'foot_contact_def': {}, 'frames': {}, 'tpose': {}, 'tpose_isb': {}, 'identity': {}, 'meta_data': meta_data}