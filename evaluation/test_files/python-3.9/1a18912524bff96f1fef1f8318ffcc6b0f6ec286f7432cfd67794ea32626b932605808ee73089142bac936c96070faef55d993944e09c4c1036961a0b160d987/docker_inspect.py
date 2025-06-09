"""
DockerInspect - Command ``docker inspect --type={TYPE}``
========================================================

This module parses the output of the ``docker inspect`` command.  This uses
the ``core.marshalling.unmarshal`` function to parse the JSON output from the
commands.  The parsed data can be accessed a dictionary via the object itself.

"""
from insights import parser, CommandParser
from insights.core.marshalling import unmarshal
from insights.parsers import SkipException
from insights.specs import Specs
from insights.util import deprecated

class DockerInspect(CommandParser, dict):
    """
    .. warning::
        This class is deprecated, please use
        :py:class:`insights.parsers.containers_inspect.ContainersInspect` instead.

    Parse the output of command "docker inspect --type=image" and "docker
    inspect --type=container".  The output of these two commands is formatted
    as JSON, so "json.loads" is an option to parse the output in the future.

    Raises:
        SkipException: If content is not provided
    """

    def __init__(self, *args, **kwargs):
        deprecated(DockerInspect, 'Please use the :class:`insights.parsers.containers_inspect.ContainersInspect` instead.', '3.2.25')
        super(DockerInspect, self).__init__(*args, **kwargs)

    def parse_content(self, content):
        if not content:
            raise SkipException
        content = '\n'.join(list(content))
        try:
            inspect_data = unmarshal(content)
            self.update(inspect_data[0])
        except:
            raise SkipException

    @property
    def data(self):
        return self

@parser(Specs.docker_image_inspect)
class DockerInspectImage(DockerInspect):
    """
    Parse docker image inspect output using the DockerInspect parser class.

    Sample input::

        [
            {
                "Id": "882ab98aae5394aebe91fe6d8a4297fa0387c3cfd421b2d892bddf218ac373b2",
                "RepoTags": [
                    "rhel7_imagemagick:latest"
                ],
                "RepoDigests": [],
        ...

    Examples:

        >>> image['Id'] == '882ab98aae5394aebe91fe6d8a4297fa0387c3cfd421b2d892bddf218ac373b2'
        True
        >>> image['RepoTags'][0] == 'rhel7_imagemagick:latest'
        True

    """
    pass

@parser(Specs.docker_container_inspect)
class DockerInspectContainer(DockerInspect):
    """
    .. warning::
        This parser is deprecated, please use
        :py:class:`insights.parsers.containers_inspect.ContainersInspect` instead.

    Parse docker container inspect output using the DockerInspect parser class.

    Sample input::

        [
            {
                "Id": "97d7cd1a5d8fd7730e83bb61ecbc993742438e966ac5c11910776b5d53f4ae07",
                "Created": "2016-06-23T05:12:25.433469799Z",
                "Path": "/bin/bash",
                "Args": [],
                "Name": "/hehe2",
                "State": {
                    "Status": "running",
                    "Running": true,
                    "Paused": false,
                    "Restarting": false,
            ...

    Examples:

        >>> container['Id'] == '97d7cd1a5d8fd7730e83bb61ecbc993742438e966ac5c11910776b5d53f4ae07'
        True
        >>> container['Name'] == '/hehe2'
        True
        >>> container.get('State').get('Paused') # sub-dictionaries
        False

    """

    def __init__(self, *args, **kwargs):
        deprecated(DockerInspectContainer, 'Please use the :class:`insights.parsers.containers_inspect.ContainersInspect` instead.', '3.2.25')
        super(DockerInspectContainer, self).__init__(*args, **kwargs)