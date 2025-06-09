import os
import pytest
import textwrap
from conans.test.assets.sources import gen_function_cpp
from conans.test.functional.toolchains.meson._base import TestMesonBase

@pytest.mark.tool_pkg_config
class MesonTest(TestMesonBase):
    _test_package_meson_build = textwrap.dedent("\n        project('test_package', 'cpp')\n        hello = dependency('hello', version : '>=0.1')\n        test_package = executable('test_package', 'test_package.cpp', dependencies: hello)\n        test('test package', test_package)\n        ")
    _test_package_conanfile_py = textwrap.dedent('\n        import os\n        from conan import ConanFile\n        from conan.tools.meson import Meson, MesonToolchain\n\n\n        class TestConan(ConanFile):\n            settings = "os", "compiler", "build_type", "arch"\n            generators = "pkg_config"\n\n            def layout(self):\n                self.folders.build = "build"\n\n            def generate(self):\n                tc = MesonToolchain(self)\n                tc.generate()\n\n            def build(self):\n                meson = Meson(self)\n                meson.configure()\n                meson.build()\n\n            def test(self):\n                meson = Meson(self)\n                meson.configure()\n                meson.test()\n        ')

    def test_reuse(self):
        self.t.run('new hello/0.1 -s')
        test_package_cpp = gen_function_cpp(name='main', includes=['hello'], calls=['hello'])
        self.t.save({os.path.join('test_package', 'conanfile.py'): self._test_package_conanfile_py, os.path.join('test_package', 'meson.build'): self._test_package_meson_build, os.path.join('test_package', 'test_package.cpp'): test_package_cpp})
        self.t.run('create . hello/0.1@ %s' % self._settings_str)
        self._check_binary()