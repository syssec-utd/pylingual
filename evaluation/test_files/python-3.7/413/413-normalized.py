def download_file(self, local_path, remote_path, nthreads=64, overwrite=True, buffersize=4194304, blocksize=4194304):
    """
        Download a file from Azure Blob Storage.

        :param local_path: local path. If downloading a single file, will write to this
            specific file, unless it is an existing directory, in which case a file is
            created within it. If downloading multiple files, this is the root
            directory to write within. Will create directories as required.
        :type local_path: str
        :param remote_path: remote path/globstring to use to find remote files.
            Recursive glob patterns using `**` are not supported.
        :type remote_path: str
        :param nthreads: Number of threads to use. If None, uses the number of cores.
        :type nthreads: int
        :param overwrite: Whether to forcibly overwrite existing files/directories.
            If False and remote path is a directory, will quit regardless if any files
            would be overwritten or not. If True, only matching filenames are actually
            overwritten.
        :type overwrite: bool
        :param buffersize: int [2**22]
            Number of bytes for internal buffer. This block cannot be bigger than
            a chunk and cannot be smaller than a block.
        :type buffersize: int
        :param blocksize: int [2**22]
            Number of bytes for a block. Within each chunk, we write a smaller
            block for each API call. This block cannot be bigger than a chunk.
        :type blocksize: int
        """
    multithread.ADLDownloader(self.connection, lpath=local_path, rpath=remote_path, nthreads=nthreads, overwrite=overwrite, buffersize=buffersize, blocksize=blocksize)