"""
This module provides convenience methods for writing of the files that represent the
artifacts.
"""
from hana_ml.artifacts.utils import FileHandler
from hana_ml.artifacts.utils import StringUtils

class FileWriterBase(object):
    """
    This class provides helper function for file writing
    """

    def __init__(self, config):
        """
        This is main entry point.

        Parameters
        ----------
        config : dict
            Central config object
        """
        self.file_handler = FileHandler()
        self.config = config

    def write_content(self, path, filename, content=''):
        """
        Write the content to a file

        Parameters
        ----------
        path : str
            Physical location
        filename : str
            Filename to write
        content : str
            Content of the file
        """
        self.file_handler.write_text_file(path, filename, content)

    def write_template(self, path, filename, template_file, replacements={}):
        """
        Use a template of af file content and replace placeholders with
        the content to be written en then write the content to a file.

        Parameters
        ----------
        path : str
            Physical location
        filename : str
            Filename to write
        template_file : str
            Location of the template file
        replacements : dict
            Replacements for the template placeholders
        """
        with open(template_file, 'r') as temp:
            file_content = temp.read()
        if replacements:
            file_content = StringUtils.multi_replace(file_content, replacements)
        self.write_content(path, filename, file_content)

    def add_config_entry(self, key, value):
        """
        Convenience method to add data to the config under the provided key

        Parameters
        ----------
        key: str
            The key under which the value needs to be stored
        value: object
            Object that will be stored under the provided key
        """
        self.config.add_entry(key, value)

    def get_config_entry(self, key):
        """
        Convenience method to get data from the config using the provided key

        Parameters
        ----------
        key: str
            The key under which the value needs to be stored

        Returns
        -------
        value: object
            Object that will be stored under the provided key
        """
        return self.config.get_entry(key)