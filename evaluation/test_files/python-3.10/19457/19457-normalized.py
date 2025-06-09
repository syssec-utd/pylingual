def find_file(path):
    """
	Given a path to a part in a zip file, return a path to the file and
	the path to the part.

	Assuming /foo.zipx exists as a file,

	>>> find_file('/foo.zipx/dir/part') # doctest: +SKIP
	('/foo.zipx', '/dir/part')

	>>> find_file('/foo.zipx') # doctest: +SKIP
	('/foo.zipx', '')
	"""
    path_components = split_all(path)

    def get_assemblies():
        """
		Enumerate the various combinations of file paths and part paths
		"""
        for n in range(len(path_components), 0, -1):
            file_c = path_components[:n]
            part_c = path_components[n:] or ['']
            yield (os.path.join(*file_c), posixpath.join(*part_c))
    for (file_path, part_path) in get_assemblies():
        if os.path.isfile(file_path):
            return (file_path, part_path)