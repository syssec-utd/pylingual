def _get_data_files(self):
    """Generate list of '(package,src_dir,build_dir,filenames)' tuples"""
    self.analyze_manifest()
    data = []
    for package in self.packages or ():
        src_dir = self.get_package_dir(package)
        build_dir = os.path.join(*[self.build_lib] + package.split('.'))
        plen = len(src_dir) + 1
        filenames = [file[plen:] for file in self.find_data_files(package, src_dir)]
        data.append((package, src_dir, build_dir, filenames))
    return data