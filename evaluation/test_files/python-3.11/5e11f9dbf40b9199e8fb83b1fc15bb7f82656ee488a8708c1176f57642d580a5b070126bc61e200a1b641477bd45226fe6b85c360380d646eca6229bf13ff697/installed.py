import pkg_resources
from z3c.checkversions import base

class Checker(base.Checker):
    """Checker class for installed packages
    """

    def get_versions(self, level=0):
        working_set = pkg_resources.working_set
        versions = {d.key: d.version for d in working_set}
        print('# Checking your installed distributions')
        return versions