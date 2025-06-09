def equal(self, cwd):
    """ Returns True if left and right are equal
        """
    cmd = ['diff']
    cmd.append('-q')
    cmd.append(self.left.get_name())
    cmd.append(self.right.get_name())
    try:
        Process(cmd).run(cwd=cwd, suppress_output=True)
    except SubprocessError as e:
        if e.get_returncode() == 1:
            return False
        else:
            raise e
    return True