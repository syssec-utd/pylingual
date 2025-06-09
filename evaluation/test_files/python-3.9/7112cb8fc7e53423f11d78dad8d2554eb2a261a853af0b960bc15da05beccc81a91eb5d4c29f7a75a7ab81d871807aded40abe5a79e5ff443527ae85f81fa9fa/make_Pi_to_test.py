_Pi = ['./a.py', './b.py', './c.py']
_test_all = False
_prev = {'./b.py': 32481.8, './c.py': 32497.3}
_last_mods = {'./a.py': 97551.0, './b.py': 32481.8, './c.py': 32497.3}

def f(_Pi, test_all, prev, last_mods):
    return (_Pi.copy() if test_all else [_pi for _pi in _Pi if (prev[_pi] if _pi in prev else 0) != (last_mods[_pi] if _pi in last_mods else 0)]) or _Pi.copy()
t = lambda : ['./a.py'] == f(_Pi, _test_all, _prev, _last_mods)