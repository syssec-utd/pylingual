from itertools import repeat
from typing import Optional, Sequence
import numpy as np

def getFTMatrix(fList: Sequence[float], numOfPoints: int, phaseList: Optional[Sequence[float]]=None, weight: Optional[np.ndarray]=None, sampleRate: float=1000000000.0) -> np.ndarray:
    """
    get a matrix for Fourier transform

    Args:
        fList (Sequence[float]): list of frequencies
        numOfPoints (int): size of signal frame
        phaseList (Optional[Sequence[float]], optional): list of phase. Defaults to None.
        weight (Optional[np.ndarray], optional): weight or list of weight. Defaults to None.
        sampleRate (float, optional): sample rate of signal. Defaults to 1e9.

    Returns:
        numpy.ndarray: exp matrix
    
    >>> shots, numOfPoints, sampleRate = 100, 1000, 1e9
    >>> f1, f2 = -12.7e6, 32.8e6
    >>> signal = np.random.randn(shots, numOfPoints)
    >>> e = getFTMatrix([f1, f2], numOfPoints, sampleRate=sampleRate)
    >>> ret = signal @ e
    >>> ret.shape
    (100, 2)
    >>> t = np.arange(numOfPoints) / sampleRate
    >>> signal = 0.8 * np.sin(2 * np.pi * f1 * t) + 0.2 * np.cos(2 * np.pi * f2 * t)
    >>> signal @ e
    array([-0.00766509-0.79518987j,  0.19531432+0.00207068j])
    >>> spec = 2 * np.fft.fft(signal) / numOfPoints
    >>> freq = np.fft.fftfreq(numOfPoints)
    >>> e = getFTMatrix(freq, numOfPoints, sampleRate=1)
    >>> np.allclose(spec, signal @ e)
    True
    """
    e = []
    t = np.linspace(0, numOfPoints / sampleRate, numOfPoints, endpoint=False)
    if weight is None or len(weight) == 0:
        weight = np.full(numOfPoints, 2 / numOfPoints)
    if phaseList is None or len(phaseList) == 0:
        phaseList = np.zeros_like(fList)
    if weight.ndim == 1:
        weightList = repeat(weight)
    else:
        weightList = weight
    for (f, phase, weight) in zip(fList, phaseList, weightList):
        e.append(weight * np.exp(-1j * (2 * np.pi * f * t + phase)))
    return np.asarray(e).T
if __name__ == '__main__':
    import doctest
    doctest.testmod()