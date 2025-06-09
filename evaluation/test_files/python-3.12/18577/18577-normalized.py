def to_png_file(self, fname: str):
    """
        write a '.png' file.
        """
    cmd = pipes.Template()
    cmd.append('dot -Tpng > %s' % fname, '-.')
    with cmd.open('pipefile', 'w') as f:
        f.write(self.to_dot())