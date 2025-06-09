import textwrap
from conans.model.ref import ConanFileReference
from conans.test.utils.tools import TestClient

class TestExportFoldersAvailability:

    def test_export_sources_folder_availability_local_methods(self):
        conanfile = textwrap.dedent('\n        from conan import ConanFile\n\n        class ConanLib(ConanFile):\n\n            def layout(self):\n                self.folders.source = "MY_SOURCE"\n\n            def generate(self):\n                self.output.info("Running generate, value {}!".format(self.export_sources_folder))\n\n            def export(self):\n                self.output.info("Running export, value {}!".format(self.export_sources_folder))\n\n            def export_sources(self):\n                self.output.info("Running export_sources, value {}!".format(self.export_sources_folder))\n\n            def source(self):\n                self.output.info("Running source, value {}!".format(self.export_sources_folder))\n\n            def build(self):\n                self.output.info("Running build, value {}!".format(self.export_sources_folder))\n\n            def package(self):\n                self.output.info("Running package, value {}!".format(self.export_sources_folder))\n\n        ')
        client = TestClient()
        client.save({'conanfile.py': conanfile})
        client.run('export . foo/1.0@')
        cache_exports_sources = client.cache.package_layout(ConanFileReference.loads('foo/1.0')).export_sources()
        assert 'Running export, value None!' in client.out
        assert 'Running export_sources, value {}!'.format(cache_exports_sources) in client.out
        client.run('install .')
        assert 'Running generate, value {}!'.format(client.current_folder) in client.out
        client.run('source .')
        assert 'Running source, value {}!'.format(client.current_folder) in client.out
        client.run('build .')
        assert 'Running build, value {}!'.format(client.current_folder) in client.out

    def test_export_folder_availability_local_methods(self):
        conanfile = textwrap.dedent('\n        from conan import ConanFile\n\n        class ConanLib(ConanFile):\n\n            def layout(self):\n                self.folders.source = "MY_SOURCE"\n\n            def generate(self):\n                self.output.info("Running generate, value {}!".format(self.export_folder))\n\n            def export(self):\n                self.output.info("Running export, value {}!".format(self.export_folder))\n\n            def export_sources(self):\n                self.output.info("Running export_sources, value {}!".format(self.export_folder))\n\n            def source(self):\n                self.output.info("Running source, value {}!".format(self.export_folder))\n\n            def build(self):\n                self.output.info("Running build, value {}!".format(self.export_folder))\n\n            def package(self):\n                self.output.info("Running package, value {}!".format(self.export_folder))\n\n        ')
        client = TestClient()
        client.save({'conanfile.py': conanfile})
        client.run('export . foo/1.0@')
        cache_exports = client.cache.package_layout(ConanFileReference.loads('foo/1.0')).export()
        assert 'Running export_sources, value None!' in client.out
        assert 'Running export, value {}!'.format(cache_exports) in client.out
        client.run('install .')
        assert 'Running generate, value None!' in client.out
        client.run('source .')
        assert 'Running source, value None!' in client.out
        client.run('build .')
        assert 'Running build, value None!' in client.out

    def test_export_folder_availability_create(self):
        conanfile = textwrap.dedent('\n        from conan import ConanFile\n\n        class ConanLib(ConanFile):\n\n            def layout(self):\n                self.folders.source = "MY_SOURCE"\n\n            def generate(self):\n                self.output.info("Running generate, value {}!".format(self.export_folder))\n\n            def export(self):\n                self.output.info("Running export, value {}!".format(self.export_folder))\n\n            def export_sources(self):\n                self.output.info("Running export_sources, value {}!".format(self.export_folder))\n\n            def source(self):\n                self.output.info("Running source, value {}!".format(self.export_folder))\n\n            def build(self):\n                self.output.info("Running build, value {}!".format(self.export_folder))\n\n            def package(self):\n                self.output.info("Running package, value {}!".format(self.export_folder))\n\n        ')
        client = TestClient()
        client.save({'conanfile.py': conanfile})
        cache_exports = client.cache.package_layout(ConanFileReference.loads('foo/1.0')).export()
        client.run('create . foo/1.0@')
        assert 'Running export_sources, value None!' in client.out
        assert 'Running export, value {}!'.format(cache_exports) in client.out
        assert 'Running generate, value None!' in client.out
        assert 'Running source, value None!' in client.out
        assert 'Running build, value None!' in client.out

    def test_export_sources_folder_availability_create(self):
        conanfile = textwrap.dedent('\n        from conan import ConanFile\n\n        class ConanLib(ConanFile):\n\n            def layout(self):\n                self.folders.source = "MY_SOURCE"\n\n            def generate(self):\n                self.output.info("Running generate, value {}!".format(self.export_sources_folder))\n\n            def export(self):\n                self.output.info("Running export, value {}!".format(self.export_sources_folder))\n\n            def export_sources(self):\n                self.output.info("Running export_sources, value {}!".format(self.export_sources_folder))\n\n            def source(self):\n                self.output.info("Running source, value {}!".format(self.export_sources_folder))\n\n            def build(self):\n                self.output.info("Running build, value {}!".format(self.export_sources_folder))\n\n            def package(self):\n                self.output.info("Running package, value {}!".format(self.export_sources_folder))\n\n        ')
        client = TestClient()
        client.save({'conanfile.py': conanfile})
        cache_exports = client.cache.package_layout(ConanFileReference.loads('foo/1.0')).export_sources()
        client.run('create . foo/1.0@')
        assert 'Running export, value None!' in client.out
        assert 'Running export_sources, value {}!'.format(cache_exports) in client.out
        cache_base_source = client.cache.package_layout(ConanFileReference.loads('foo/1.0')).source()
        assert 'Running generate, value {}!'.format(cache_base_source) in client.out
        assert 'Running source, value {}!'.format(cache_base_source) in client.out
        assert 'Running build, value {}!'.format(cache_base_source) in client.out