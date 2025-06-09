import numpy as np
from numpy import pi, sin
from cubature import cubature

def integrand_rectangle(x_array):
    return 1.0

def integrand_rectangle_v(x_array):
    return np.ones_like(x_array[:, 0])

def integrand_circle(x_array):
    return x_array[0]

def integrand_circle_v(x_array):
    return x_array[:, 0]

def exact_rectangle(a, b):
    return a * b

def exact_circle(r):
    return pi * r ** 2
if __name__ == '__main__':
    print('_________________')
    print('')
    print('Rectangle')
    (a, b) = (3, 5)
    xmin = [0, 0]
    xmax = [a, b]
    (val, err) = cubature(integrand_rectangle, 2, 1, xmin, xmax)
    print('Approximated: {0}'.format(val))
    print('Exact: {0}'.format(exact_rectangle(a, b)))
    print('_________________')
    print('')
    print('Rectangle (vectorized)')
    (a, b) = (3, 5)
    xmin = [0, 0]
    xmax = [a, b]
    (val, err) = cubature(integrand_rectangle_v, 2, 1, xmin, xmax, vectorized=True)
    print('Approximated: {0}'.format(val))
    print('Exact: {0}'.format(exact_rectangle(a, b)))
    print('_________________')
    print('')
    print('Circle')
    r = 3.0
    xmin = [0, 0]
    xmax = [r, 2 * pi]
    (val, err) = cubature(integrand_circle, 2, 1, xmin, xmax)
    print('Approximated: {0}'.format(val))
    print('Exact: {0}'.format(exact_circle(r)))
    print('_________________')
    print('_________________')
    print('')
    print('Circle (vectorized)')
    r = 3.0
    xmin = [0, 0]
    xmax = [r, 2 * pi]
    (val, err) = cubature(integrand_circle_v, 2, 1, xmin, xmax, vectorized=True)
    print('Approximated: {0}'.format(val))
    print('Exact: {0}'.format(exact_circle(r)))
    print('_________________')