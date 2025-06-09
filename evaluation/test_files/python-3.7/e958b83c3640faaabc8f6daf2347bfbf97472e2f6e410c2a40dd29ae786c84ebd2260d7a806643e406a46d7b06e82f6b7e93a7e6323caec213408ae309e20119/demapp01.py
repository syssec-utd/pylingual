import numpy as np
import matplotlib.pyplot as plt
from compecon import BasisChebyshev, BasisSpline, demo

def f(x):
    return np.exp(-x)

def d1(x):
    return -np.exp(-x)

def d2(x):
    return np.exp(-x)
(n, a, b) = (10, -1, 1)

def plotzero():
    plt.hlines(0, a, b, 'k', linestyle='--', linewidth=2)
F = BasisChebyshev(n, a, b, f=f)
x = 0
ffit = F(x)
dfit1 = F(x, 1)
dfit2 = F(x, 2)
intfit = F(x, -1)
print('Function Values, Derivatives and Definite Integral of exp(-x) at x=0')
print('%-20s %12s %12s' % (' ', 'Numerical', 'Analytic'))
print('%-20s %12.8f %12.8f' % ('Function', ffit, f(x)))
print('%-20s %12.8f %12.8f' % ('First Derivative', dfit1, d1(x)))
print('%-20s %12.8f %12.8f' % ('Second Derivative', dfit2, d2(x)))
print('%-20s %12.8f %12.8f' % ('Definite Integral', intfit, np.exp(1) - 1))
nplot = 501
xgrid = np.linspace(a, b, nplot)
figures = []

def approx_error(true_func, appr_func, d=0, title=''):
    demo.figure(title, 'x', 'Error')
    plotzero()
    plt.plot(xgrid, appr_func(xgrid, d) - true_func(xgrid))
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    figures.append(plt.gcf())
approx_error(f, F, title='Chebychev Approximation Error - Function')
approx_error(d1, F, 1, title='Chebychev Approximation Error - First Derivative')
approx_error(d2, F, 2, title='Chebychev Approximation Error - Second Derivative')
n = 21
S = BasisSpline(n, a, b, f=f)
yapp = S(xgrid)
approx_error(f, S, title='Cubic Spline Approximation Error - Function')
approx_error(d1, S, 1, title='Cubic Spline Approximation Error - First Derivative')
approx_error(d2, S, 2, title='Cubic Spline Approximation Error - Second Derivative')
n = 31
L = BasisSpline(n, a, b, k=1, f=f)
approx_error(f, L, title='Linear Spline Approximation Error - Function')
demo.savefig(figures)