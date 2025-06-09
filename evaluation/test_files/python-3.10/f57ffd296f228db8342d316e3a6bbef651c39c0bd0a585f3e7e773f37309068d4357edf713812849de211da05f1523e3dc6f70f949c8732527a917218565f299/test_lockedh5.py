from nose.tools import assert_raises
from horton_grid import *
from ..common import tmpdir

def test_locked1():
    with tmpdir('horton.scripts.test.test_common.test_locked1') as dn:
        with LockedH5File('%s/foo.h5' % dn, 'w'):
            pass

def test_locked2():
    with assert_raises(IOError):
        with tmpdir('horton.scripts.test.test_common.test_locked2') as dn:
            with LockedH5File('%s/foo.h5' % dn, mode='r', wait=0.1, count=3):
                pass

def test_locked3():
    with assert_raises(ValueError):
        with LockedH5File('horton.scripts.test.test_common.test_locked3.h5', driver='fubar', wait=0.1, count=3):
            pass

def test_locked4():
    with assert_raises(ValueError):
        with tmpdir('horton.scripts.test.test_common.test_locked4') as dn:
            with LockedH5File('%s/foo.h5' % dn, 'w', driver='core'):
                pass

def test_locked5():
    with assert_raises(RuntimeError):
        with tmpdir('horton.scripts.test.test_common.test_locked5') as dn:
            with LockedH5File('%s/foo.h5' % dn, 'w'):
                raise RuntimeError