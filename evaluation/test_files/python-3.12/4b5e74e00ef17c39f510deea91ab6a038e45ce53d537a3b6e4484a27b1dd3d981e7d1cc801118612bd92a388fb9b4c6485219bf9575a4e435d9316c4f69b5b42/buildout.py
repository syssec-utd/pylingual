try:
    from zc.buildout.buildout import Buildout
except ImportError:
    raise ImportError("zc.buildout is not installed! \nIf you're in a buildout environment,\nenable the buildout extra requirement like this:\neggs = z3c.checkversions [buildout]\nIf you installed z3c.checkversions via pip,\nplease make sure to also install zc.buildout.")
from z3c.checkversions import base

class Checker(base.Checker):
    """checker class for a buildout
    """

    def __init__(self, *args, **kw):
        self.filename = kw.pop('filename')
        super().__init__(*args, **kw)

    def get_versions(self):
        print('# Checking buildout file %s' % self.filename)
        buildout = Buildout(self.filename, '')
        buildout_index = buildout['buildout'].get('index')
        if not self.__custom_url:
            self._set_index_url(buildout_index)
        return buildout['versions']