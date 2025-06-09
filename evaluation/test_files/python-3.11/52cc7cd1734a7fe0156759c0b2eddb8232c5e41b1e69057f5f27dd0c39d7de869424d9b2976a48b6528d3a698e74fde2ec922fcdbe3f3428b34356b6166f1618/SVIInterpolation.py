u"""
Created on 2017-1-7

@author: cheng.li
"""
import numpy as np
from scipy.optimize import least_squares
from PyFin.PricingEngines.SVIInterpolationImpl import sviVolatility
from PyFin.PricingEngines.SVIInterpolationImpl import sviVolatilities
from PyFin.PricingEngines.SVIInterpolationImpl import _sviCalibrationIteration
from PyFin.PricingEngines.SVIInterpolationImpl import _parametersCheck

def sviCalibration(strikes, volatilites, forward, expiryTime, initialA, initialB, initialSigma, initialRho, initialM, isFixedA=False, isFixedB=False, isFixedSigma=False, isFixedRho=False, isFixedM=False, method='trf'):
    x0, freeParameters, fixedParameters, bounds = _parametersCheck(initialA, initialB, initialSigma, initialRho, initialM, isFixedA, isFixedB, isFixedSigma, isFixedRho, isFixedM)
    if method != 'lm':
        x = least_squares(_sviCalibrationIteration, x0, method=method, bounds=bounds, ftol=1e-10, gtol=1e-10, xtol=1e-10, args=(freeParameters, strikes, volatilites, forward, expiryTime, fixedParameters))
    else:
        x = least_squares(_sviCalibrationIteration, x0, method=method, ftol=1e-10, gtol=1e-10, xtol=1e-10, args=(freeParameters, strikes, volatilites, forward, expiryTime, fixedParameters))
    parameters = ['a', 'b', 'sigma', 'rho', 'm']
    calibratedParameters = dict(zip(freeParameters, x.x))
    res = []
    for name in parameters:
        try:
            res.append(calibratedParameters[name])
        except KeyError:
            res.append(fixedParameters[name])
    return (np.array(res), x.status, x.message)
__all__ = ['sviVolatility', 'sviVolatilities', 'sviCalibration']