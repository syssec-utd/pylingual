def check_nsp(dist, attr, value):
    """Verify that namespace packages are valid"""
    assert_string_list(dist, attr, value)
    for nsp in value:
        if not dist.has_contents_for(nsp):
            raise DistutilsSetupError('Distribution contains no modules or packages for ' + 'namespace package %r' % nsp)
        if '.' in nsp:
            parent = '.'.join(nsp.split('.')[:-1])
            if parent not in value:
                distutils.log.warn('%r is declared as a package namespace, but %r is not: please correct this in setup.py', nsp, parent)