"""
Author: Kyle Koeller
Created: 11/08/2022
Last Edited: 03/08/2023

This program is meant to automatically do the data reduction of the raw images from the
Ball State University Observatory (BSUO) and SARA data. The new calibrated images are placed into a new folder as to
not overwrite the original images.
"""
from pathlib import Path
import time
import warnings
from astropy import wcs
from astropy.stats import mad_std
from astropy import units as u
import ccdproc as ccdp
import numpy as np
from astropy.nddata import CCDData
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore', category=wcs.FITSFixedWarning)
sigma_clip_low_thresh = None
sigma_clip_high_thresh = 3
sigclip = 5
rdnoise = 10.83 * u.electron
gain = 1.43 * u.electron / u.adu
overwrite = True
mem_limit = 450000000.0

def main():
    """
    This function calls all other functions in order of the calibration.

    :return: outputs all calibration images into a new reduced folder designated by the user.
    """
    path = input("Please enter a file pathway (i.e. C:\\folder1\\folder2) to where the raw images are or type the word 'Close' to leave: ")
    if path.lower() == 'close':
        exit()
    calibrated = input('Please enter a file pathway for a new calibrated folder to not overwrite the original images (): ')
    while True:
        try:
            images_path = Path(path)
            calibrated_data = Path(calibrated)
            break
        except FileNotFoundError:
            print('Files were not found. Please try again.\n')
            path = input('Please enter a file path or folder name (if this code is in the same main folder): ')
            calibrated = input('Please enter a name for a new calibrated folder to not overwrite the original images: ')
    calibrated_data.mkdir(exist_ok=True)
    files = ccdp.ImageFileCollection(images_path)
    zero, overscan_region, trim_region = bias(files, calibrated_data, path)
    master_dark = dark(files, zero, calibrated_data, overscan_region, trim_region)
    flat(files, zero, master_dark, calibrated_data, overscan_region, trim_region)
    science_images(files, calibrated_data, zero, master_dark, trim_region, overscan_region)

def reduce(ccd, overscan_region, trim_region, num, zero, combined_dark, good_flat):
    """
    This function takes the information for each section of the reduction process into a singular function for
    limits in duplication of the code.

    :param ccd: individual image
    :param overscan_region: the overscan region of the image
    :param trim_region: region of the image to trim
    :param num: tells the program what stage of the process it is in
    :param zero: master bias
    :param combined_dark: master dark
    :param good_flat: master flat
    :return: depends on the stage of process, but will return a final image for each process
    """
    if overscan_region.lower() == 'none':
        pass
    else:
        ccd = ccdp.subtract_overscan(ccd, fits_section=overscan_region, median=True, overscan_axis=1)
    ccd = ccdp.trim_image(ccd, fits_section=trim_region)
    new_ccd = ccdp.gain_correct(ccd, gain=gain)
    if num == 0:
        return new_ccd
    elif num == 1:
        sub_ccd = ccdp.subtract_bias(new_ccd, zero)
        return sub_ccd
    elif num == 2:
        sub_ccd = ccdp.subtract_bias(new_ccd, zero)
        final_ccd = ccdp.subtract_dark(sub_ccd, combined_dark, exposure_time='exptime', exposure_unit=u.second, scale=True)
        return final_ccd
    elif num == 3:
        sub_ccd = ccdp.subtract_bias(new_ccd, zero)
        reduced = ccdp.subtract_dark(sub_ccd, combined_dark, exposure_time='exptime', exposure_unit=u.second, scale=True)
        reduced = ccdp.flat_correct(ccd=reduced, flat=good_flat, min_value=1.0)
        return reduced

def bias(files, calibrated_data, path):
    """
    Calibrates the bias images

    :param path: the raw images folder path
    :param files: file location where all raw images are
    :param calibrated_data: file location where the new images go
    :return: the combined bias image and the trim and overscan regions
    """
    print('\nThe bias image that you enter next should be inside the FIRST folder that you entered above or this will crash.\n')
    image = input('Please enter the name of one of the bias images to be looked at for overscan and trim regions: ')
    cryo_path = Path(path)
    bias_1 = CCDData.read(cryo_path / image, unit='adu')
    print('\n\nFor the overscan region, [rows, columns], and if you want all the columns then you want would enter, \n[1234:5678, 1234:5678] and this would say rows between those values and all the columns. \nThis would also work if you wanted all the rows ([: , 1234:5678]).\n')
    bias_plot(bias_1)
    overscan_region = input("Please enter the overscan region you determined from the figure.\nExample '[2073:2115, :]' or if you do not have an overscan region enter 'None': ")
    trim_region = input("Please enter the trim region. Example '[20:2060, 12:2057]': ")
    print()
    print('\nStarting overscan on bias.\n')
    for ccd, file_name in files.ccds(imagetyp='BIAS', return_fname=True, ccd_kwargs={'unit': 'adu'}):
        new_ccd = reduce(ccd, overscan_region, trim_region, 0, zero=None, combined_dark=None, good_flat=None)
        list_of_words = file_name.split('-')
        new_fname = 'bias_o_{}.fits'.format(list_of_words[3])
        new_ccd.write(calibrated_data / new_fname, overwrite=overwrite)
        print('Finished overscan correction for ' + str(new_fname))
    print('\nFinished overscan correcting bias frames.')
    reduced_images = ccdp.ImageFileCollection(calibrated_data)
    calibrated_biases = reduced_images.files_filtered(imagetyp='BIAS', include_path=True)
    combined_bias = ccdp.combine(calibrated_biases, method='average', sigma_clip=True, sigma_clip_low_thresh=sigma_clip_low_thresh, sigma_clip_high_thresh=sigma_clip_high_thresh, sigma_clip_func=np.ma.median, signma_clip_dev_func=mad_std, mem_limit=450000000.0)
    combined_bias.meta['combined'] = True
    combined_bias.write(calibrated_data / 'zero.fits', overwrite=overwrite)
    print('\nFinished creating zero.fits\n')
    return (combined_bias, overscan_region, trim_region)

def bias_plot(ccd):
    """
    Plots the count values for row 1000 to find the overscan and trim regions

    :param ccd: bias image to be looked at
    :return: None
    """
    plt.figure(figsize=(10, 5))
    plt.plot(ccd.data[1000][:], label='Raw Bias')
    plt.grid()
    plt.axvline(x=2077, color='black', linewidth=2, linestyle='dashed', label='Suggested Start of Overscan')
    plt.legend()
    plt.ylim(750, 1250)
    plt.xlim(-50, 2130)
    plt.xlabel('pixel number')
    plt.ylabel('Counts')
    plt.title('Count Values for Row 1000')
    plt.show()

def dark(files, zero, calibrated_path, overscan_region, trim_region):
    """
    Calibrates the dark frames.

    :param files: file location of raw images
    :param zero: master bias image
    :param calibrated_path: file location for the new images
    :param trim_region: trim region for images
    :param overscan_region: overscan region for images
    :return: combined master dark
    """
    print('Starting dark calibration.\n')
    for ccd, file_name in files.ccds(imagetyp='DARK', ccd_kwargs={'unit': 'adu'}, return_fname=True):
        sub_ccd = reduce(ccd, overscan_region, trim_region, 1, zero, combined_dark=None, good_flat=None)
        list_of_words = file_name.split('-')
        new_fname = 'dark_o_b_{}.fits'.format(list_of_words[3])
        sub_ccd.write(calibrated_path / new_fname, overwrite=overwrite)
        print('Finished overscan correction and bias subtraction for ' + str(new_fname))
    print('\nFinished overscan correcting and bias subtracting all dark frames.')
    print('\nStarting combining dark frames.\n')
    time.sleep(10)
    reduced_images = ccdp.ImageFileCollection(calibrated_path)
    calibrated_darks = reduced_images.files_filtered(imagetyp='dark', include_path=True)
    combined_dark = ccdp.combine(calibrated_darks, method='average', sigma_clip=True, sigma_clip_low_thresh=sigma_clip_low_thresh, sigma_clip_high_thresh=sigma_clip_high_thresh, sigma_clip_func=np.ma.median, signma_clip_dev_func=mad_std, rdnoise=rdnoise, gain=gain, mem_limit=450000000.0)
    combined_dark.meta['combined'] = True
    combined_dark.write(calibrated_path / 'master_dark.fits', overwrite=overwrite)
    print('Finished creating a master dark.\n')
    return combined_dark

def flat(files, zero, combined_dark, calibrated_path, overscan_region, trim_region):
    """
    Calibrate flat images.

    :param files: file location for raw images
    :param zero: combined bias image
    :param combined_dark: combined bias image
    :param calibrated_path: file location for new images
    :param trim_region: trim region for images
    :param overscan_region: overscan region for images
    :return: master flat files in each filter
    """
    print('Starting flat calibration.\n')
    print()
    for ccd, file_name in files.ccds(imagetyp='FLAT', return_fname=True, ccd_kwargs={'unit': 'adu'}):
        final_ccd = reduce(ccd, overscan_region, trim_region, 2, zero, combined_dark, good_flat=None)
        list_of_words = file_name.split('-')
        new_fname = 'flat_o_b_d_{}{}.fits'.format(list_of_words[2], list_of_words[4])
        final_ccd.write(calibrated_path / new_fname, overwrite=overwrite)
        print('Finished overscan correction, bias subtraction, and dark subtraction for ' + str(new_fname))
    print('\nFinished overscan, bias subtracting, and dark subtracting of flat frames.\n')
    print('Starting flat combination.\n')
    time.sleep(10)
    ifc = ccdp.ImageFileCollection(calibrated_path)
    flat_filters = set((h['FILTER'] for h in ifc.headers(imagetyp='FLAT')))
    for filt in flat_filters:
        to_combine = ifc.files_filtered(imagetyp='flat', filter=filt, include_path=True)
        combined_flats = ccdp.combine(to_combine, method='average', sigma_clip_high_thresh=sigma_clip_high_thresh, sigma_clip_func=np.ma.median, signma_clip_dev_func=mad_std, rdnoise=rdnoise, gain=gain, mem_limit=450000000.0)
        combined_flats.meta['combined'] = True
        flat_file_name = 'master_flat_{}.fits'.format(filt.replace('Empty/', ''))
        combined_flats.write(calibrated_path / flat_file_name, overwrite=overwrite)
        print('Finished combining flat ' + str(flat_file_name))
    print('\nFinished creating the master flats by filter.\n')
    return combined_flats

def science_images(files, calibrated_data, zero, combined_dark, trim_region, overscan_region):
    all_reds = []
    science_imagetyp = 'LIGHT'
    flat_imagetyp = 'FLAT'
    ifc_reduced = ccdp.ImageFileCollection(calibrated_data)
    combined_flats = {ccd.header['filter']: ccd for ccd in ifc_reduced.ccds(imagetyp=flat_imagetyp, combined=True)}
    print('Starting reduction of science images.\n')
    for light, file_name in files.ccds(imagetyp=science_imagetyp, return_fname=True, ccd_kwargs={'unit': 'adu'}):
        good_flat = combined_flats[light.header['filter']]
        reduced = reduce(light, overscan_region, trim_region, 3, zero, combined_dark, good_flat)
        list_of_words = file_name.split('-')
        new_fname = '{}_o_b_d_f_{}_{}_{}.fits'.format(list_of_words[0], list_of_words[2], list_of_words[5], list_of_words[6].replace('.fts', ''))
        all_reds.append(reduced)
        reduced.write(calibrated_data / new_fname, overwrite=overwrite)
        print('Finished calibration of ' + str(new_fname))
    print('\nFinished calibrating all science images.')
if __name__ == '__main__':
    main()