import typing as t
import types
import os
import errno
from werkzeug.utils import import_string

class AppConfig(dict):

    def __init__(self, root_path: str, defaults: t.Optional[dict]=None) -> None:
        super().__init__(defaults or {})
        self.root_path = root_path

    def from_pyfile(self, filename: str, silent: bool=False) -> bool:
        """Updates the values in the config from a Python file.  This function
        behaves as if the file was imported as module with the
        :meth:`from_object` function.
        :param filename: the filename of the config.  This can either be an
                         absolute filename or a filename relative to the
                         root path.
        :param silent: set to ``True`` if you want silent failure for missing
                       files.
        :return: ``True`` if the file was loaded successfully.
        .. versionadded:: 0.7
           `silent` parameter.
        """
        filename = os.path.join(self.root_path, filename)
        d = types.ModuleType('config')
        d.__file__ = filename
        try:
            with open(filename, mode='rb') as config_file:
                exec(compile(config_file.read(), filename, 'exec'), d.__dict__)
        except OSError as e:
            if silent and e.errno in (errno.ENOENT, errno.EISDIR, errno.ENOTDIR):
                return False
            e.strerror = f'Unable to load configuration file ({e.strerror})'
            raise
        self.from_object(d)
        return True

    def from_object(self, obj: t.Union[object, str]) -> None:
        """Updates the values from the given object.  An object can be of one
        of the following two types:
        -   a string: in this case the object with that name will be imported
        -   an actual object reference: that object is used directly
        Objects are usually either modules or classes. :meth:`from_object`
        loads only the uppercase attributes of the module/class. A ``dict``
        object will not work with :meth:`from_object` because the keys of a
        ``dict`` are not attributes of the ``dict`` class.
        Example of module-based configuration::
            app.config.from_object('yourapplication.default_config')
            from yourapplication import default_config
            app.config.from_object(default_config)
        Nothing is done to the object before loading. If the object is a
        class and has ``@property`` attributes, it needs to be
        instantiated before being passed to this method.
        You should not use this function to load the actual configuration but
        rather configuration defaults.  The actual config should be loaded
        with :meth:`from_pyfile` and ideally from a location not within the
        package because the package might be installed system wide.
        See :ref:`config-dev-prod` for an example of class-based configuration
        using :meth:`from_object`.
        :param obj: an import name or object
        """
        if isinstance(obj, str):
            obj = import_string(obj)
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)

    def __repr__(self) -> str:
        return f'<{type(self).__name__} {dict.__repr__(self)}>'