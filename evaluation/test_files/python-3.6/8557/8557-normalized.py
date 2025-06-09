def get_filtered_sized_root_folder(self):
    """Return the location where filtered + sized images are stored."""
    sized_root_folder = self.get_sized_root_folder()
    return os.path.join(sized_root_folder, VERSATILEIMAGEFIELD_FILTERED_DIRNAME)