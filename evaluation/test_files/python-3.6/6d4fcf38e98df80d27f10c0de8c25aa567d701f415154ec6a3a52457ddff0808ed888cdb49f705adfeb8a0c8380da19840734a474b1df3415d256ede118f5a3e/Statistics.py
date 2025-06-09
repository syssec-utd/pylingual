""" This is the "Statistics" sub-module. """

def mean(data):
    if isinstance(data, (list, tuple, set)):
        if data != None and sum(data) != 0:
            return sum(data) / len(data)
        else:
            raise Exception("The data can't be null and the sum of the data can't be zero.")
    else:
        raise TypeError('The data should be in the form of a list, tuple, or set.')

def mode(data):
    if isinstance(data, (list, tuple, set)):
        if data != None and sum(data) != 0:
            return max(data)
        else:
            raise Exception("The data can't be null and the sum of the data can't be zero.")
    else:
        raise TypeError('The data should be in the form of a list, tuple, or set.')

def median(data):
    if isinstance(data, (list, tuple, set)):
        if data != None and sum(data) != 0:
            data.sort()
            mid = len(data) // 2
            return (data[mid] + data[~mid]) / 2
        else:
            raise Exception("The data can't be null and the sum of the data can't be zero.")
    else:
        raise TypeError('The data should be in the form of a list, tuple, or set.')