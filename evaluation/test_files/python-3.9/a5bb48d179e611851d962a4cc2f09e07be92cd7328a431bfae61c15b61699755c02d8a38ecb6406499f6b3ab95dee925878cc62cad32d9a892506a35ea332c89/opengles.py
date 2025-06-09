import config.package
import os

class Configure(config.package.Package):

    def __init__(self, framework):
        config.package.Package.__init__(self, framework)
        self.functions = []
        self.includes = []
        self.worksonWindows = 0
        return

    def setupDependencies(self, framework):
        config.package.Package.setupDependencies(self, framework)
        return

    def configureLibrary(self):
        self.addDefine('HAVE_OPENGL', 1)
        self.addDefine('HAVE_OPENGLES', 1)