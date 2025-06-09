import os
import string, random, sys, re
import unicodedata
from knowsmore.util.color import Color

class Tools:

    def __init__(self):
        pass

    @staticmethod
    def random_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join((random.choice(chars) for x in range(size)))

    @staticmethod
    def clear_line():
        sys.stderr.write('\x1b[K')
        sys.stdout.write('\x1b[K')
        try:
            size = os.get_terminal_size(fd=os.STDOUT_FILENO)
        except:
            size = 50
        print(' ' * size, end='\r', flush=True)
        print(' ' * size, file=sys.stderr, end='\r', flush=True)

    @staticmethod
    def permited_char(s):
        if s.isalpha():
            return True
        elif bool(re.match('^[A-Za-z0-9:]*$', s)):
            return True
        elif s == '.':
            return True
        else:
            return False

    @staticmethod
    def mandatory():
        Color.pl('{!} {R}error: missing a mandatory option, use -h help{W}\r\n')
        Tools.exit_gracefully(1)

    @staticmethod
    def exit_gracefully(code=0):
        exit(code)

    @staticmethod
    def count_file_lines(filename: str):

        def _count_generator(reader):
            b = reader(1024 * 1024)
            while b:
                yield b
                b = reader(1024 * 1024)
        with open(filename, 'rb') as fp:
            c_generator = _count_generator(fp.raw.read)
            count = sum((buffer.count(b'\n') for buffer in c_generator))
            return count + 1

    @staticmethod
    def clear_string(text):
        return ''.join(filter(Tools.permited_char, Tools.strip_accents(text))).strip().lower()

    @staticmethod
    def strip_accents(text):
        try:
            text = unicode(text, 'utf-8')
        except NameError:
            pass
        text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('utf-8')
        return str(text).strip()