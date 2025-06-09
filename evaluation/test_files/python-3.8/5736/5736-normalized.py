def _check_exception_inherit_from_stopiteration(exc):
    """Return True if the exception node in argument inherit from StopIteration"""
    stopiteration_qname = '{}.StopIteration'.format(utils.EXCEPTIONS_MODULE)
    return any((_class.qname() == stopiteration_qname for _class in exc.mro()))