def make_local_static_report_files(self):
    """Make local instances of static files for HTML report."""
    for (static, pkgdir) in self.STATIC_FILES:
        shutil.copyfile(data_filename(static, pkgdir), os.path.join(self.directory, static))
    if self.extra_css:
        shutil.copyfile(self.config.extra_css, os.path.join(self.directory, self.extra_css))