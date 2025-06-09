def check_docs(variable, search, m):
    if type(getattr(variable, m).__doc__) != str:
        return False
    else:
        return search in getattr(variable, m).__doc__

def s(variable, search: str):
    methods = dir(variable)
    return [m for m in methods if search in m]

def d(variable, search: str):
    methods = dir(variable)
    for m in methods:
        if check_docs(variable, search, m):
            doc = getattr(variable, m).__doc__
            tar = doc.index(search)
            print(f'\x1b[0m \x1b[1m {m}:')
            print(f'\x1b[0m{doc[tar - 100:tar - 5]}\x1b[31m{doc[tar - 5:tar + 5]}\x1b[0m{doc[tar + 5:tar + 100]}')

def a(variable):
    methods = dir(variable)
    return {m: getattr(variable, m) for m in methods if not m.startswith('_')}