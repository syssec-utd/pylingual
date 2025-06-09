import re
import os
import glob
import imghdr
from imghdr import tests
from natsort import natsorted

def get_project_config(line):
    r = re.compile('([^\\t]*)\\t*')
    return r.findall(line)

def test_jpeg1(h, f):
    """JPEG data in JFIF format"""
    if b'JFIF' in h[:23]:
        return 'jpeg'
JPEG_MARK = b'\xff\xd8\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f'

def test_jpeg2(h, f):
    """JPEG with small header"""
    if len(h) >= 32 and 67 == h[5] and (h[:32] == JPEG_MARK):
        return 'jpeg'

def test_jpeg3(h, f):
    """JPEG data in JFIF or Exif format"""
    if h[6:10] in (b'JFIF', b'Exif') or h[:2] == b'\xff\xd8':
        return 'jpeg'
tests.append(test_jpeg1)
tests.append(test_jpeg2)
tests.append(test_jpeg3)

def recursive_glob_image_files(input_path):
    support_img_format = ['png', 'jpg', 'bmp', 'jpeg']
    imgs_path = {}
    files_path = sorted(glob.glob(os.path.join(input_path, '**/*'), recursive=True))
    for file_path in select_image_files(files_path):
        if '@' not in file_path and (not os.path.isdir(file_path)):
            img_format = imghdr.what(file_path)
            if img_format in support_img_format:
                key = extract_file_key(input_path, file_path)
                imgs_path[key] = file_path
    return imgs_path

def select_image_files(file_list):
    image_file_list = []
    support_img_format = ('.png', '.jpg', '.bmp', '.jpeg')
    for file_name in file_list:
        if file_name.lower().endswith(support_img_format):
            image_file_list.append(file_name)
    return image_file_list

def recursive_glob_video_paths(input_path):
    support_img_format = ['png', 'jpg', 'bmp', 'jpeg']
    video_paths = {}
    for dirpath, dirnames, files in os.walk(input_path):
        if len(files) != 0 and dirpath != input_path:
            image_file_list = select_image_files(files)
            if len(image_file_list) != 0:
                key = extract_file_key(input_path, dirpath)
                video_paths[key] = {'path': dirpath, 'file_names': natsorted(image_file_list)}
    return video_paths

def recursive_glob_label_files(input_path):
    support_label_format = ['.json']
    labels_path = {}
    files_path = sorted(glob.glob(os.path.join(input_path, '**/*'), recursive=True))
    for file_path in files_path:
        if '@' not in file_path and (not os.path.isdir(file_path)):
            file_format = os.path.splitext(file_path)[1]
            if file_format in support_label_format:
                key = extract_file_key(input_path, file_path)
                labels_path[key] = file_path
    return labels_path

def extract_file_key(input_folder_path, file_path):
    key = os.path.abspath(file_path).replace(os.path.abspath(input_folder_path), '')
    key = '/'.join(key.split(os.sep)[1:])
    return key