def pseudo_tempname(self):
    """Return a pseudo-tempname base in the install directory.
        This code is intentionally naive; if a malicious party can write to
        the target directory you're already in deep doodoo.
        """
    try:
        pid = os.getpid()
    except:
        pid = random.randint(0, maxsize)
    return os.path.join(self.install_dir, 'test-easy-install-%s' % pid)