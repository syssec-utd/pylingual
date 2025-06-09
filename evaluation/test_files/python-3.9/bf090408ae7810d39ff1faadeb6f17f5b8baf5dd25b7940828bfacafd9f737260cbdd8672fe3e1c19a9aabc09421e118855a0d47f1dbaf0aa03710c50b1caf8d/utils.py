import itertools
import os
from rcounting.units import HOUR, MINUTE

def flatten(mylist):
    return [element for sublist in mylist for element in sublist]

def partition(mylist, indices):
    return [mylist[i:j] for (i, j) in zip([0] + indices, indices + [None])]

def is_leap_year(n):
    return n % 4 == 0 and (n % 400 == 0 or n % 100 != 0)

def format_timedelta(timedelta):

    def format_one_interval(n, unit):
        if n == 0:
            return ''
        return f"{n} {unit}{('s' if n > 1 else '')}"
    days = timedelta.days
    (hours, rem) = divmod(timedelta.seconds, HOUR)
    (minutes, seconds) = divmod(rem, MINUTE)
    amounts = [days, hours, minutes, seconds]
    units = ['day', 'hour', 'minute', 'second']
    formatted = [format_one_interval(n, unit) for (n, unit) in zip(amounts, units)]
    return ', '.join([x for x in formatted if x])

def ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
deleted_phrases = ['[deleted]', '[removed]', '[banned]']

def chunked(iterable, n):
    it = iter(iterable)
    while True:
        chunk_it = itertools.islice(it, n)
        try:
            first_el = next(chunk_it)
        except StopIteration:
            return
        yield itertools.chain((first_el,), chunk_it)