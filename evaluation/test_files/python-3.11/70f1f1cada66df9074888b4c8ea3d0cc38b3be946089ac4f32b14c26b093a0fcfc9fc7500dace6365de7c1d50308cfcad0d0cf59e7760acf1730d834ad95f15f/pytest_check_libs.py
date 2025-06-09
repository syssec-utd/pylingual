import pytest
import os
import subprocess
import time

def pytest_addoption(parser):
    parser.addoption('--lib', action='store', default='off', help='check your missing library')

def pytest_sessionstart(session):
    path = session.config.getoption('--lib')
    os.chdir(path)
    file_name = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_name.append(file)
    if 'requirements.txt' in file_name:
        libs = os.popen('pip list').read()
        with open('libs_backup.txt', 'w') as f:
            f.write(libs)
        with open('libs_backup.txt', 'r') as f:
            lines = f.readlines()
            for i in lines:
                line = i.strip().split(' ')
                if line[0] == 'Package':
                    pass
                elif '---' in line[0]:
                    pass
                else:
                    with open('doc.txt', 'a') as f:
                        f.write(f'{line[0]}=={line[len(line) - 1]}\n')
        os.remove('libs_backup.txt')
        lib_list = []
        try:
            with open('requirements.txt', 'r') as fr:
                with open('libs_backup.txt', 'r') as fd:
                    requirments = fr.readlines()
                    doc = fd.read()
                    for fr_line in requirments:
                        if fr_line not in doc:
                            lib_list.append(fr_line)
            time.sleep(3)
            if lib_list != 0:
                print('The following versions are found missing')
                print(lib_list)
                for lib in lib_list:
                    print(f'Installing {lib}, please wait')
                    cmd = f'pip install -i http://pypi.douban.com/simple/ {lib}'
                    output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                    for line in output.stdout:
                        print(line)
            else:
                print('No difference in current version')
        finally:
            os.remove('doc.txt')
    else:
        raise 'Not found requirements.txt'