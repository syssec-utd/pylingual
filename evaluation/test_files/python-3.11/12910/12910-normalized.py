def get_header(self, patch_dir=None):
    """ Returns bytes """
    lines = []
    if patch_dir:
        file = patch_dir + File(self.get_name())
        name = file.get_name()
    else:
        name = self.get_name()
    with open(name, 'rb') as f:
        for line in f:
            if line.startswith(b'---') or line.startswith(b'Index:'):
                break
            lines.append(line)
    return b''.join(lines)