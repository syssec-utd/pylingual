import config.package

class Configure(config.package.GNUPackage):

    def __init__(self, framework):
        config.package.GNUPackage.__init__(self, framework)
        self.download = ['http://pyyaml.org/download/libyaml/yaml-0.2.5.tar.gz', 'http://ftp.mcs.anl.gov/pub/petsc/externalpackages/yaml-0.2.5.tar.gz']
        self.functions = ['yaml_parser_load']
        self.includes = ['yaml.h']
        self.liblist = [['libyaml.a']]
        return