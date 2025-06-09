from numpy import *
from numpy.linalg import lstsq

def jacob(f, x, y=None, mask=None, eps=1e-05):
    if mask is None:
        mask = ones(len(f(x)), dtype=bool)
    if y is None:
        y = f(x) * 0
    m, n = (sum(mask), len(x))
    jac = zeros((m, n))
    x1 = x.copy()
    for i in range(n):
        xstep = x[i] * eps
        x1[i] = x[i] + xstep
        y1 = f(x1)[mask]
        jac[:, i] = (y1 - y) / xstep
        x1[i] = x[i]
    return jac

def merit(f, mask, x, xbest, penbest):
    y = f(x)
    mask |= (y < 0) & ~mask
    y = y[mask]
    pen = dot(y, y)
    if penbest > pen:
        penbest = pen
        xbest = x.copy()
    return (y, pen, penbest, xbest)

def _pdebug(msg, debug):
    if debug:
        (print(msg),)

def jacobian(myf, xstart, maskstart=None, maxsteps=20, bisec=10, tol=1e-20, maxcalls=10000, eps=None, debug=True):
    raise NotImplementedError
    xstart = array(xstart)
    x = xstart.copy()
    ystart = myf(xstart)
    if not hasattr(ystart, '__len__'):
        f = lambda x: array([myf(x)])
    else:
        f = lambda x: array(myf(x))
    if maskstart is None:
        maskstart = ones(len(f(xstart)), dtype=bool)
    mask = maskstart.copy()
    if eps is None:
        eps = sqrt(dot(x, x)) * 0.001
    xbest = xstart.copy()
    penbest = 1e+200
    ncalls = 0
    info = {}
    for step in range(maxsteps):
        mask[:] = maskstart
        y, pen, penbest, xbest = merit(f, mask, x, xbest, penbest)
        ncalls += 1
        _pdebug('%5d %6d' % (step, ncalls), debug)
        _pdebug('%12.5e %s' % (pen, sum(mask)), debug)
        if pen < tol:
            info['desc'] = 'tollerance met'
            _pdebug('\n', debug)
            break
        if ncalls > maxcalls:
            info['desc'] = 'max calls reached'
            _pdebug('\n', debug)
            break
        jac = jacob(f, x, y, mask, eps=eps)
        ncalls += len(x)
        xstep = lstsq(jac, y, rcond=None)[0]
        newpen = pen * 2
        alpha = -1
        while newpen > pen:
            if alpha > bisec:
                break
            alpha += 1
            l = 2.0 ** (-alpha)
            ytest, newpen, penbest, xbest = merit(f, mask, x - l * xstep, xbest, penbest)
            ncalls += 1
        _pdebug(alpha, debug)
        x -= l * xstep
        _pdebug('\n', debug)
        if alpha > 30:
            info['desc'] = 'not any progress'
            break
    else:
        info['desc'] = 'max num iteration reached'
    info['ncalls'] = ncalls
    info['penalty'] = penbest
    if penbest < tol:
        info['success'] = True
    else:
        info['success'] = False
    return (xbest, info)
if __name__ == '__main__':

    def f(x, y=zeros(4)):
        y[0] = x[1] ** 2 + sin(x[2]) - 4
        y[1] = x[1] ** 3 + sin(x[2]) - 8
        y[2] = x[0] ** 2 + sin(x[1]) - 2
        y[3] = x[0] + 3
        return y
    x = array([1, 2.0, 3])
    f(x)
    x, info = jacobian(f, x, array([True, True, True, False]))
    f(x)