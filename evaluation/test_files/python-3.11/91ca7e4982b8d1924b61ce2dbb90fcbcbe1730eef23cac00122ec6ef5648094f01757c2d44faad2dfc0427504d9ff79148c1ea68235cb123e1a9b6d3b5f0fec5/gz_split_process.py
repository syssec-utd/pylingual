from allz.libs.abstract_decompress import AbstractDecompress
from allz.libs import common

class GzSplitProcess(AbstractDecompress):

    def __init__(self):
        super().__init__()

    def split_decompress(self, split_files, dest_path, is_force_mode=False):
        cmd = ''
        if len(split_files) > 0:
            src_path = '.'.join(str(split_files[0]).split('.')[:-1]) + '*'
            is_split, prefix_path = common.get_split_volumn_suffix(split_files[0])
            if is_split:
                src_path = f'{prefix_path}*'
            if is_force_mode:
                cmd = f'cat {src_path} | tar zx -C {dest_path} --overwrite'
            else:
                cmd = f'cat {src_path} | tar zx -C {dest_path} --skip-old-files'
        return cmd or None

    def handle(self, src_path, dest_path, is_force_mode=False):
        pass

    def decompress_test(self):
        pass