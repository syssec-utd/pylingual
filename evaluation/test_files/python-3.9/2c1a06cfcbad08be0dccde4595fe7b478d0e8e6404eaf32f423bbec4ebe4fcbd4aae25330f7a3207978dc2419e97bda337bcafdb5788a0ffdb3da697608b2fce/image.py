import numpy as np
from photutils.detection import DAOStarFinder
from photutils.background import Background2D, SExtractorBackground
from astropy.stats import SigmaClip
from astropy.io import fits
from PIL import Image

def read_image(imagefile):
    """
    Read an astronomical image captured by cameras in fits format or in generic image format.

    Usage:
        >>> imagefile = 'obs/fits/img_00000.fits' # imagefile = 'obs/bmp/img_00000.bmp'
        >>> image_raw = read_image(imagefile)

    Inputs:
        imagefile -> [str] image filename

    Outputs:
        image_raw -> [2d array of float] raw grayscale image with origin at bottom left corner point
    """
    if imagefile.split('.')[1] in ['fits', 'fit']:
        unit_list = fits.open(imagefile)
        image_raw = unit_list[0].data.astype(float)
    else:
        image_raw = Image.open(imagefile).convert('L')
        image_raw = np.asarray(image_raw)
    image_raw = image_raw[::-1]
    return image_raw

def source_extract(image_raw, max_control_points=60, fwhm=12, mask=False):
    """
    Search for star spots in an image, extracting their centroids and doing photometry.

    Usage: 
        >>> imagefile = 'obs/fits/img_00000.fits' # imagefile = 'obs/bmp/img_00000.bmp'
        >>> image_raw = read_image(imagefile)
        >>> xy_centroids,offset,image,bkg_rms,mask_rectangle = source_extract(image_raw)
    
    Inputs:
        image_raw -> [2d array of float] raw grayscale image with origin at bottom left corner point  
        max_control_points -> [int,optional,default=50] Maximum number of sources to extract
        fwhm -> [float,optional,default=15] Full-width half-maximum (FWHM) of the Gaussian kernel in units of pixels used in DAOStarFinder
        mask -> [bool,optional,default=False] A True value indicates the edge area of an image is masked. Masked pixels are ignored when searching for stars.

    Outputs:
        xy_centroids -> [2d array of float] Cartesian pixel coordinates of the centroids of star spots
        offset -> [array of float] Cartesian coordinates of the center of the image
        image -> [2d array of float] signal, i.e. subtracting the background gray value from the raw grayscale image
        bkg_rms -> [2d array of float] background noise
        mask_rectangle -> [None or tuple] If None, then no mask rectangle is generated; Else, a rectangle defined by the bottom left corner point, width and height is generated
    """
    (yc, xc) = image_raw.shape
    offset = np.array([xc / 2, yc / 2]) - 0.5
    sigma_clip = SigmaClip(sigma=3.0)
    bkg_estimator = SExtractorBackground()
    bkg = Background2D(image_raw, (yc // 16, xc // 16), filter_size=(3, 3), sigma_clip=sigma_clip, bkg_estimator=bkg_estimator)
    image = image_raw - bkg.background
    bkg_rms = bkg.background_rms
    bkg_sigma = bkg.background_rms_median
    if mask:
        mask_region = np.ones(image_raw.shape, dtype=bool)
        (bb, ub) = (yc // 4, yc // 4 * 3)
        (lb, rb) = (xc // 4, xc // 4 * 3)
        (width, height) = (xc // 2, yc // 2)
        mask_rectangle = ([lb, bb], width, height)
        mask_region[bb:ub, lb:rb] = False
    else:
        mask_region = None
        mask_rectangle = None
    daofind = DAOStarFinder(fwhm=fwhm, threshold=5 * bkg_sigma, brightest=max_control_points)
    star_spots = daofind(image, mask=mask_region)
    xy_centroids = np.transpose((star_spots['xcentroid'], star_spots['ycentroid']))
    return (xy_centroids, offset, image, bkg_rms, mask_rectangle)