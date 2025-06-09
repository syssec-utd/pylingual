"""Functions for parallel computation on multiple cores.

Introduced in Python-RSA 3.1.

.. note::

    Requires Python 2.6 or newer.

"""
import multiprocessing as mp
from multiprocessing.connection import Connection
import rsa.prime
import rsa.randnum

def _find_prime(nbits: int, pipe: Connection) -> None:
    while True:
        integer = rsa.randnum.read_random_odd_int(nbits)
        if rsa.prime.is_prime(integer):
            pipe.send(integer)
            return

def getprime(nbits: int, poolsize: int) -> int:
    """Returns a prime number that can be stored in 'nbits' bits.

    Works in multiple threads at the same time.

    >>> p = getprime(128, 3)
    >>> rsa.prime.is_prime(p-1)
    False
    >>> rsa.prime.is_prime(p)
    True
    >>> rsa.prime.is_prime(p+1)
    False

    >>> from rsa import common
    >>> common.bit_size(p) == 128
    True

    """
    pipe_recv, pipe_send = mp.Pipe(duplex=False)
    try:
        procs = [mp.Process(target=_find_prime, args=(nbits, pipe_send)) for _ in range(poolsize)]
        for p in procs:
            p.start()
        result = pipe_recv.recv()
    finally:
        pipe_recv.close()
        pipe_send.close()
    for p in procs:
        p.terminate()
    return result
__all__ = ['getprime']
if __name__ == '__main__':
    print('Running doctests 1000x or until failure')
    import doctest
    for count in range(100):
        failures, tests = doctest.testmod()
        if failures:
            break
        if count % 10 == 0 and count:
            print('%i times' % count)
    print('Doctests done')