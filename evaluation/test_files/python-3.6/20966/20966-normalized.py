def transplant_class(cls, module):
    """
    Make a class appear to reside in `module`, rather than the module in which
    it is actually defined.

    >>> from nose.failure import Failure
    >>> Failure.__module__
    'nose.failure'
    >>> Nf = transplant_class(Failure, __name__)
    >>> Nf.__module__
    'nose.util'
    >>> Nf.__name__
    'Failure'

    """

    class C(cls):
        pass
    C.__module__ = module
    C.__name__ = cls.__name__
    return C