""" File Input/Output Utility Methods """
import os
from io import StringIO
from io import open as io_open
from csv import reader as csv_reader
from typing import Generator
from sys import platform
from pathlib import Path
from collections import defaultdict
from codecs import open as codecs_open
from json import load as json_load
from json import loads as json_loads
from json import dumps as json_dumps
from json.decoder import JSONDecodeError
from yaml import Loader
from yaml import YAMLError
from yaml import dump as yaml_dump
from yaml import load as yaml_load

class FileIO(object):
    """ File Input/Output Utility Methods """

    @staticmethod
    def local_directory() -> str:
        """ Retrieve a Platform Specific Local Directory

        Raises:
            NotImplementedError: Platform O/S Not Recognized

        Returns:
            str: absolute Path to a Local Directory
        """
        if platform == 'linux' or platform == 'linux2':
            return os.environ['HOME']
        elif platform == 'darwin':
            return os.environ['HOME']
        elif platform == 'win32':
            return os.environ['APPDATA']
        raise NotImplementedError(platform)

    @staticmethod
    def local_directory_by_name(folder_name: str) -> str:
        """ Create a Local Directory under a Platform Specific Directory

        Args:
            folder_name (str): the local directory to create

        Returns:
            str: absolute Path to Local Directory
        """
        local_path = FileIO.join(FileIO.local_directory(), folder_name)
        FileIO.exists_or_create(local_path)
        return local_path

    @staticmethod
    def normpath(path: str) -> str:
        """ Normalize Path to use forward slashes

        This differs from
            os.path.normpath
        in that the Python std lib call will normalize on a platform-specific basis

        This means a path like this
            alpha/bravo/charlie
        will become
            alpha\\bravo\\charlie
        on a Windows platform; which is silly, because forward slashes work just fine on Windows

        Args:
            path (str): the incoming path

        Returns:
            str: the outgoing path
        """
        if '\\' in path:
            path = path.replace('\\', '/')
            os.path.normpath
        return path

    @staticmethod
    def join(*args) -> str:
        return os.path.normpath(os.path.join(*args))

    @staticmethod
    def join_cwd(*args) -> str:
        return os.path.normpath(os.path.join(os.getcwd(), *args))

    @staticmethod
    def temp(data: object) -> str:
        """ Write a Data Object to a Temp File

        Args:
            data (object): any data object

        Raises:
            NotImplementedError: unrecognized data type
            ValueError: unrecognized data type

        Returns:
            str: the path the file was written to
        """
        _type = type(data)
        if _type not in [dict, list, str]:
            raise NotImplementedError(_type)
        path = FileIO.join(FileIO.local_directory(), 'temp.json')
        if _type == str:
            FileIO.write_string(data, path)
        else:
            FileIO.write_json(data, path)
        print(f'Wrote File to {path}')
        return path

    @staticmethod
    def exists(file_path: str) -> bool:
        """ Check if File or Directory exists

        Args:
            file_path (str): a file path

        Returns:
            bool: True if file or directory exists
        """
        return os.path.exists(file_path)

    @staticmethod
    def exists_or_error(file_path: str) -> None:
        """ Raise Exception if File Path does not exist

        Args:
            file_path (str): an input path

        Raises:
            FileNotFoundError: an input path
        """
        if not FileIO.exists(file_path):
            raise FileNotFoundError(file_path)

    @staticmethod
    def exists_or_create(file_path: str) -> None:
        """ Create File Path if File Path does not exist

        Args:
            file_path (str): an input path
        """
        if not FileIO.exists(file_path):
            FileIO.create_dir(file_path)

    @staticmethod
    def create_dir(dir_name: str) -> None:
        """ Create Directory (recursive)

        Args:
            dir_name (str): an input path
        """
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name)

    @staticmethod
    def get_file_name(file_path: str) -> str:
        """ Get the File Name From the File Path

        Args:
            file_path (str): the path to the file
                example: /root/temp-file.ext

        Returns:
            str: the filename only
                example: temp-file
        """
        file_name = os.path.basename(file_path)
        return os.path.splitext(file_name)[0]

    @staticmethod
    def debug(data: object) -> None:
        """ Debug Mechanism for Examining 'Stack Trace'

        Args:
            data (object): the JSON object

        Raises:
            ValueError: Stops Program Execution
        """
        file_path = os.path.join(os.environ['DESKTOP'], 'temp.json')
        FileIO.write_json(data, file_path=file_path)
        raise ValueError(f'Wrote Temp File: {file_path}')

    @staticmethod
    def write_json(data: object, file_path: str) -> None:
        """ Write JSON to File

        Args:
            data (object): the JSON object
            file_path (str): the absolute and qualified output file path
        """
        with io_open(file_path, 'w') as json_file:
            json_dump = json_dumps(data, indent=4, sort_keys=False, ensure_ascii=True)
            json_file.write(json_dump)

    @staticmethod
    def read_json(file_path: str) -> object:
        """ Read JSON from File

        Args:
            file_path (str): the absolute and qualified output file path
            file_encoding (str, optional): The output file encoding. Defaults to "utf-8".

        Returns:
            [type]: the JSON object
        """
        with open(file_path) as json_file:
            return json_load(json_file)

    @staticmethod
    def read_string(file_path: str, encoding: str='utf-8', replace_newlines: bool=False) -> str:
        """ Read String from File

        Args:
            file_path (str): the absolute and qualified input file path
            encoding (str, optional): the file encoding. Defaults to "utf-8".

        Returns:
            str: the file contents as a single string
        """
        with open(file_path, 'r', encoding=encoding) as myfile:
            if replace_newlines:
                return myfile.read().replace('\n', ' ')
            return myfile.read()

    @staticmethod
    def write_string(input_text: str, file_path: str, file_encoding: str='utf-8') -> None:
        """ Write String to File

        Args:
            input_text (str): the string contents to write to file
            file_path (str): the absolute and qualified input file path
            file_encoding (str, optional): the file encoding. Defaults to "utf-8".

        Raises:
            ValueError: Invalid Input
        """
        if not input_text or type(input_text) != str:
            raise ValueError
        target = codecs_open(file_path, mode='w', encoding=file_encoding)
        target.write(input_text)
        target.close()

    @staticmethod
    def write_lines(lines: list, file_path: str, file_encoding: str='utf-8') -> None:
        """ Write Lines to File

        Args:
            lines (list): the list to write to file
            file_path (str): the absolute and qualified input file path
            file_encoding (str, optional): the file encoding. Defaults to "utf-8".

        Raises:
            ValueError: Invalid Input
        """
        input_text = '\n'.join(lines)
        FileIO.write_string(input_text=input_text, file_path=file_path, file_encoding=file_encoding)

    @staticmethod
    def write_yaml(d: dict, file_path: str) -> None:
        """ Write YAML to File

        Args:
            d (dict): the py YAML dictionary
            file_path (str): the absolute and qualified output file path
        """
        with open(file_path, 'w') as file:
            documents = yaml_dump(d, file)

    @staticmethod
    def read_yaml(file_path: str) -> dict:
        """ Read YAML from File

        Args:
            file_path (str): the absolute and qualified input file path

        Raises:
            ValueError: the file is not valid YAML

        Returns:
            dict: a py YAML dictionary
        """
        FileIO.exists_or_error(file_path)
        with open(file_path, 'r') as stream:
            try:
                return yaml_load(stream, Loader)
            except YAMLError:
                raise ValueError(f'Invalid YAML File: {file_path}')

    @staticmethod
    def read_lines(file_path: str, file_encoding: str='utf-8') -> list:
        """ Read Lines of a File into a List

        Args:
            file_path (str): the absolute and qualified input file path
            file_encoding (str, optional): the file encoding. Defaults to "utf-8".

        Returns:
            list: each line in the file as a list
        """
        target = codecs_open(file_path, mode='r', encoding=file_encoding)
        lines = [x.replace('\n', '').strip() for x in target.readlines() if x]
        target.close()
        return lines

    @staticmethod
    def yield_lines(file_path: str, file_encoding: str='utf-8') -> list:
        """Read Lines of a File using a yield Generator

        Args:
            file_path (str): the absolute and qualified input file path
            file_encoding (str, optional): the file encoding. Defaults to "utf-8".

        Returns:
            Generator: a yield function
            Sample Output:
                ['A3.26	1993	2	2']
                ['A3.26	1994	2	2']
                ['A3.26	1995	6	6']
                ['A3.26	1996	4	4']
                ['A3.26	1997	5	5']
                ['A3.26	1998	1	1']
                ['A3.26	1999	4	3']

            Notes:
                each output line is a list with one element that requires independent delimitation            
        """
        with codecs_open(file_path, mode='r', encoding=file_encoding) as f:
            for line in csv_reader(f):
                yield line

    @staticmethod
    def has_files(directory: str, extension: str) -> bool:
        """ Check if files exist in a directory by extension

        Args:
            file_path (str): the absolute and qualified directory path
            extension (str): the extendion to check for

        Returns:
            bool: True if files exist
        """
        return len(FileIO.load_files(directory, extension))

    @staticmethod
    def load_files(directory: str, extension: str, limit: int=None, blacklist: list=None, recursive: bool=False) -> list:
        """ Load Files from a directory

        Args:
            directory (str): the absolute and qualified directory path
            extension (str): the file extension to load
            recursive (bool, optional): loads files recursively if set to True. Defaults to False.
            limit (int, optional): The number of files to load. Defaults to None.
            blacklist (list, optional): an list of File Names to exclude. Defaults to None.

        Returns:
            list: list of files
        """

        def non_recursive_loader() -> list:
            files = os.listdir(directory)
            files = [f for f in files if f.endswith(extension)]
            if limit and len(files) >= limit:
                files = files[:limit]
            files = [os.path.normpath(os.path.join(directory, f)) for f in files]
            return files

        def recursive_loader() -> list:
            results = []
            for (dirpath, dirnames, files) in os.walk(directory):
                files = [x for x in files if x.lower().endswith(extension)]
                for name in files:
                    path = os.path.join(dirpath, name)
                    if not is_valid(path):
                        continue
                    results.append(path)
                    if limit and len(results) >= limit:
                        return results
            return results

        def load_files() -> list:
            if recursive:
                return recursive_loader()
            return non_recursive_loader()

        def is_valid(a_file: str) -> bool:
            if blacklist and len(blacklist):
                for entry in blacklist:
                    if entry in a_file:
                        return False
            return True
        return [x for x in load_files() if is_valid(x)]

    @staticmethod
    def load_all_files(directory: str, exclude: list=None) -> list:
        """ Load all Files from a directory and key by extension

        Args:
            directory (str): the absolute and qualified directory path
            exclude (list): a list of folders (or sub-folders) to exclude

        Returns:
            list: list of files
        """
        d = defaultdict(list)
        if not exclude:
            exclude = []
        exclude_sub = []
        for sub_folder in exclude:
            if os.path.sep not in sub_folder:
                exclude_sub.append(f'{os.path.sep}{sub_folder}{os.path.sep}')
            else:
                exclude_sub.append(sub_folder)

        def load_files() -> list:
            results = []
            for (dirpath, _, files) in os.walk(directory):
                if os.path.basename(dirpath) in exclude:
                    continue

                def has_excluded_subfolder() -> bool:
                    for sub_folder in exclude_sub:
                        if sub_folder in dirpath:
                            return True
                    return False
                if has_excluded_subfolder():
                    continue
                for name in files:
                    results.append(os.path.normpath(os.path.join(dirpath, name)))
            return results
        for f in load_files():
            d[FileIO.extension(f)].append(f)
        return dict(d)

    @staticmethod
    def load_all_folders(directory: str, exclude: list=None) -> list:
        """ Load all Folders from a directory

        Args:
            directory (str): the absolute and qualified directory path
            exclude (list): a list of folders (or sub-folders) to exclude

        Returns:
            list: list of folder base names
        """
        d_folders = defaultdict(list)
        if not exclude:
            exclude = []
        exclude_sub = []
        for sub_folder in exclude:
            if os.path.sep not in sub_folder:
                exclude_sub.append(f'{os.path.sep}{sub_folder}{os.path.sep}')
            else:
                exclude_sub.append(sub_folder)
        for (dirpath, _, files) in os.walk(directory):
            base_name = os.path.basename(dirpath)
            if base_name in exclude:
                continue

            def has_excluded_subfolder() -> bool:
                for sub_folder in exclude_sub:
                    if sub_folder in dirpath:
                        return True
                return False
            if has_excluded_subfolder():
                continue
            for name in files:
                d_folders[base_name].append(os.path.normpath(os.path.join(dirpath, name)))
        return dict(d_folders)

    def extension(file_name: str) -> str or None:
        """ Extract Extension from a File Name

        Args:
            file_name (str): a file name

        Returns:
            str: the file extension
        """
        ext = Path(file_name).suffix
        if ext.startswith('.'):
            return ext[1:]
        if not len(ext):
            return None
        return ext

    @staticmethod
    def parse_yaml(file_data: str) -> dict:
        """ Read YAML from String

        Args:
            file_data (str): the string-ified YAML data

        Raises:
            ValueError: the file data is not valid YAML

        Returns:
            dict: a py YAML dictionary
        """
        try:
            return yaml_load(StringIO(file_data), Loader)
        except YAMLError:
            raise ValueError(f'Invalid YAML Data')

    @staticmethod
    def parse_json(file_data: str) -> dict:
        """ Read JSON from String

        Args:
            file_data (str): the string-ified JSON data

        Raises:
            ValueError: the file data is not valid JSON

        Returns:
            dict: a py JSON dictionary
        """
        try:
            file_data_type = type(file_data)
            if file_data_type == dict:
                return dict(file_data)
            if file_data_type == list:
                return list(file_data)
            return json_loads(file_data)
        except JSONDecodeError:
            raise ValueError(f'Invalid JSON Data')