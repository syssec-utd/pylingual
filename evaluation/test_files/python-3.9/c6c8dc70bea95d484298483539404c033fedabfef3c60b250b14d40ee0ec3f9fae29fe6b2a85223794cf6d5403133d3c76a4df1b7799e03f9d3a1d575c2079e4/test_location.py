"""Tests for breezy.location."""
from .. import osutils, tests, urlutils
from ..directory_service import directories
from ..location import hooks as location_hooks, location_to_url, rcp_location_to_url

class SomeDirectory(object):

    def look_up(self, name, url, purpose=None):
        return 'http://bar'

class TestLocationToUrl(tests.TestCase):

    def get_base_location(self):
        path = osutils.abspath('/foo/bar')
        if path.startswith('/'):
            url = 'file://%s' % (path,)
        else:
            url = 'file:///%s' % (path,)
        return (path, url)

    def test_regular_url(self):
        self.assertEqual('file://foo', location_to_url('file://foo'))

    def test_directory(self):
        directories.register('bar:', SomeDirectory, 'Dummy directory')
        self.addCleanup(directories.remove, 'bar:')
        self.assertEqual('http://bar', location_to_url('bar:'))

    def test_unicode_url(self):
        self.assertRaises(urlutils.InvalidURL, location_to_url, b'http://fo/\xc3\xaf'.decode('utf-8'))

    def test_unicode_path(self):
        (path, url) = self.get_base_location()
        location = path + b'\xc3\xaf'.decode('utf-8')
        url += '%C3%AF'
        self.assertEqual(url, location_to_url(location))

    def test_path(self):
        (path, url) = self.get_base_location()
        self.assertEqual(url, location_to_url(path))

    def test_relative_file_url(self):
        self.assertEqual(urlutils.local_path_to_url('.') + '/bar', location_to_url('file:bar'))

    def test_absolute_file_url(self):
        self.assertEqual('file:///bar', location_to_url('file:/bar'))

    def test_pserver(self):
        self.assertEqual('cvs+pserver://anonymous@odessa.cvs.sourceforge.net/cvsroot/odess', location_to_url(':pserver:anonymous@odessa.cvs.sourceforge.net:/cvsroot/odess'))
        self.assertRaises(urlutils.InvalidURL, location_to_url, ':pserver:blah')
        self.assertRaises(urlutils.InvalidURL, location_to_url, ':pserver:blah:bloe')

    def test_extssh(self):
        self.assertEqual('cvs+ssh://anonymous@odessa.cvs.sourceforge.net/cvsroot/odess', location_to_url(':extssh:anonymous@odessa.cvs.sourceforge.net:/cvsroot/odess'))

    def test_missing_scheme(self):
        self.skipTest('need clever guessing of scheme')
        self.assertEqual('cvs+pserver://anonymous@savi.cvs.sourceforge.net:/cvsroot/savi', location_to_url('anonymous@savi.cvs.sourceforge.net:/cvsroot/savi'))

    def test_rcp_url(self):
        self.assertEqual('ssh://example.com/srv/git/bar', location_to_url('example.com:/srv/git/bar'))

    def test_rewrite_hook(self):
        self.assertEqual('http://foo.example.com/blah', location_to_url('http://foo.example.com/blah'))

        def rewrite_url(url, purpose=None):
            return url.replace('foo', 'bar')
        self.addCleanup(location_hooks.uninstall_named_hook, 'rewrite_url', 'test')
        location_hooks.install_named_hook('rewrite_url', rewrite_url, 'test')
        self.assertEqual('http://bar.example.com/bar', location_to_url('http://foo.example.com/foo'))

class RCPLocationTests(tests.TestCase):

    def test_without_user(self):
        self.assertEqual('git+ssh://example.com/srv/git/bar', rcp_location_to_url('example.com:/srv/git/bar', scheme='git+ssh'))
        self.assertEqual('ssh://example.com/srv/git/bar', rcp_location_to_url('example.com:/srv/git/bar'))

    def test_with_user(self):
        self.assertEqual('git+ssh://foo@example.com/srv/git/bar', rcp_location_to_url('foo@example.com:/srv/git/bar', scheme='git+ssh'))

    def test_invalid(self):
        self.assertRaises(ValueError, rcp_location_to_url, 'http://srv/git/bar')
        self.assertRaises(ValueError, rcp_location_to_url, 'git/bar')
        self.assertRaises(ValueError, rcp_location_to_url, 'c:/git/bar')