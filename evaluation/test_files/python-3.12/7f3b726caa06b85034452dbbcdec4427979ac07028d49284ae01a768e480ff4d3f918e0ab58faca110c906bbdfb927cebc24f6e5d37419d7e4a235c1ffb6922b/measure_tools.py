"""
Created on Mon Sep  7 14:38:27 2020

@author: Xuheng Ding

A group of function to measure the photometry.
"""
import numpy as np
import matplotlib.pyplot as plt
import astropy.io.fits as pyfits
import scipy.ndimage as ndimage
import scipy.ndimage.filters as filters
from matplotlib.colors import LogNorm
from matplotlib.ticker import AutoMinorLocator
import copy
import matplotlib
from photutils import make_source_mask
from galight.tools.astro_tools import plt_fits
my_cmap = copy.copy(matplotlib.cm.get_cmap('gist_heat'))
my_cmap.set_bad('black')
import photutils
from packaging import version

def find_loc_max(image, neighborhood_size=8, threshold=5):
    """
    Find all the local maximazation in a 2D array, used to search the targets such as QSOs and PSFs.
    This function is created and inspired based on:
        https://stackoverflow.com/questions/9111711/get-coordinates-of-local-maxima-in-2d-array-above-certain-value
   
    Parameter
    --------
        image: 
            2D array type image.
        
        neighborhood_size: digit.
            Define the region size to filter the local minima.
        
        threshold: digit.
            Define the significance (flux value) of the maximazation point. The lower, the more would be found.
    
    Return
    --------
        A list of x and y of the searched local maximazations.
    """
    data_max = filters.maximum_filter(image, neighborhood_size)
    maxima = image == data_max
    data_min = filters.minimum_filter(image, neighborhood_size)
    diff = data_max - data_min > threshold
    maxima[diff == 0] = 0
    labeled, num_objects = ndimage.label(maxima)
    slices = ndimage.find_objects(labeled)
    x, y = ([], [])
    for dy, dx in slices:
        x_center = (dx.start + dx.stop - 1) / 2
        x.append(x_center)
        y_center = (dy.start + dy.stop - 1) / 2
        y.append(y_center)
    return (x, y)

def search_local_max(image, radius=120, view=False, **kwargs):
    """
    Use 'find_loc_max()' to search all the maxs. The edges position with a lot of zeros would be excluded.
    
    Parameter
    --------
        image: 
            2D array type image.
        
        radius: 
            A radius used to test if any empty pixels around.
        
    Return
    --------
        A list of positions of 'PSF'
    """
    from galight.tools.cutout_tools import cutout
    PSFx, PSFy = find_loc_max(image, **kwargs)
    PSF_locs = []
    ct = 0
    for i in range(len(PSFx)):
        cut_img = cutout(image, [PSFx[i], PSFy[i]], radius=radius)
        cut_img[np.isnan(cut_img)] = 0
        if np.sum(cut_img == 0) > len(cut_img) ** 2 / 20:
            continue
        PSF_locs.append([PSFx[i], PSFy[i]])
        if view == True:
            print('plot for position: [{0}, {1}]'.format(PSFx[i], PSFy[i]), 'idx:', ct)
            print('total flux:', cut_img.sum())
            print('measure FWHM:', np.round(measure_FWHM(cut_img), 3))
            plt_fits(cut_img)
            print('================')
            ct += 1
    return PSF_locs

def measure_FWHM(image, radius=10):
    """
    Fit image as 2D gaussion to calculate the FWHM on four directions.
    
    Parameter
    --------
        image: 
            2D array type image.
            
        radius: 
            Define the distance (2*radius) to sample the pixel value and fit Gaussian.
        
    Return
    --------
        FWHM on four different direcions, i.e., x, y, xy, -xy.
    """
    seed_num = 2 * radius + 1
    frm = len(image)
    q_frm = int(frm / 4)
    x_center = np.where(image == image[q_frm:-q_frm, q_frm:-q_frm].max())[1][0]
    y_center = np.where(image == image[q_frm:-q_frm, q_frm:-q_frm].max())[0][0]
    x_n = np.asarray([image[y_center][x_center + i] for i in range(-radius, radius + 1)])
    y_n = np.asarray([image[y_center + i][x_center] for i in range(-radius, radius + 1)])
    xy_n = np.asarray([image[y_center + i][x_center + i] for i in range(-radius, radius + 1)])
    xy__n = np.asarray([image[y_center - i][x_center + i] for i in range(-radius, radius + 1)])
    from astropy.modeling import models, fitting
    g_init = models.Gaussian1D(amplitude=y_n.max(), mean=radius, stddev=1.5)
    fit_g = fitting.LevMarLSQFitter()
    g_x = fit_g(g_init, range(seed_num), x_n)
    g_y = fit_g(g_init, range(seed_num), y_n)
    g_xy = fit_g(g_init, range(seed_num), xy_n)
    g_xy_ = fit_g(g_init, range(seed_num), xy__n)
    from astropy.stats import gaussian_fwhm_to_sigma
    FWHM_ver = g_x.stddev.value / gaussian_fwhm_to_sigma
    FWHM_hor = g_y.stddev.value / gaussian_fwhm_to_sigma
    FWHM_xy = g_xy.stddev.value / gaussian_fwhm_to_sigma * np.sqrt(2.0)
    FWHM_xy_ = g_xy_.stddev.value / gaussian_fwhm_to_sigma * np.sqrt(2.0)
    return (FWHM_ver, FWHM_hor, FWHM_xy, FWHM_xy_)

def flux_in_region(image, region, mode='exact'):
    """
    Measure the total flux inside a 'region'.
    
    Parameter
    --------
        image: 
            2D array type image.
        
        region: 
            Region generated by pix_region.
        
        mode: 
            define the mode to measure flux, setting including. Based on region.to_mask()
                -'exact', 
                -'center'
            default is 'exact'.
        
    Returns
    --------
        Total flux value.
    """
    mask = region.to_mask(mode=mode)
    data = mask.cutout(image)
    tot_flux = np.sum(mask.data * data)
    return tot_flux
from galight.tools.cutout_tools import pix_region

def flux_profile(image, center, radius=35, start_p=1.5, grids=20, x_gridspace=None, if_plot=False, fits_plot=False, mask_image=None, q=None, theta=None):
    """
    Obtain the flux profile of a 2D image, region at the center position.
    
    Parameters
    --------
        image: 
            A 2-D array image.
            
        center: 
            Center point of the profile.
            
        radius: 
            The radius of the profile edge, default = 35.
            
        grids: 
            The Number of points to sample the flux, default = 20.
            
        if_plot: 
            If plot the profile.
            
        fits_plot: 
            If plot the fits file with the regions.
            
        mask_list: 
            A list of reg filenames used to generate a mask.
        
    Returns
    --------
        1. A 1-D array of the tot_flux value of each 'grids' in the profile sampled radius. 
        2. The grids of each pixel radius.
        3. The region file for each radius.
    """
    if x_gridspace == None:
        r_grids = (np.linspace(0, 1, grids + 1) * radius)[1:]
        diff = start_p - r_grids[0]
        r_grids += diff
    elif x_gridspace == 'log':
        r_grids = (np.logspace(-2, 0, grids + 1) * radius)[1:]
        diff = start_p - r_grids[0]
        r_grids += diff
    r_flux = np.empty(grids)
    regions = []
    mask = np.ones(image.shape)
    if mask_image is not None:
        mask = mask_image * mask
    for i in range(len(r_grids)):
        region = pix_region(center, r_grids[i], q=q, theta=theta)
        r_flux[i] = flux_in_region(image * mask, region)
        regions.append(region)
    if fits_plot == True:
        ax = plt.subplot(1, 1, 1)
        cax = ax.imshow(image * mask, norm=LogNorm(), origin='lower')
        for i in range(grids):
            ax.add_patch(regions[i].as_artist(facecolor='none', edgecolor='orange'))
        plt.colorbar(cax)
        plt.show()
    if if_plot == True:
        minorLocator = AutoMinorLocator()
        fig, ax = plt.subplots()
        plt.plot(r_grids, r_flux, 'x-')
        ax.xaxis.set_minor_locator(minorLocator)
        plt.tick_params(which='both', width=2)
        plt.tick_params(which='major', length=7)
        plt.tick_params(which='minor', length=4, color='r')
        plt.grid()
        ax.set_ylabel('Total Flux')
        ax.set_xlabel('Pixels')
        if x_gridspace == 'log':
            ax.set_xscale('log')
            plt.xlim(start_p * 0.7)
        plt.grid(which='minor')
        plt.show()
    return (r_flux, r_grids, regions)

def SB_profile(image, center, radius=35, start_p=1.5, grids=20, x_gridspace=None, if_plot=False, fits_plot=False, if_annuli=False, mask_image=None, q=None, theta=None):
    """
    Derive the SB profile of one image start at the center.
    
    Parameters
    --------
        image: 
            2-D array image.
            
        center: 
            The center point of the profile.
            
        radius: 
            The radius of the profile favourable with default equals to 35.
            
        grids: 
            The number of points to sample the flux with default equals to 20.
            
        if_plot: 
            if plot the profile.
            
        fits_plot: 
            if plot the fits file with the regions.
            
        if_annuli: 
            if False: The overall surface brightness with a circle. True, return annuli surface brightness between i and i-1 cirle.
            
        mask_image: 
            if is not None, will use this image as mask.
            
    Returns
    --------
        A 1-D array of the SB value of each 'grids' in the profile with the sampled radius.
    """
    mask = np.ones(image.shape)
    if mask_image is not None:
        mask = mask * mask_image
    r_flux, r_grids, regions = flux_profile(image * mask, center, radius=radius, start_p=start_p, grids=grids, x_gridspace=x_gridspace, if_plot=False, fits_plot=False, q=q, theta=theta)
    region_size = np.zeros([len(r_flux)])
    for i in range(len(r_flux)):
        circle = regions[i].to_mask(mode='exact')
        circle_mask = circle.cutout(mask)
        region_size[i] = (circle.data * circle_mask).sum()
    if if_annuli == False:
        r_SB = r_flux / region_size
    elif if_annuli == True:
        r_SB = np.zeros_like(r_flux)
        r_SB[0] = r_flux[0] / region_size[0]
        r_SB[1:] = (r_flux[1:] - r_flux[:-1]) / (region_size[1:] - region_size[:-1])
    if fits_plot == True:
        ax = plt.subplot(1, 1, 1)
        cax = ax.imshow(image * mask, norm=LogNorm(), origin='lower')
        for i in range(grids):
            ax.add_patch(regions[i].as_artist(facecolor='none', edgecolor='orange'))
        plt.colorbar(cax)
        plt.show()
    if if_plot == True:
        minorLocator = AutoMinorLocator()
        fig, ax = plt.subplots()
        plt.plot(r_grids, r_SB, 'x-')
        ax.xaxis.set_minor_locator(minorLocator)
        plt.tick_params(which='both', width=2)
        plt.tick_params(which='major', length=7)
        plt.tick_params(which='minor', length=4, color='r')
        plt.grid()
        ax.set_ylabel('Surface Brightness')
        ax.set_xlabel('Pixels')
        if x_gridspace == 'log':
            ax.set_xscale('log')
            plt.xlim(start_p * 0.7)
        plt.grid(which='minor')
        plt.show()
    return (r_SB, r_grids)

def profiles_compare(prf_list, prf_name_list=None, x_gridspace=None, radius=6, grids=20, norm_pix=3, if_annuli=False, y_log=False, scale_list=None):
    """
    Compare the SB profile between different images. 
    
    Parameter
    --------
        prf_list: 
            a list of image profiles.
            
        prf_name_list: 
            a list of name for each profiles.
        norm_pix: 
            The x-position (i.e. pixel) to norm the profiles.
        scale_list: 
            a list for the scaled value for the resultion, default as scale as 1 (set by None), i.e. same resolution.
        
    Return
    --------
        The plot of SB comparison.
    """
    if x_gridspace == None:
        radius = radius
    elif x_gridspace == 'log':
        radius = len(prf_list[1]) / 2
    if scale_list == None:
        scale_list = [1] * len(prf_list)
    minorLocator = AutoMinorLocator()
    fig, ax = plt.subplots(figsize=(10, 7))
    prf_NO = len(prf_list)
    if prf_name_list == None:
        prf_name_list = ['Profile-{0}'.format(i) for i in range(len(prf_list))]
    if len(prf_name_list) != len(prf_list):
        raise ValueError('The profile name is not in right length')
    for i in range(prf_NO):
        b_c = int(len(prf_list[i]) / 2)
        b_r = int(len(prf_list[i]) / 6)
        center = np.reshape(np.asarray(np.where(prf_list[i] == prf_list[i][b_c - b_r:b_c + b_r, b_c - b_r:b_c + b_r].max())), 2)[::-1]
        scale = scale_list[i]
        r_SB, r_grids = SB_profile(prf_list[i], center, radius=radius * scale, grids=grids, x_gridspace=x_gridspace, if_annuli=if_annuli)
        if isinstance(norm_pix, int) or isinstance(norm_pix, float):
            count = r_grids <= norm_pix * scale
            idx = count.sum() - 1
            r_SB /= r_SB[idx]
        r_grids /= scale
        if y_log == False:
            plt.plot(r_grids, r_SB, 'x-', label=prf_name_list[i])
        elif y_log == True:
            plt.plot(r_grids, np.log10(r_SB), 'x-', label=prf_name_list[i])
    ax.xaxis.set_minor_locator(minorLocator)
    plt.tick_params(which='both', width=2)
    plt.tick_params(which='major', length=7)
    plt.tick_params(which='minor', length=4, color='r')
    plt.grid()
    ax.set_ylabel('Scaled Surface Brightness', fontsize=20)
    ax.set_xlabel('Pixels', fontsize=20)
    if x_gridspace == 'log':
        ax.set_xscale('log')
    plt.grid(which='minor')
    plt.legend(prop={'size': 15}, ncol=2)
    plt.tick_params(labelsize=20)
    plt.show()
    return fig

def measure_bkg(img, if_plot=False, nsigma=2, npixels=25, dilate_size=11):
    """
    Estimate the 2D background of a image, based on photutils.Background2D, with SExtractorBackground.
    Checkout: https://photutils.readthedocs.io/en/stable/background.html
    
    Parameter
    --------
        parameters (including nsigma, npixels and dilate_size) will be passed to photutils.make_source_mask()
        
    Return
    --------
        A 2D array type of the background light.
    """
    print('Estimating the background light ... ... ...')
    from astropy.stats import SigmaClip
    from photutils import Background2D, SExtractorBackground
    try:
        sigma_clip = SigmaClip(sigma=3.0, maxiters=10)
    except TypeError:
        sigma_clip = SigmaClip(sigma=3.0, iters=10)
    bkg_estimator = SExtractorBackground()
    if version.parse(photutils.__version__) > version.parse('0.7'):
        mask_0 = make_source_mask(img, nsigma=nsigma, npixels=npixels, dilate_size=dilate_size)
    else:
        mask_0 = make_source_mask(img, snr=nsigma, npixels=npixels, dilate_size=dilate_size)
    mask_1 = np.isnan(img)
    mask_2 = img == 0
    mask = mask_0 + mask_1 + mask_2
    box_s = int(len(img) / 40)
    if box_s < 10:
        box_s = 10
    bkg = Background2D(img, (box_s, box_s), filter_size=(3, 3), sigma_clip=sigma_clip, bkg_estimator=bkg_estimator, mask=mask)
    fig = plt.figure(figsize=(15, 15))
    ax = fig.add_subplot(1, 1, 1)
    ax.imshow(img, norm=LogNorm(), origin='lower')
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    if if_plot:
        plt.show()
    else:
        plt.close()
    fig = plt.figure(figsize=(15, 15))
    ax = fig.add_subplot(1, 1, 1)
    ax.imshow(mask, origin='lower')
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    if if_plot:
        plt.show()
    else:
        plt.close()
    bkg_light = bkg.background * ~mask_1
    fig = plt.figure(figsize=(15, 15))
    ax = fig.add_subplot(1, 1, 1)
    ax.imshow(bkg_light, origin='lower', cmap='Greys_r')
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    if if_plot:
        plt.show()
    else:
        plt.close()
    return bkg_light

def string_find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ''

def cr_mask(image, filename='test_circle.reg'):
    """
    The creat a mask using a DS9 .reg file. The pixels in the region are 0, ouside ones are 1.
    
    Parameter
    --------
        image: 
            A 2D array image as a template frame.
            
        filename: 
            Full name of the region file.
        
    Return
    --------
        A image.shape array. Pixels in the region is 0, otherwise 1.
    """
    with open(filename, 'r') as input_file:
        reg_string = input_file.read().replace('\n', '')
    if 'physicalcircle' in reg_string:
        abc = string_find_between(reg_string, '(', ')')
        reg_info = np.fromstring(abc, dtype=float, sep=',')
        center, radius = (reg_info[:2] - 1, reg_info[2])
        region = pix_region(center, radius)
        box = 1 - region.to_mask(mode='center').data
    elif 'physicalbox' in reg_string:
        abc = string_find_between(reg_string, '(', ')')
        reg_info = np.fromstring(abc, dtype=float, sep=',')
        center = reg_info[:2] - 1
        x_r, y_r = reg_info[2:4]
        box = np.zeros([np.int(x_r) + 1, np.int(y_r) + 1]).T
    else:
        print(reg_string)
        raise ValueError('The input reg is un-defined yet')
    frame_size = image.shape
    box_size = box.shape
    x_edge = np.int(center[1] - box_size[0] / 2)
    y_edge = np.int(center[0] - box_size[1] / 2)
    mask = np.ones(frame_size)
    mask_box_part = mask[x_edge:x_edge + box_size[0], y_edge:y_edge + box_size[1]]
    mask_box_part *= box
    return mask

def image_moments(image, sexseg, pflag, plot=False):
    """
    Compute galaxy moments from galaxy pixels in [image]. The target galaxy's flag in the segmentation image [sexseg] should be [pflag]. All other source flags are irrelevant. The sky pixel flag should be 0. The moments can be computed for all flagged sources in an image iteratively for each [pflag]. Returns dictionary of image moments.
    
    References: 
    
    http://raphael.candelier.fr/?blog=Image%20Moments
    
    Image Moments-based Structuring and Tracking of Objects. L. Rocha, L. Velho and P.C.P. Calvalho (2002). URL=http://sibgrapi.sid.inpe.br/col/sid.inpe.br/banon/2002/10.23.11.34/doc/35.pdf
    """
    mask = sexseg == pflag
    y, x = np.where(mask)
    intensities = image[tuple([y, x])]
    M = np.sum(intensities)
    xbar = np.sum(x * intensities) / M
    ybar = np.sum(y * intensities) / M
    x = x - xbar
    y = y - ybar
    Mxx = np.sum(x ** 2 * intensities) / M
    Myy = np.sum(y ** 2 * intensities) / M
    Mxy = np.sum(x * y * intensities) / M
    Mrr = abs(np.sum(np.sqrt(x ** 2 + y ** 2) * intensities) / M)
    a = 2 * np.sqrt(abs(2 * (Mxx + Myy + np.sqrt(4 * Mxy ** 2 + (Mxx - Myy) ** 2))))
    b = 2 * np.sqrt(abs(2 * (Mxx + Myy - np.sqrt(4 * Mxy ** 2 + (Mxx - Myy) ** 2))))
    phi_deg = 0.5 * np.arctan(2 * Mxy / (Mxx - Myy)) * 180 / np.pi + (Mxx < Myy) * 90.0
    if plot:
        import matplotlib.pyplot as plt
        _fig, _ax = plt.subplots(figsize=(5, 5))
        from matplotlib.patches import Ellipse
        _ax.imshow(image, vmin=-0.001, vmax=0.001, origin='lower')
        _ax.scatter(xbar, ybar, s=10)
        e = Ellipse(xy=[xbar, ybar], width=Mrr, height=Mrr * b / a, edgecolor='red', facecolor='None', alpha=1.0, angle=phi_deg, transform=_ax.transData)
        _ax.add_artist(e)
    return {'M00': M, 'X': xbar, 'Y': ybar, 'Mxx': Mxx, 'Myy': Myy, 'Mxy': Mxy, 'Mrr': Mrr, 'a': a, 'b': b, 'q': b / a, 'phi_deg': phi_deg}

def detect_obj(image, detect_tool='phot', exp_sz=1.2, if_plot=False, auto_sort_center=True, nsigma=2.8, npixels=15, contrast=0.001, nlevels=25, use_moments=True, thresh=2.8, err=None, mask=None, minarea=5, filter_kernel=None, filter_type='matched', deblend_nthresh=32, deblend_cont=0.005, clean=True, clean_param=1.0):
    """
    Define the apeatures for all the objects in the image.
    
    Parameter
    --------
        img : 2-D array type image.
            The input image
    
        exp_sz : float.
            The level to expand the mask region.
    
        nsigma : float.
            The number of standard deviations per pixel above the
            ``background`` for which to consider a pixel as possibly being
            part of a source.
        
        npixels: int.
            The number of connected pixels, each greater than ``threshold``,
            that an object must have to be detected.  ``npixels`` must be a
            positive integer.
        
        if_plot: bool.
            If ture, plot the detection figure.    
        
    Return
    --------
        A list of photutils defined apeatures that cover the detected objects.
    """
    from photutils import EllipticalAperture
    apertures = []
    from photutils import detect_threshold
    if detect_tool == 'phot':
        from astropy.stats import gaussian_fwhm_to_sigma
        from astropy.convolution import Gaussian2DKernel
        from photutils import detect_sources, deblend_sources
        from photutils.segmentation import SourceCatalog
        if version.parse(photutils.__version__) > version.parse('0.7'):
            threshold = detect_threshold(image, nsigma=nsigma)
        else:
            threshold = detect_threshold(image, snr=nsigma)
        sigma = 3.0 * gaussian_fwhm_to_sigma
        kernel = Gaussian2DKernel(sigma, x_size=3, y_size=3)
        kernel.normalize()
        if version.parse(photutils.__version__) >= version.parse('1.2.0'):
            segm = detect_sources(image, threshold, npixels=npixels, kernel=kernel)
            segm_deblend = deblend_sources(image, segm, npixels=npixels, kernel=kernel, nlevels=nlevels, contrast=contrast)
        else:
            segm = detect_sources(image, threshold, npixels=npixels, filter_kernel=kernel)
            segm_deblend = deblend_sources(image, segm, npixels=npixels, filter_kernel=kernel, nlevels=nlevels, contrast=contrast)
        cat = SourceCatalog(image, segm_deblend)
        tbl = cat.to_table()
        segm_deblend_size = segm_deblend.areas
        for obj in cat:
            size = segm_deblend_size[obj.label - 1]
            position = (obj.xcentroid, obj.ycentroid)
            a_o = obj.semimajor_sigma.value
            b_o = obj.semiminor_sigma.value
            size_o = np.pi * a_o * b_o
            r = np.sqrt(size / size_o) * exp_sz
            a, b = (a_o * r, b_o * r)
            if version.parse(photutils.__version__) > version.parse('0.7'):
                theta = obj.orientation.value / 180 * np.pi
            else:
                theta = obj.orientation.value
            apertures.append(EllipticalAperture(position, a, b, theta=theta))
    elif detect_tool == 'sep':
        import sep
        data = image
        data = data.copy(order='C')
        if err is None:
            err = detect_threshold(image, nsigma=1.5)
        try:
            objects, segm_deblend = sep.extract(data, thresh=thresh, err=err.copy(order='C'), mask=mask, minarea=minarea, filter_kernel=filter_kernel, filter_type=filter_type, deblend_nthresh=deblend_nthresh, deblend_cont=deblend_cont, clean=clean, clean_param=clean_param, segmentation_map=True)
        except:
            data = data.byteswap().newbyteorder()
            objects, segm_deblend = sep.extract(data, thresh=thresh, err=err.copy(order='C'), mask=mask, minarea=minarea, filter_kernel=filter_kernel, filter_type=filter_type, deblend_nthresh=deblend_nthresh, deblend_cont=deblend_cont, clean=clean, clean_param=clean_param, segmentation_map=True)
        for i in range(len(objects)):
            position = (objects['x'][i], objects['y'][i])
            a, b = (np.sqrt(exp_sz * 6) * objects['a'][i], np.sqrt(exp_sz * 6) * objects['b'][i])
            theta = objects['theta'][i]
            apertures.append(EllipticalAperture(position, a, b, theta=theta))
    if auto_sort_center == True:
        center = np.array([len(image) / 2, len(image) / 2])
        dis_sq = [np.sum((apertures[i].positions - center) ** 2) for i in range(len(apertures))]
        dis_sq = np.array(dis_sq)
        c_order = dis_sq.argsort()
        apertures = [apertures[c_idx] for c_idx in c_order]
        _segm_deblend = np.zeros_like(segm_deblend)
        if detect_tool == 'phot':
            tbl['label'] = tbl['label'] - 1
            t_order = [None] * len(c_order)
            for i in c_order:
                t_order[c_order[i]] = i
            tbl['label'] = t_order
        for i in range(len(apertures)):
            _segm_deblend += (segm_deblend == c_order[i] + 1) * (i + 1)
        segm_deblend = _segm_deblend
    try:
        segm_deblend = np.array(segm_deblend.data)
    except:
        segm_deblend = np.array(segm_deblend)
    mask_apertures = copy.deepcopy(apertures)
    if use_moments == True:
        for i in range(np.max(segm_deblend)):
            moments = image_moments(image, segm_deblend, i + 1)
            apertures[i].positions = [moments['X'], moments['Y']]
            apertures[i].a = moments['Mrr']
            apertures[i].b = apertures[i].a * moments['q']
            apertures[i].theta = moments['phi_deg'] * np.pi / 180
    if if_plot == True:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 10))
        vmin = 0.001
        vmax = image.max()
        ax1.imshow(image, origin='lower', cmap=my_cmap, norm=LogNorm(vmin=vmin, vmax=vmax))
        ax1.set_title('Data', fontsize=25)
        ax1.tick_params(labelsize=15)
        ax2.imshow(segm_deblend, origin='lower')
        for i in range(len(apertures)):
            plt_xi, plt_yi = apertures[i].positions
            ax2.text(plt_xi, plt_yi, '{0}'.format(i), fontsize=25, bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 1})
        for i in range(len(apertures)):
            aperture = apertures[i]
            if version.parse(photutils.__version__) > version.parse('0.7'):
                aperture.plot(color='white', lw=1.5, axes=ax1)
                aperture.plot(color='white', lw=1.5, axes=ax2)
            else:
                aperture.plot(color='white', lw=1.5, ax=ax1)
                aperture.plot(color='white', lw=1.5, ax=ax2)
        ax2.set_title('Segmentation Image', fontsize=25)
        ax2.tick_params(labelsize=15)
        plt.show()
    return (apertures, segm_deblend, mask_apertures, tbl)

def sort_apertures(image, apertures):
    """
    Automaticlly sort the apertures based on the positions related to the center.
    """
    center = np.array([len(image) / 2, len(image) / 2])
    dis_sq = [np.sum((apertures[i].positions - center) ** 2) for i in range(len(apertures))]
    dis_sq = np.array(dis_sq)
    c_idx = np.where(dis_sq == dis_sq.min())[0][0]
    apertures = [apertures[c_idx]] + [apertures[i] for i in range(len(apertures)) if i != c_idx]
    return apertures

def mask_obj(image, apertures, if_plot=False, sum_mask=False):
    """
    Automaticlly generate a list of masked based on the input apertures.
    """
    from regions import PixCoord, EllipsePixelRegion
    from astropy.coordinates import Angle
    masks = []
    for i in range(len(apertures)):
        aperture = apertures[i]
        if isinstance(apertures[0].positions[0], np.ndarray):
            x, y = aperture.positions[0]
        elif isinstance(apertures[0].positions[0], float):
            x, y = aperture.positions
        center = PixCoord(x=x, y=y)
        theta = Angle(aperture.theta / np.pi * 180.0, 'deg')
        reg = EllipsePixelRegion(center=center, width=aperture.a * 2, height=aperture.b * 2, angle=theta)
        patch = reg.as_artist(facecolor='none', edgecolor='red', lw=2)
        mask_set = reg.to_mask(mode='center')
        mask = mask_set.to_image((len(image), len(image)))
        mask = 1 - mask
        if if_plot:
            print('plot mask for object {0}:'.format(i))
            fig, axi = plt.subplots(1, 1, figsize=None)
            axi.add_patch(patch)
            axi.imshow(mask, origin='lower')
            plt.show()
        masks.append(mask)
    if sum_mask == True:
        mask_ = np.ones_like(image)
        for i in range(len(masks)):
            mask_ = mask_ * masks[i]
        masks = mask_
    return masks

def esti_bgkstd(image, nsigma=2, exp_sz=1.5, npixels=15, if_plot=False):
    """
    Estimate the value of the background rms, by first block all the light and measure empty regions.
    """
    apertures, _, _, _ = detect_obj(image, nsigma=nsigma, exp_sz=exp_sz, npixels=npixels, if_plot=False, use_moments=False)
    mask_list = mask_obj(image, apertures, if_plot=False)
    mask = np.ones_like(image)
    for i in range(len(mask_list)):
        mask *= mask_list[i]
    image_mask = image * mask
    stdd = np.std(image_mask[image_mask != 0])
    if if_plot == True:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 6))
        ax1.imshow(image_mask, origin='lower', cmap=my_cmap, norm=LogNorm())
        ax1.set_title('pixels used to estimate bkg stdd', fontsize=20)
        ax1.tick_params(labelsize=15)
        values = ax2.hist(image_mask[image_mask != 0])
        ax2.plot(np.zeros(5) + np.median(image_mask[image_mask != 0]), np.linspace(0, values[0].max(), num=5), 'k--', linewidth=4)
        ax2.set_title('pixel value hist and med-point (mid = {0:.4f}).'.format(np.median(image_mask[image_mask != 0])), fontsize=20)
        ax2.tick_params(labelsize=15)
    return stdd

def model_flux_cal(params_list, model_list=None, sersic_major_axis=None):
    """
    Calculate the flux of a Sersic (i.e., itergral to infinite) which is same defination as Galfit.
    
    Parameter
    --------
        params_list: 
            a list of (Sersic) Soure params defined by Lenstronomy.
            
        model_list: 
            a list of names of light profile model.
        
    Return
    --------
        The flux value of Sersic.
    """
    from lenstronomy.LightModel.light_model import LightModel
    if model_list is None:
        model_list = ['SERSIC_ELLIPSE'] * len(params_list)
    light = LightModel(model_list, sersic_major_axis=sersic_major_axis)
    flux = light.total_flux(params_list)
    return flux

def plot_data_apertures(image, apertures, if_plot=True):
    """
    Quickly make a image+aperture plot.
    """
    plt.figure(figsize=(8, 6))
    plt.title('Data and apertures sets')
    vmin = 0.001
    vmax = 2.1
    plt.imshow(image, origin='lower', cmap=my_cmap, norm=LogNorm(vmin=vmin, vmax=vmax))
    np.random.seed(seed=3)
    for i in range(len(apertures)):
        aperture = apertures[i]
        aperture.plot(color=(np.random.uniform(0, 1), np.random.uniform(0, 1), np.random.uniform(0, 1)), lw=3.5, label='aperture {0}'.format(i))
    plt.legend()
    if if_plot == True:
        plt.show()
    else:
        plt.close()

def plot_data_apertures_point(image, apertures, ps_center_list, savename=None, show_plot=True):
    """
    Quickly make a image+aperture+PS plot.
    """
    plt.figure(figsize=(8, 6))
    plt.title('Data and components used to fit', fontsize=25)
    vmin = 0.001
    vmax = image.max()
    plt.imshow(image, origin='lower', cmap=my_cmap, norm=LogNorm(vmin=vmin, vmax=vmax))
    np.random.seed(seed=4)
    for i in range(len(ps_center_list)):
        plt.scatter(ps_center_list[i][0], ps_center_list[i][1], color=(np.random.uniform(0, 1), np.random.uniform(0, 1), np.random.uniform(0, 1)), s=180, marker='.', label='PS {0}'.format(i))
    np.random.seed(seed=3)
    for i in range(len(apertures)):
        aperture = apertures[i]
        aperture.plot(color=(np.random.uniform(0, 1), np.random.uniform(0, 1), np.random.uniform(0, 1)), lw=3.5, label='comp {0}'.format(i))
    plt.legend(prop={'size': 15})
    plt.tick_params(labelsize=15)
    if savename is not None:
        plt.savefig(savename, bbox_inches='tight')
    if show_plot == True:
        plt.show()
    else:
        plt.close()

def twoD_Gaussian(box_size, amplitude, xo, yo, sigma_x, sigma_y, theta, offset):
    """
    Function to define a 2-D Gaussian
    
    Parameter
    --------
        amplitude: 
            amplitude of the 2D gaussian
            
        xo, yo: 
            x, y position
            
        sigma_x, sigma_y: 
            sigma on x, y
            
        theta: 
            orientation
            
        offset: 
            offset (baseline, i.e., background)
            
    Return
    --------
        A 2-D gaussian profile, but use ravel to strech into 1D
    Reference: https://stackoverflow.com/questions/21566379/fitting-a-2d-gaussian-function-using-scipy-optimize-curve-fit-valueerror-and-m
    """
    x = np.linspace(0, box_size - 1, box_size)
    y = np.linspace(0, box_size - 1, box_size)
    x, y = np.meshgrid(x, y)
    xo = float(xo)
    yo = float(yo)
    a = np.cos(theta) ** 2 / (2 * sigma_x ** 2) + np.sin(theta) ** 2 / (2 * sigma_y ** 2)
    b = -np.sin(2 * theta) / (4 * sigma_x ** 2) + np.sin(2 * theta) / (4 * sigma_y ** 2)
    c = np.sin(theta) ** 2 / (2 * sigma_x ** 2) + np.cos(theta) ** 2 / (2 * sigma_y ** 2)
    g = offset + amplitude * np.exp(-(a * (x - xo) ** 2 + 2 * b * (x - xo) * (y - yo) + c * (y - yo) ** 2))
    return g.ravel()

def fit_data_twoD_Gaussian(data, popt_ini=None, if_plot=False):
    """
    Fit the data as twoD_Gaussian() and return parameters
    
    Parameter
    --------
        data: 
            the data should be put in the center.
            
    Return
    --------
        Parameters in twoD_Gaussian, i.e., amplitude, xo, yo, sigma_x, sigma_y, theta, offset
    """
    import scipy.optimize as opt
    if popt_ini == None:
        popt_ini = (data.max(), len(data) / 2, len(data) / 2, 2, 2, 0, 0.1)
    box_size = len(data)
    popt, pcov = opt.curve_fit(twoD_Gaussian, box_size, data.ravel(), p0=popt_ini)
    popt[3], popt[4] = (abs(popt[3]), abs(popt[4]))
    data_fitted = twoD_Gaussian(box_size, *popt)
    if if_plot == True:
        fig, ax = plt.subplots(1, 1)
        ax.imshow(data, cmap=my_cmap, origin='bottom')
        x = np.linspace(0, box_size - 1, box_size)
        y = np.linspace(0, box_size - 1, box_size)
        x, y = np.meshgrid(x, y)
        ax.contour(x, y, data_fitted.reshape(len(data), len(data)), 8, colors='w')
        plt.show()
    return popt

def oneD_gaussian(x, mean, amplitude, standard_deviation):
    return amplitude * np.exp(-((x - mean) / standard_deviation) ** 2)

def fit_data_oneD_gaussian(data, ifplot=False):
    """
    Fit data as 1D gaussion
    """
    bin_heights, bin_borders = np.histogram(data, bins='auto')
    bin_widths = np.diff(bin_borders)
    bin_centers = bin_borders[:-1] + bin_widths / 2
    plt.bar(bin_centers, bin_heights, width=bin_widths, label='histogram')
    from scipy.optimize import curve_fit
    popt, pcov = curve_fit(oneD_gaussian, bin_centers, bin_heights, p0=[0.0, bin_heights.max(), 0.01])
    x_interval_for_fit = np.linspace(bin_borders[0], bin_borders[-1], 10000)
    gauss_grid = oneD_gaussian(x_interval_for_fit, *popt)
    plt.plot(x_interval_for_fit, gauss_grid, label='fit', c='red')
    fit_center_idx = np.where(gauss_grid == gauss_grid.max())[0][0]
    line = np.linspace(0, 10000, 10)
    peak_loc = x_interval_for_fit[fit_center_idx]
    plt.plot(peak_loc * np.ones_like(line), line, 'black')
    plt.plot(peak_loc * np.ones_like(line) + popt[2], line, 'black')
    plt.plot(peak_loc * np.ones_like(line) - popt[2], line, 'black')
    plt.ylim((0, bin_heights.max() * 5.0 / 4.0))
    plt.legend()
    if ifplot == True:
        plt.show()
    else:
        plt.close()
    return (peak_loc, popt[2])