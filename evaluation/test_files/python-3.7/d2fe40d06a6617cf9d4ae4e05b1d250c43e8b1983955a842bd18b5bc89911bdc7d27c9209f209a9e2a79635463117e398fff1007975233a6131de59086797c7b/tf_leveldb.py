"""For reading and writing TFTables files."""
import os
import typing
from tfrecords.python.util import compat
from tfrecords.lib import tfrecords_cc as _pywrap_db_io
__all__ = ['LeveldbCompressionType', 'LeveldbOptions', 'LeveldbIterater', 'Leveldb']

class LeveldbCompressionType(object):
    """The type of compression for the table."""
    NONE = 0
    SNAPPY = 1

class LeveldbOptions(object):
    """Options used for manipulating TFTable files."""
    compression_type_map = {'': LeveldbCompressionType.NONE, 'SNAPPY': LeveldbCompressionType.SNAPPY}

    def __init__(self, compression_type='SNAPPY', create_if_missing=True, error_if_exists=True, paranoid_checks=False, write_buffer_size=4 * 1024 * 1024, max_open_files=1000, block_size=4 * 1024, block_restart_interval=16, max_file_size=1 * 1024 * 1024 * 1024, reuse_logs=False):
        """Creates a `TFTableOptions` instance.

    Options only effect TFTableWriter when compression_type is not `None`.
    Documentation, details, and defaults can be found in
    [`zlib_compression_options.h`](https://www.tensorflow.org/code/tensorflow/core/lib/io/zlib_compression_options.h)
    and in the [zlib manual](http://www.zlib.net/manual.html).
    Leaving an option as `None` allows C++ to set a reasonable default.

    Args:
      compression_type: `"SNAPPY"`, or `""` (no compression).
      create_if_missing: int or `None`.
      error_if_exists: int or `None`.
      paranoid_checks: int or `None`.
      write_buffer_size: int or `None`.

      max_open_files: int or `None`.
      block_size: int or `None`.
      block_restart_interval: int or `None`.
      max_file_size: int or `None`.
      reuse_logs: int or `None`.

    Returns:
      A `TFTableOptions` object.

    Raises:
      ValueError: If compression_type is invalid.
    """
        self.compression_type = compression_type
        if isinstance(self.compression_type, str):
            if self.compression_type is None:
                self.compression_type = 'SNAPPY'
            if self.compression_type not in LeveldbOptions.compression_type_map:
                raise ValueError('Not a valid compression_type: "{}"'.format(LeveldbOptions.compression_type_map.keys()))
        self.options = _pywrap_db_io.LeveldbOptions()
        if create_if_missing is not None:
            self.options.create_if_missing = create_if_missing
        if error_if_exists is not None:
            self.options.error_if_exists = error_if_exists
        if paranoid_checks is not None:
            self.options.paranoid_checks = paranoid_checks
        if write_buffer_size is not None:
            self.options.write_buffer_size = write_buffer_size
        if max_open_files is not None:
            self.options.max_open_files = max_open_files
        if block_size is not None:
            self.options.block_size = block_size
        if block_restart_interval is not None:
            self.options.block_restart_interval = block_restart_interval
        if max_file_size is not None:
            self.options.max_file_size = max_file_size
        if reuse_logs is not None:
            self.options.reuse_logs = reuse_logs

    def __reduce_ex__(self, *args, **kwargs):
        return (self.__class__, (self.compression_type, self.options.create_if_missing, self.options.paranoid_checks, self.options.write_buffer_size, self.options.max_open_files, self.options.block_size, self.options.block_restart_interval, self.options.max_file_size, self.options.reuse_logs))

    def as_options(self):
        return self.options

class LeveldbIterater(_pywrap_db_io.LeveldbIterater):

    def __init__(self, *args, **kwargs):
        super(LeveldbIterater, self).__init__(*args, **kwargs)

    def __del__(self):
        self.close()
        super(LeveldbIterater, self).__del__()

    def __iter__(self):
        raise NotImplementedError

    def __next__(self):
        raise NotImplementedError

    def Valid(self):
        return super(LeveldbIterater, self).Valid()

    def current(self):
        return super(LeveldbIterater, self).current()

    def next(self):
        return super(LeveldbIterater, self).next()

    def prev(self):
        return super(LeveldbIterater, self).prev()

    def SeekToFirst(self):
        return super(LeveldbIterater, self).SeekToFirst()

    def SeekToLast(self):
        return super(LeveldbIterater, self).SeekToLast()

    def Seek(self, key):
        return super(LeveldbIterater, self).Seek(key)

    def close(self):
        super(LeveldbIterater, self).close()

class Leveldb(_pywrap_db_io.Leveldb):
    iterator_list = []

    def __init__(self, path: str, options: typing.Union[str, LeveldbOptions]=None):
        """Opens file `path` and creates a `TFTableWriter` writing to it.

    Args:
      path: The path to the TFTables file.
      options: (optional) LeveldbOptions , or string `"SNAPPY"`, or `""` (no compression).

    Raises:
      IOError: If `path` cannot be opened for writing.
      ValueError: If valid compression_type can't be determined from `options`.
    """
        if not isinstance(options, LeveldbOptions):
            options = LeveldbOptions(compression_type=options)
        super(Leveldb, self).__init__(path, options.as_options())
        self.path = path
        self.options = options
        assert self.status() == 0, self.error()

    def __reduce_ex__(self, *args, **kwargs):
        return (self.__class__, (self.path, self.options))

    def __del__(self):
        self.close()

    def get_iterater(self, reverse=False) -> LeveldbIterater:
        it = super(Leveldb, self).get_iterater(reverse)
        self.iterator_list.append(it)
        return it

    def get(self, key: typing.Union[str, bytes], value=None):
        try:
            return super(Leveldb, self).get(key)
        except:
            pass
        return value

    def put_batch(self, keys: typing.List[typing.Union[str, bytes]], values: typing.List[typing.Union[str, bytes]]):
        return super(Leveldb, self).put_batch(keys, values)

    def put(self, key: typing.Union[str, bytes], value: typing.Union[str, bytes]):
        return super(Leveldb, self).put(key, value)

    def remove(self, key: typing.Union[str, bytes]):
        return super(Leveldb, self).remove(key)

    def close(self):
        """Close the file."""
        for it in self.iterator_list:
            if it is not None:
                it.close()
        self.iterator_list.clear()
        super(Leveldb, self).close()

    def error(self) -> str:
        return super(Leveldb, self).error()

    def status(self) -> int:
        return super(Leveldb, self).status()