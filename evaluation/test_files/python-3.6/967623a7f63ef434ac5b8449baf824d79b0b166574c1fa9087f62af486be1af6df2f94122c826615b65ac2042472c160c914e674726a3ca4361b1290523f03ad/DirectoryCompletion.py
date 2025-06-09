import readline
readline.set_completer_delims(' \t\n`~!@#$%^&*()=+[{]}\\|;:\'",<>/?')
import os.path

class DirectoryCompletion(object):

    def __init__(self, fs):
        self.fs = fs

    def parse_text_line(self, text, line, cwd):
        """Here, the text and line is from the
        complete_xxx(self, text, line, begidx, endidx).

        text is the word. line is the whole sentence.

        such as

        /home/ihep/work/initrd.lz[]

        [] indicates the CURSOR.

        so, initrd.lz is the text,
        and ``/home/ihep/work/initrd.lz`` is the line.
        """
        result = []
        path = self.generate_absolute(line, cwd)
        dirname = self.get_dirname(path)
        filename = self.get_filename(path, dirname)
        result = list(self.fs.list_dir(dirname))
        text = filename
        result = [i for i in result if i.startswith(text)]
        return result

    def check_absolute(self, path):
        if path.startswith(self.fs.seq):
            return True
        else:
            return False

    def generate_absolute(self, path, cwd):
        if self.check_absolute(path):
            pass
        else:
            path = os.path.join(cwd, path)
        return path

    def get_dirname(self, path):
        if self.check_absolute(path):
            if path.endswith(self.fs.seq):
                path = os.path.normpath(path) + self.fs.seq
            else:
                path = os.path.normpath(os.path.dirname(path)) + self.fs.seq
        path = path.replace('//', '/')
        return path

    def get_filename(self, path, dirname):
        if self.check_absolute(path):
            if path.endswith(self.fs.seq):
                path = ''
            else:
                path = os.path.normpath(os.path.basename(path))
        path = path.replace('//', '/')
        return path
if __name__ == '__main__':
    from DIRAC.DataManagementSystem.Client.CmdDirCompletion.AbstractFileSystem import UnixLikeFileSystem
    ulfs = UnixLikeFileSystem()
    dc = DirectoryCompletion(ulfs)
    print(dc.parse_text_line('ls', '/bin/', '/home/ihep'))
    print(dc.parse_text_line('.vim', '', '/home/ihep'))
    print(dc.parse_text_line('', '', '/home/ihep'))