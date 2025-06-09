"""
Module Error
"""
from linux_profile.utils.text import color

class ErrorLoadSettings(Exception):

    def __init__(self):
        message = 'It is not possible to load the basic settings.'
        super(ErrorLoadSettings, self).__init__(message)

class ErrorFile(Exception):

    def __init__(self, parameter: str='Ops'):
        message = f'File Error: [{parameter}]'
        super(ErrorFile, self).__init__(message)

class ErrorOptionIsMissing(Exception):

    def __init__(self, parameter):
        message = f'Option [{parameter}] is missing!'
        super(ErrorOptionIsMissing, self).__init__(message)

class ErrorOptionIsInvalid(Exception):

    def __init__(self, parameter, options):
        message = f'Option [{parameter}] invalid! Usage: {str(options)}'
        super(ErrorOptionIsInvalid, self).__init__(message)

class ErrorInvalidValue(Exception):

    def __init__(self, parameter):
        message = f'Option [{parameter}] invalid value!'
        super(ErrorInvalidValue, self).__init__(message)

class ErrorParameterIsMissing(Exception):

    def __init__(self, parameter):
        message = f'Parameter --{parameter} is missing'
        super(ErrorParameterIsMissing, self).__init__(message)

class ErrorArgumentIsInvalid(Exception):

    def __init__(self, argument, error):
        message = f'Argument [{argument}] invalid! {str(error)}'
        super(ErrorArgumentIsInvalid, self).__init__(message)

def print_warning(parameter):
    print(color(text='WARNING: ' + parameter, types=['bold', 'yellow']))

def print_error(parameter):
    print(color(text='ERROR: ' + parameter, types=['bold', 'red']))