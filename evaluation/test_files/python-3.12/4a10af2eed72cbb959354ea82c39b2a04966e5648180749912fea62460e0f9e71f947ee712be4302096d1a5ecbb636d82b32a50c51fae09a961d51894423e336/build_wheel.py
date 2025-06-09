import os
import shutil
import subprocess
import sys
import zipfile
import requests
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LIBNAME = 'adbutils'
BINARIES_DIR = os.path.join(ROOT_DIR, LIBNAME, 'binaries')
FNAMES_PER_PLATFORM = {'darwin': ['adb'], 'linux': ['adb'], 'win32': ['adb.exe', 'AdbWinApi.dll', 'AdbWinUsbApi.dll']}
BINARIES_URL = {'darwin': 'https://dl.google.com/android/repository/platform-tools-latest-darwin.zip', 'linux': 'https://dl.google.com/android/repository/platform-tools-latest-linux.zip', 'win32': 'https://dl.google.com/android/repository/platform-tools-latest-windows.zip'}
linux_plats = 'manylinux_2_24_x86_64.manylinux_2_24_aarch64'
darwin_plats = 'macosx_10_9_intel.macosx_10_9_x86_64.macosx_10_10_intel.macosx_10_10_x86_64'
WHEEL_BUILDS = {'py3-none-' + darwin_plats: 'darwin', 'py3-none-win32': 'win32', 'py3-none-win_amd64': 'win32'}

def copy_binaries(target_dir, platform: str):
    assert os.path.isdir(target_dir)
    base_url = BINARIES_URL[platform]
    archive_name = os.path.join(target_dir, f'{platform}.zip')
    print('Downloading', base_url, '...', end=' ', flush=True)
    with open(archive_name, 'wb') as handle:
        response = requests.get(base_url, stream=True)
        if not response.ok:
            print(response)
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)
    print('done')
    for fname in FNAMES_PER_PLATFORM[platform]:
        print('Extracting', fname, '...', end=' ')
        member_name = f'platform-tools/{fname}'
        extract_archive_file(archive_file=archive_name, file=member_name, destination_folder=target_dir)
        shutil.move(src=os.path.join(target_dir, member_name), dst=os.path.join(target_dir, fname))
        filename = os.path.join(target_dir, fname)
        if fname == 'adb':
            os.chmod(filename, 493)
        print('done')
    os.rmdir(path=os.path.join(target_dir, 'platform-tools'))
    os.remove(path=archive_name)

def extract_archive_file(archive_file, file, destination_folder):
    extension = archive_file.rsplit('.', 1)[-1].lower()
    if extension == 'zip':
        with zipfile.ZipFile(archive_file, 'r') as archive:
            archive.extract(member=file, path=destination_folder)

def clear_binaries_dir(target_dir):
    assert os.path.isdir(target_dir)
    assert os.path.basename(target_dir) == 'binaries'
    for fname in os.listdir(target_dir):
        if fname != 'README.md':
            print('Removing', fname, '...', end=' ')
            os.remove(os.path.join(target_dir, fname))
            print('done')

def clean():
    for root, dirs, files in os.walk(ROOT_DIR):
        for dname in dirs:
            if dname in ('__pycache__', '.cache', 'dist', 'build', LIBNAME + '.egg-info'):
                shutil.rmtree(os.path.join(root, dname))
                print('Removing', dname)
        for fname in files:
            if fname.endswith(('.pyc', '.pyo')):
                os.remove(os.path.join(root, fname))
                print('Removing', fname)

def build():
    clean()
    clear_binaries_dir(BINARIES_DIR)
    print('Using setup.py to generate wheel ...', end='')
    subprocess.check_output([sys.executable, 'setup.py', 'sdist', 'bdist_wheel'], cwd=ROOT_DIR)
    print('done')
    version = None
    distdir = os.path.join(ROOT_DIR, 'dist')
    for fname in os.listdir(distdir):
        if fname.endswith('.whl'):
            version = fname.split('-')[1]
            break
    assert version
    fname = '-'.join([LIBNAME, version, 'py3-none-any.whl'])
    packdir = LIBNAME + '-' + version
    infodir = f'{LIBNAME}-{version}.dist-info'
    wheelfile = os.path.join(distdir, packdir, infodir, 'WHEEL')
    print('Path:', os.path.join(distdir, fname))
    assert os.path.isfile(os.path.join(distdir, fname))
    print('Unpacking ...', end='')
    subprocess.check_output([sys.executable, '-m', 'wheel', 'unpack', fname], cwd=distdir)
    os.remove(os.path.join(distdir, packdir, infodir, 'RECORD'))
    print('done')
    for wheeltag, platform in WHEEL_BUILDS.items():
        print(f'Edit for {platform} {wheeltag}')
        binary_dir = os.path.join(distdir, packdir, LIBNAME, 'binaries')
        clear_binaries_dir(binary_dir)
        copy_binaries(binary_dir, platform)
        lines = []
        for line in open(wheelfile, 'r', encoding='UTF-8'):
            if line.startswith('Tag:'):
                line = 'Tag: ' + wheeltag
            lines.append(line.rstrip())
        with open(wheelfile, 'w', encoding='UTF-8') as f:
            f.write('\n'.join(lines))
        print('Pack ...', end='')
        subprocess.check_output([sys.executable, '-m', 'wheel', 'pack', packdir], cwd=distdir)
        print('done')
    os.remove(os.path.join(distdir, fname))
    shutil.rmtree(os.path.join(distdir, packdir))
    print('Dist folder:')
    for fname in sorted(os.listdir(distdir)):
        s = os.stat(os.path.join(distdir, fname)).st_size
        print('  {:0.0f} KB {}'.format(s / 2 ** 10, fname))

def release():
    """ Release the packages to pypi """
    username = os.environ['PYPI_USERNAME']
    password = os.environ['PYPI_PASSWORD']
    subprocess.check_call([sys.executable, '-m', 'twine', 'upload', '-u', username, '-p', password, 'dist/*'])
if __name__ == '__main__':
    build()