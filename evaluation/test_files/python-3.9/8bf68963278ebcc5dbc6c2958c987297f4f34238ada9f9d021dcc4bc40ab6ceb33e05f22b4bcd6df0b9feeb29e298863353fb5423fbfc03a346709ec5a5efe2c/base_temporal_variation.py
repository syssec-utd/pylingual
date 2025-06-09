import jax
import jax.numpy as np
from jax import vmap
import equinox as eqx
from copy import deepcopy
import dLux

class OpticalSystem(eqx.Module):
    """ Optical System class, Equinox Modle
    
    DOCSTRING NOT COMPLETE
    
    A Class to store and apply properties external to the optical system
    Ie: stellar positions and spectra
    
    positions: (Nstars, 2) array
    wavels: (Nwavels) array
    weights: (Nwavel)/(Nwavels, Nstars) array
    
    dLux currently does not check that inputs are correctly shaped/formatted!

    Notes:
     - Take in layers in order to re-intialise the model every call?
    
    General images output shape: (Nimages, Nstars, Nwavels, Npix, Npix)
    
     - Currently doesnt allow temporal variation in spectrum because I'm lazy
     - Currently doesnt allow temporal variation in flux because I'm lazy
    
    TODO: Add getter methods for acessing weights and fluxes attributes that
    use np.squeeze to remove empy axes

    
    Attributes
    ----------
    layers: list, required
        - A list of layers that defines the tranformaitons and operations of the system (typically optical)
     
    wavels: ndarray, optional
        - An array of wavelengths in meters to simulate
        - The shape must be 1d - stellar spectrums are controlled through the weights parameter
        - No default value is set if not provided and this will throw an error if you try to call functions that depend on this parameter
        - It is left as optional so that functions that allow wavelength input can be called on objects without having to pre-input wavelengths
    positions: ndarray, optional
        - An array of (x,y) stellar positions in units of radians, measured as deviation of the optical axis. 
        - Its input shape should be (Nstars, 2), defining an x, y position for each star. 
        - If not provided, the value defaults to (0, 0) - on axis
    fluxes: ndarray, optional
        - An array of stellar fluxes, its length must match the positions inputs size to work properly
        - Theoretically this has arbitrary units, but we think of it as photons
        - Defaults to 1 (ie, returning a unitary flux psf if not specified)
    weights: ndarray, optional
        - An array of stellar spectral weights (arb units)
        - This can take multiple shapes
        - Default is to weight all wavelengths equally (top-hat)
        - If a 1d array is provided this is applied to all stars, shape (Nwavels)
        - if a 2d array is provided each is applied to each individual star, shape (Nstars, Nwavels)
        - Note the inputs values are always normalised and will not directly change total output flux (inderectly it can change it by weighting more flux to wavelengths with more aperture losses, for example)
    dithers: ndarray, optional
        - An arary of (x, y) positional dithers in units of radians
        - Its input shape should be (Nims, 2), defining the (x,y) dither for each image
        - if not provided, defualts to no-dither
    detector_layers: list, optional
        - A second list of layer objects designed to allow processing of psfs, rather than wavefronts
        - It is applied to each image after psfs have been approraitely weighted and summed
    
    
    """
    Nstars: int
    Nwavels: int
    Nims: int
    wavels: np.ndarray
    positions: np.ndarray
    fluxes: np.ndarray
    weights: np.ndarray
    dithers: np.ndarray
    layers: list
    detector_layers: list
    temporal_variation: bool

    def __init__(self, layers, wavels=None, positions=None, fluxes=None, weights=None, dithers=None, detector_layers=None, temporal_variation=False):
        self.layers = layers
        self.wavels = np.array(wavels).astype(float)
        self.positions = np.zeros([1, 2]) if positions is None else np.array(positions)
        self.fluxes = np.ones(len(self.positions)) if fluxes is None else np.array(fluxes)
        self.weights = np.ones(len(self.wavels)) if weights is None else np.array(weights)
        self.dithers = np.zeros([1, 2]) if dithers is None else dithers
        self.detector_layers = [] if detector_layers is None else detector_layers
        self.temporal_variation = bool(temporal_variation)
        if self.fluxes.shape == ():
            self.fluxes = np.array([self.fluxes])
        self.Nwavels = 0 if wavels is None else len(self.wavels)
        if not self.temporal_variation:
            self.Nstars = len(self.positions)
            self.Nims = len(self.dithers)
            assert self.positions.shape[-1] == 2, 'Input positions must be \n            of shape (Nstars, 2)'
            assert self.fluxes.shape[0] == self.Nstars, 'Input fluxes must be\n            match input positions.'
            weight_shape = self.weights.shape
            if len(weight_shape) == 1 and weights is not None:
                assert weight_shape[0] == self.Nwavels, 'Inputs weights shape \n                must be either (len(wavels)) or  (len(positions), len(wavels)), \n                got shape: {}'.format(self.weights.shape)
            elif len(weight_shape) == 2:
                assert weight_shape == [self.Nstars, self.Nwavels], 'Inputs \n                weights shape must be either (len(wavels)) or  (len(positions), \n                len(wavels))'
        else:
            print('Warning, inputs shapes are not checked for temporally \n            varying models, and is minimally tested. Currently only supports \n            single-star models, and seems to flip x-y positions likely \n            originating from the dither_positions method')
            self.Nstars = 1
            self.Nims = len(self.positions)
            assert len(self.positions) == len(self.fluxes), 'Input positions\n            and fluxes must have the same shape'

    def debug_prop(self, wavel, offset=np.zeros(2)):
        """
        I believe this is diffable but there is no reason to force it to be
        """
        params_dict = {'Wavefront': dLux.PhysicalWavefront(wavel, offset)}
        intermeds = []
        layers_applied = []
        for i in range(len(self.layers)):
            params_dict = self.layers[i](params_dict)
            intermeds.append(deepcopy(params_dict))
            layers_applied.append(self.layers[i].__str__())
        return (params_dict['Wavefront'].wavefront_to_psf(), intermeds, layers_applied)
    '################################'
    '################################'

    def __call__(self):
        """
        Maps the wavelength and position calcualtions across multiple dimesions
        
        To Do: Reformat the vmaps such that we only vmap over wavelengths and
        positions in order to simplify the dimensionality
        """
        propagate_single = vmap(self.propagate_mono, in_axes=(0, None))
        propagator = vmap(propagate_single, in_axes=(None, 0))
        dithered_positions = self.dither_positions()
        psfs = propagator(self.wavels, dithered_positions)
        psfs = self.reshape_psfs(psfs)
        psfs = self.weight_psfs(psfs).sum([1, 2])
        detector_vmap = vmap(self.apply_detector_layers, in_axes=0)
        images = detector_vmap(psfs)
        return np.squeeze(images)

    def propagate_mono(self, wavel, offset=np.zeros(2)):
        """
        
        """
        params_dict = {'Wavefront': dLux.PhysicalWavefront(wavel, offset), 'Optical System': self}
        for i in range(len(self.layers)):
            params_dict = self.layers[i](params_dict)
        return params_dict['Wavefront'].wavefront_to_psf()

    def propagate_single(self, wavels, offset=np.zeros(2), weights=1.0, flux=1.0, apply_detector=False):
        """
        Only propagates a single star, allowing wavelength input
        sums output to single array
        
        Wavels must be an array and the same shape as weights if provided
        """
        prop_wf_map = vmap(self.propagate_mono, in_axes=(0, None))
        psfs = weights * prop_wf_map(wavels, offset) / len(wavels)
        image = flux * psfs.sum(0)
        if apply_detector:
            image = self.apply_detector_layers(image)
        return image

    def apply_detector_layers(self, image):
        """
        
        """
        for i in range(len(self.detector_layers)):
            image = self.detector_layers[i](image)
        return image

    def reshape_psfs(self, psfs):
        """
        
        """
        npix = psfs.shape[-1]
        if not self.temporal_variation:
            return psfs.reshape([self.Nims, self.Nstars, self.Nwavels, npix, npix])
        else:
            return psfs.reshape([self.Nims, 1, self.Nwavels, npix, npix])

    def dither_positions(self):
        """
        Dithers the input positions, returned with shape (Npsfs, 2)
        """
        if not self.temporal_variation:
            Npsfs = self.Nstars * self.Nims
            shaped_pos = self.positions.reshape([1, self.Nstars, 2])
            shaped_dith = self.dithers.reshape([self.Nims, 1, 2])
            dithered_positions = (shaped_pos + shaped_dith).reshape([Npsfs, 2])
        else:
            dithered_positions = self.positions
        return dithered_positions

    def weight_psfs(self, psfs):
        """
        Normalise Weights, and format weights/fluxes
        Psfs output shape: (Nims, Nstars, Nwavels, npix, npix)
        We want weights shape: (1, 1, Nwavels, 1, 1)
        We want fluxes shape: (1, Nstars, 1, 1, 1)
        
        Something else for temporal variation
        """
        Nims = self.Nims
        Nstars = self.Nstars
        Nwavels = self.Nwavels
        if len(self.weights.shape) == 3:
            weights_in = self.weights.reshape([Nims, Nstars, Nwavels, 1, 1])
            weights_in /= np.expand_dims(weights_in.sum(2), axis=2)
        elif len(self.weights.shape) == 2:
            weights_in = self.weights.reshape([1, Nstars, Nwavels, 1, 1])
            weights_in /= np.expand_dims(weights_in.sum(2), axis=2)
        elif self.weights.shape[0] == self.Nwavels:
            weights_in = self.weights.reshape([1, 1, Nwavels, 1, 1])
            weights_in /= np.expand_dims(weights_in.sum(2), axis=2)
        else:
            weights_in = self.weights
        if not self.temporal_variation:
            if len(self.fluxes) == 1:
                fluxes = self.fluxes
            else:
                fluxes = self.fluxes.reshape([1, Nstars, 1, 1, 1])
        else:
            fluxes = self.fluxes.reshape([Nims, 1, 1, 1, 1])
        psfs *= weights_in
        psfs *= fluxes
        return psfs