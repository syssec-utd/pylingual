import os
import platform
import pytest
import textwrap
from conan.tools.microsoft.visual import vcvars_command
from ._base import BaseIntelTestCase
from conans.test.assets.sources import gen_function_cpp
from ..microsoft.test_msbuild import sln_file, myapp_vcxproj
conanfile_py = textwrap.dedent('\n    from conans import ConanFile, MSBuild, MSBuildToolchain\n\n    class App(ConanFile):\n        settings = \'os\', \'arch\', \'compiler\', \'build_type\'\n        exports_sources = "MyProject.sln", "MyApp/MyApp.vcxproj", "MyApp/MyApp.cpp"\n        generators = "msbuild"\n        requires = "hello/0.1"\n\n        def generate(self):\n            tc = MSBuildToolchain(self)\n            tc.generate()\n\n        def build(self):\n            msbuild = MSBuild(self)\n            msbuild.build("MyProject.sln")\n')

@pytest.mark.tool_cmake
@pytest.mark.tool_msbuild
@pytest.mark.tool_icc
@pytest.mark.xfail(reason='Intel compiler not installed yet on CI')
@pytest.mark.skipif(platform.system() != 'Windows', reason='msbuild requires Windows')
class MSBuildIntelTestCase(BaseIntelTestCase):

    def test_use_msbuild_toolchain(self):
        self.t.save({'profile': self.profile})
        self.t.run('new hello/0.1 -s')
        self.t.run('create . hello/0.1@ -pr:h=profile')
        app = gen_function_cpp(name='main', includes=['hello'], calls=['hello'])
        self.t.save({'conanfile.py': conanfile_py, 'MyProject.sln': sln_file, 'MyApp/MyApp.vcxproj': myapp_vcxproj, 'MyApp/MyApp.cpp': app, 'profile': self.profile}, clean_first=True)
        self.t.run('install . -pr:h=profile -if=conan')
        self.assertIn('conanfile.py: MSBuildToolchain created conan_toolchain_release_x64.props', self.t.out)
        self.t.run('build . -if=conan')
        self.assertIn('Visual Studio 2017', self.t.out)
        self.assertIn("[vcvarsall.bat] Environment initialized for: 'x64'", self.t.out)
        exe = 'x64\\Release\\MyApp.exe'
        self.t.run_command(exe)
        self.assertIn('main __INTEL_COMPILER1910', self.t.out)
        vcvars = vcvars_command(version='15', architecture='x64')
        dumpbind_cmd = '%s && dumpbin /dependents "%s"' % (vcvars, exe)
        self.t.run_command(dumpbind_cmd)
        self.assertIn('KERNEL32.dll', self.t.out)
        os.unlink(os.path.join(self.t.current_folder, exe))
        cmd = vcvars + ' && msbuild "MyProject.sln" /p:Configuration=Release /p:Platform=x64 /p:PlatformToolset="Intel C++ Compiler 19.1"'
        self.t.run_command(cmd)
        self.assertIn('Visual Studio 2017', self.t.out)
        self.assertIn("[vcvarsall.bat] Environment initialized for: 'x64'", self.t.out)
        self.t.run_command(exe)
        self.assertIn('main __INTEL_COMPILER1910', self.t.out)
        self.t.run_command(dumpbind_cmd)
        self.assertIn('KERNEL32.dll', self.t.out)