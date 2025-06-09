def splitBy(data, num):
    """ Turn a list to list of list """
    return [data[i:i + num] for i in range(0, len(data), num)]