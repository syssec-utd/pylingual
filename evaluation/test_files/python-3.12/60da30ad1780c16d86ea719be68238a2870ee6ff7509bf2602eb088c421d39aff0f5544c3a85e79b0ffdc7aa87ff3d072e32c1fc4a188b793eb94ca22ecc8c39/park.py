import numpy as np
from scipy.integrate import quad
from scipy.special import gamma

class Park(object):
    """Class for fatigue life estimation using frequency domain 
    method by Park et al.[1].
      
    References
    ----------
    [1] Jun-Bum Park, Joonmo Choung and Kyung-Su Kim. A new fatigue prediction model for marine 
        structures subject to wide band stress process. Ocean Engineering, 76: 144-151, 2014
    [2] Janko Slavič, Matjaž Mršnik, Martin Česnik, Jaka Javh, Miha Boltežar. 
        Vibration Fatigue by Spectral Methods, From Structural Dynamics to Fatigue Damage
        – Theory and Experiments, ISBN: 9780128221907, Elsevier, 1st September 2020
        
    Example
    -------
    Import modules, define time- and frequency-domain data

    >>> import FLife
    >>> import pyExSi as es
    >>> import numpy as np
    >>> from matplotlib import pyplot as plt
    >>> # time-domain data
    >>> N = 2 ** 16  # number of data points of time signal
    >>> fs = 2048  # sampling frequency [Hz]
    >>> t = np.arange(0, N) / fs  # time vector
    >>> # frequency-domain data
    >>> M = N // 2 + 1  # number of data points of frequency vector
    >>> freq = np.arange(0, M, 1) * fs / N  # frequency vector
    >>> PSD_lower = es.get_psd(freq, 20, 60, variance = 5)  # lower mode of random process
    >>> PSD_higher = es.get_psd(freq, 100, 120, variance = 2)  # higher mode of random process
    >>> PSD = PSD_lower + PSD_higher # bimodal one-sided flat-shaped PSD

    Get Gaussian stationary signal, instantiate SpectralData object and plot PSD

    >>> rg = np.random.default_rng(123) # random generator seed
    >>> x = es.random_gaussian(N, PSD, fs, rg) # Gaussian stationary signal
    >>> sd = FLife.SpectralData(input=x, dt=1/fs) # SpectralData instance
    >>> plt.plot(sd.psd[:,0], sd.psd[:,1]) 
    >>> plt.xlabel('Frequency [Hz]')
    >>> plt.ylabel('PSD')

    Define S-N curve parameters and get fatigue-life estimatate

    >>> C = 1.8e+22  # S-N curve intercept [MPa**k]
    >>> k = 7.3 # S-N curve inverse slope [/]
    >>> park = FLife.Park(sd)
    >>> print(f'Fatigue life: {park.get_life(C,k):.3e} s.')

    Define stress vector and depict stress peak PDF

    >>> s = np.arange(0,np.max(x),.01) 
    >>> plt.plot(s,park.get_PDF(s))
    >>> plt.xlabel('Stress [MPa]')
    >>> plt.ylabel('PDF')
    """

    def __init__(self, spectral_data):
        """Get needed values from reference object.

        :param spectral_data:  Instance of class SpectralData
        """
        self.spectral_data = spectral_data
        self._set_distribution_parameters()

    def get_PDF(self, s):
        """Returns cycle PDF(Probability Density Function) as a function of stress s.

        :param s:  numpy.ndarray
            Stress vector.
        :return: function pdf(s)
        """
        m0 = self.spectral_data.moments[0]

        def park_pdf(s):
            gauss_pdf = lambda s: 2 / (np.sqrt(2 * np.pi) * self.parameters['sigma_g']) * np.exp(-s ** 2 / (2 * self.parameters['sigma_g'] ** 2))
            rayleigh1_pdf = lambda s: s / self.parameters['sigma_r1'] ** 2 * np.exp(-s ** 2 / (2 * self.parameters['sigma_r1'] ** 2))
            rayleigh2_pdf = lambda s: s * np.exp(-s ** 2 / 2)
            pdf_out = self.parameters['C_g'] * gauss_pdf(s) + self.parameters['C_r1'] * rayleigh1_pdf(s) + self.parameters['C_r2'] * rayleigh2_pdf(s)
            return pdf_out
        return 1 / np.sqrt(m0) * park_pdf(s / np.sqrt(m0))

    def get_life(self, C, k, integrate_pdf=False):
        """Calculate fatigue life with parameters C, k, as defined in [2].

        :param C: [int,float]
            S-N curve intercept [MPa**k].
        :param k: [int,float]
            S-N curve inverse slope [/].
        :return:
            Estimated fatigue life in seconds.
        :rtype: float
        """
        m0 = self.spectral_data.moments[0]
        m_p = self.spectral_data.m_p
        if integrate_pdf:
            d = m_p / C * quad(lambda s: s ** k * self.get_PDF(s), a=0, b=np.Inf)[0]
        else:
            m0 = self.spectral_data.moments[0]
            d = m_p / C * np.sqrt(2 * m0) ** k * (self.parameters['C_r1'] * self.parameters['sigma_r1'] ** k * gamma(1 + k / 2) + self.parameters['C_r2'] * gamma(1 + k / 2) + self.parameters['C_g'] / np.sqrt(np.pi) * self.parameters['sigma_g'] ** k * gamma((1 + k) / 2))
        T = 1.0 / d
        return T

    def _set_distribution_parameters(self):
        """Define PDF parameters; 
        """
        alpha2 = self.spectral_data.alpha2
        alpha0_95 = self.spectral_data.get_bandwidth_estimator(self.spectral_data.PSD_splitting, i=0.95)[0]
        alpha1_97 = self.spectral_data.get_bandwidth_estimator(self.spectral_data.PSD_splitting, i=1.97)[0]
        alpha0_54 = self.spectral_data.get_bandwidth_estimator(self.spectral_data.PSD_splitting, i=0.54)[0]
        alpha0_93 = self.spectral_data.get_bandwidth_estimator(self.spectral_data.PSD_splitting, i=0.93)[0]
        alpha1_95 = self.spectral_data.get_bandwidth_estimator(self.spectral_data.PSD_splitting, i=1.95)[0]
        M_rr_1 = alpha2
        M_rr_2 = alpha0_95 * alpha1_97
        M_rr_3 = alpha0_54 * alpha0_93 * alpha1_95
        sigma_r1 = alpha2
        C_r1 = (M_rr_2 - M_rr_3) / (sigma_r1 ** 2 * (1 - sigma_r1))
        C_r2 = (-sigma_r1 * M_rr_2 + M_rr_3) / (1 - sigma_r1)
        C_g = 1 - C_r1 - C_r2
        V_1 = 1 / np.sqrt(np.pi) * gamma(1) / gamma(1.5)
        sigma_g = 1 / (V_1 * C_g) * (M_rr_1 - C_r1 * sigma_r1 - C_r2)
        self.parameters = {}
        self.parameters['sigma_r1'] = sigma_r1
        self.parameters['sigma_g'] = sigma_g
        self.parameters['C_r1'] = C_r1
        self.parameters['C_r2'] = C_r2
        self.parameters['C_g'] = C_g