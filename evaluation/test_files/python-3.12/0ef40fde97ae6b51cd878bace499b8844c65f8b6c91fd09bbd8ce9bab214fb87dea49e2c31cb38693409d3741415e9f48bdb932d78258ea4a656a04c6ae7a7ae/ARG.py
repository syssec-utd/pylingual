import distutils.spawn
import getopt
import os
import shutil
import sys
import time
import yaml
from arg import __version__
from arg.Common.argReportParameters import argReportParameters
from arg.Applications import Explorator
from arg.Applications.argGenerator import argGenerator
ARG_VERSION = __version__
if not __package__:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
else:
    sys.path.append('..')
common_dir = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(common_dir, '../Common/argTypes.yml'), 'r', encoding='utf-8') as t_file:
    Types = yaml.safe_load(t_file)

class Runner:
    """A class to describe ARG runner parameters
    """

    def __init__(self, version=None):
        """Class constructor
        """
        self.Explore = False
        self.Generate = False
        self.Assemble = False
        self.ParametersFile = None
        self.Parameters = None
        self.Version = version
        self.LatexProcessor = None
        self.TexFile = None

    @staticmethod
    def usage():
        """Provide online help
        """
        print('Usage:')
        print('\t [-h]                      Help: print this message and exit')
        print('\t [-e]                      run Explorator then Assembler')
        print('\t [-g]                      run Generator then Assembler')
        print('\t [-E]                      run Explorator')
        print('\t [-G]                      run Generator')
        print('\t [-A]                      run Assembler')
        print('\t [-p <parameters file>]    name of parameters file')
        print('\t [-l <LaTeX processor>]    name of LaTeX processor')
        print('\t [-t]                      generate just .tex file')
        sys.exit(0)

    def parse_line(self, default_parameters_filename, types=None):
        """Parse command line and fill artifact parameters
        """
        caller = ''
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'egEGAp:l:t')
        except getopt.GetoptError:
            self.usage()
            sys.exit(1)
        for o, a in opts:
            if o == '-h':
                self.usage()
                sys.exit(0)
            elif o == '-e':
                self.Assemble = True
                self.Explore = True
                caller = 'Explorator'
            elif o == '-g':
                self.Assemble = True
                self.Generate = True
                caller = 'Generator'
            elif o == '-E':
                self.Explore = True
                caller = 'Explorator'
            elif o == '-G':
                self.Generate = True
                caller = 'Generator'
            elif o == '-A':
                self.Assemble = True
                caller = 'Assembler'
            elif o == '-p':
                self.ParametersFile = a
            elif o == '-l':
                self.LatexProcessor = a
            elif o == '-t':
                self.TexFile = True
        if not self.ParametersFile:
            print("*  WARNING: no parameters file name provided; using '{}' by default.".format(default_parameters_filename))
            self.ParametersFile = default_parameters_filename
        self.Parameters = argReportParameters('ARG', self.ParametersFile, self.Version, types, self.LatexProcessor)
        self.Parameters.TexFile = self.TexFile
        return self.Parameters.check_parameters_file() and self.Parameters.parse_parameters_file() and self.Parameters.check_parameters(caller)

    def run(self):
        """Run ARG applications based on parsed values
        """
        concatenateStructureFile = False
        if self.Explore and os.path.isfile('{}.yml'.format(self.Parameters.StructureFile)):
            concatenateStructureFile = True
            shutil.copyfile(os.path.realpath('{}.yml'.format(self.Parameters.StructureFile)), os.path.realpath('{}_tmp.yml'.format(self.Parameters.StructureFile)))
        generator = argGenerator(self.Parameters)
        if self.Explore:
            Explorator.execute(self.Parameters)
        if self.Generate:
            generator.generate_artefacts()
        if concatenateStructureFile:
            with open(self.Parameters.StructureFile, 'w') as newFile:
                with open(self.Parameters.StructureFile, 'r') as existingFile:
                    newFile.write(existingFile.read())
        if self.Assemble:
            generator.assemble_report()

def main(types, version=None):
    """ ARG main method
    """
    t_start = time.time()
    sys_version = sys.version_info
    print('[ARG] ### Started with Python {}.{}.{}'.format(sys_version.major, sys_version.minor, sys_version.micro))
    default_parameters_filename = types.get('DefaultParametersFile')
    runner = Runner(version)
    runner.parse_line(default_parameters_filename, types)
    runner.run()
    dt = time.time() - t_start
    print('[ARG] Process completed in {} seconds. ###'.format(dt))
if __name__ == '__main__':
    'Main ARG routine\n    '
    main(Types, ARG_VERSION)