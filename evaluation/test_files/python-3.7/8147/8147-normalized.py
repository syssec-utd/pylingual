def get_extension(self):
    """Returns the file extension."""
    ext = os.path.splitext(self.img.name)[1]
    if ext:
        return ext[1:]
    return ext