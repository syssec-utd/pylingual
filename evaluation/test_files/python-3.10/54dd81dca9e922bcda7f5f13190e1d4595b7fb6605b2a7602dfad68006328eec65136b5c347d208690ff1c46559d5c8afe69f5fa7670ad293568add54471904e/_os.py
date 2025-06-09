from typing import Optional
from dissect.target.filesystem import Filesystem
from dissect.target.plugins.os.unix.linux._os import LinuxPlugin
from dissect.target.target import Target

class DebianPlugin(LinuxPlugin):

    @classmethod
    def detect(cls, target: Target) -> Optional[Filesystem]:
        for fs in target.filesystems:
            if fs.exists('/etc/network/interfaces') or fs.exists('/etc/debian_version') or fs.exists('/etc/dpkg/'):
                return fs
        return None