import os, os.path, subprocess, shutil
try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen
python_versions = ['2.6.8', '2.7.5', '3.1.5', '3.2.5', '3.3.5', '3.4.1']
libcurl_versions = ['7.19.0', '7.46.0']
libcurl_meta = {'7.19.0': {'patches': ['curl-7.19.0-sslv2-c66b0b32fba-modified.patch']}}
root = os.path.abspath(os.path.dirname(__file__))

class in_dir:

    def __init__(self, dir):
        self.dir = dir

    def __enter__(self):
        self.oldwd = os.getcwd()
        os.chdir(self.dir)

    def __exit__(self, type, value, traceback):
        os.chdir(self.oldwd)

def subprocess_check_call(cmd, **kwargs):
    try:
        subprocess.check_call(cmd, **kwargs)
    except OSError as exc:
        message = exc.args[0]
        message = '%s while trying to execute %s' % (message, str(cmd))
        args = tuple([message] + exc.args[1:])
        raise type(exc)(args)

def fetch(url, archive=None):
    if archive is None:
        archive = os.path.basename(url)
    if not os.path.exists(archive):
        sys.stdout.write('Fetching %s\n' % url)
        io = urlopen(url)
        with open('.tmp.%s' % archive, 'wb') as f:
            while True:
                chunk = io.read(65536)
                if len(chunk) == 0:
                    break
                f.write(chunk)
        os.rename('.tmp.%s' % archive, archive)

def build(archive, dir, prefix, meta=None):
    if not os.path.exists(dir):
        sys.stdout.write('Building %s\n' % archive)
        subprocess_check_call(['tar', 'xf', archive])
        with in_dir(dir):
            if meta and 'patches' in meta:
                for patch in meta['patches']:
                    patch_path = os.path.join(root, 'matrix', patch)
                    subprocess_check_call(['patch', '-p1', '-i', patch_path])
            subprocess_check_call(['./configure', '--prefix=%s' % prefix])
            if 'post-configure' in meta:
                for cmd in meta['post-configure']:
                    subprocess_check_call(cmd, shell=True)
            subprocess_check_call(['make'])
            subprocess_check_call(['make', 'install'])

def run_matrix(python_versions, libcurl_versions):
    for python_version in python_versions:
        url = 'http://www.python.org/ftp/python/%s/Python-%s.tgz' % (python_version, python_version)
        archive = os.path.basename(url)
        fetch(url, archive)
        dir = archive.replace('.tgz', '')
        prefix = os.path.abspath('i/%s' % dir)
        build(archive, dir, prefix)
    for libcurl_version in libcurl_versions:
        url = 'https://curl.haxx.se/download/curl-%s.tar.gz' % libcurl_version
        archive = os.path.basename(url)
        fetch(url, archive)
        dir = archive.replace('.tar.gz', '')
        prefix = os.path.abspath('i/%s' % dir)
        build(archive, dir, prefix, meta=libcurl_meta.get(libcurl_version))
    fetch('https://raw.github.com/pypa/virtualenv/1.7/virtualenv.py', 'virtualenv-1.7.py')
    fetch('https://raw.github.com/pypa/virtualenv/1.9.1/virtualenv.py', 'virtualenv-1.9.1.py')
    if not os.path.exists('venv'):
        os.mkdir('venv')
    for python_version in python_versions:
        python_version_pieces = [int(piece) for piece in python_version.split('.')[:2]]
        for libcurl_version in libcurl_versions:
            python_prefix = os.path.abspath('i/Python-%s' % python_version)
            libcurl_prefix = os.path.abspath('i/curl-%s' % libcurl_version)
            venv = os.path.abspath('venv/Python-%s-curl-%s' % (python_version, libcurl_version))
            if os.path.exists(venv):
                shutil.rmtree(venv)
            fetch('https://pypi.python.org/packages/2.6/s/setuptools/setuptools-0.6c11-py2.6.egg')
            fetch('https://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11-py2.7.egg')
            fetch('https://pypi.python.org/packages/source/d/distribute/distribute-0.6.49.tar.gz')
            subprocess_check_call(['python', 'virtualenv-1.9.1.py', venv, '-p', '%s/bin/python%d.%d' % (python_prefix, python_version_pieces[0], python_version_pieces[1]), '--no-site-packages', '--never-download'])
            curl_config_path = os.path.join(libcurl_prefix, 'bin/curl-config')
            curl_lib_path = os.path.join(libcurl_prefix, 'lib')
            with in_dir('pycurl'):
                extra_patches = []
                extra_env = []
                deps_cmd = 'pip install -r requirements-dev.txt'
                extra_patches = ' && '.join(extra_patches)
                extra_env = ' '.join(extra_env)
                cmd = '\n                    make clean &&\n                    . %(venv)s/bin/activate &&\n                    %(deps_cmd)s && %(extra_patches)s\n                    python -V &&\n                    LD_LIBRARY_PATH=%(curl_lib_path)s PYCURL_CURL_CONFIG=%(curl_config_path)s %(extra_env)s make test\n                ' % dict(venv=venv, deps_cmd=deps_cmd, extra_patches=extra_patches, curl_lib_path=curl_lib_path, curl_config_path=curl_config_path, extra_env=extra_env)
                print(cmd)
                subprocess_check_call(cmd, shell=True)
if __name__ == '__main__':
    import sys

    def main():
        import optparse
        parser = optparse.OptionParser()
        parser.add_option('-p', '--python', help='Specify python version to test against')
        parser.add_option('-c', '--curl', help='Specify libcurl version to test against')
        options, args = parser.parse_args()
        if options.python:
            python_version = options.python
            if python_version in python_versions:
                chosen_python_versions = [python_version]
            else:
                chosen_python_versions = [v for v in python_versions if v.startswith(python_version)]
                if len(chosen_python_versions) != 1:
                    raise Exception('Bogus python version requested: %s' % python_version)
        else:
            chosen_python_versions = python_versions
        if options.curl:
            chosen_libcurl_versions = [options.curl]
        else:
            chosen_libcurl_versions = libcurl_versions
        run_matrix(chosen_python_versions, chosen_libcurl_versions)
    main()