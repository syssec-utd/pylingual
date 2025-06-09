"""
`password` type question
"""
from . import input

def question(message, **kwargs):
    kwargs['is_password'] = True
    return input.question(message, **kwargs)