def discover_modules(self):
    """ Return module sequence discovered from ``self.package_name`` 


        Parameters
        ----------
        None

        Returns
        -------
        mods : sequence
            Sequence of module names within ``self.package_name``

        Examples
        --------
        >>> dw = ApiDocWriter('sphinx')
        >>> mods = dw.discover_modules()
        >>> 'sphinx.util' in mods
        True
        >>> dw.package_skip_patterns.append('\\.util$')
        >>> 'sphinx.util' in dw.discover_modules()
        False
        >>> 
        """
    modules = [self.package_name]
    for dirpath, dirnames, filenames in os.walk(self.root_path):
        root_uri = self._path2uri(os.path.join(self.root_path, dirpath))
        for dirname in dirnames[:]:
            package_uri = '.'.join((root_uri, dirname))
            if self._uri2path(package_uri) and self._survives_exclude(package_uri, 'package'):
                modules.append(package_uri)
            else:
                dirnames.remove(dirname)
        for filename in filenames:
            module_name = filename[:-3]
            module_uri = '.'.join((root_uri, module_name))
            if self._uri2path(module_uri) and self._survives_exclude(module_uri, 'module'):
                modules.append(module_uri)
    return sorted(modules)