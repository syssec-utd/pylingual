from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pyspedas.analysis.time_clip import time_clip as tclip
from pytplot import netcdf_to_tplot
from .config import CONFIG

def loadr(trange=['2023-01-01', '2032-01-02'], probe='16', instrument='mag', datatype='1min', prefix='', suffix='', downloadonly=False, no_update=False, time_clip=False):
    """
    This function loads GOES-R L2 data (GOES-16, GOES-17, GOES-18)

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str/int or list of strs/ints
            GOES spacecraft #, e.g., probe=16

        instrument: str
            name of the instrument (euvs, xrs, mag, mpsh, sgps)

        datatype: str
            Data resolution, default is '1min'
            Valid options: low (avg), hi (full), and various other options depending on instrument

        prefix: str
            The tplot variable names will be given this prefix.
            By default, no prefix is added.
            If 'probename' then the name will be used, for example 'g16_'.

        suffix: str
            The tplot variable names will be given this suffix.
            By default, no suffix is added.

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into
            tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    -------
        List of tplot variables created. Or list of filenames downloaded.

    Notes
    -----
    Information: https://www.ngdc.noaa.gov/stp/satellite/goes-r.html
    Data: https://data.ngdc.noaa.gov/platforms/solar-space-observing-satellites/goes/
    Path: goesNN/l2/data/instrument/YYYY/MM/file.nc
    Time variable: 'time', seconds since 2000-01-01 12:00:00

    GOES-EAST (GOES-16, 2017-)
    GOES-WEST (GOES-17, 2018-2022; GOES-18, 2023-)

    Instruments:    euvs (hi, full, 1min, euvs-l2-avg1m_science/2021/05/sci_euvs-l2-avg1m_g16_d20210530_v1-0-3.nc)
                    euvs (low, avg, 1day, euvs-l2-avg1d_science/2021/06/sci_euvs-l2-avg1d_g16_d20210630_v1-0-3.nc)
                    xrs  (hi, full, 1sec, xrsf-l2-flx1s_science/2022/08/sci_xrsf-l2-flx1s_g16_d20220830_v2-1-0.nc)
                    xrs  (low, avg, 1min, xrsf-l2-avg1m_science/2021/06/sci_xrsf-l2-avg1m_g16_d20210630_v2-1-0.nc)
                    mag  (hi, full, 0.1sec, magn-l2-hires/2021/06/dn_magn-l2-hires_g16_d20210629_v1-0-1.nc)
                    mag  (low, avg, 1min, magn-l2-avg1m/2022/12/dn_magn-l2-avg1m_g16_d20221230_v2-0-2.nc)
                    mpsh (hi, full, 1min, mpsh-l2-avg1m/2022/12/sci_mpsh-l2-avg1m_g16_d20221230_v2-0-0.nc)
                    mpsh (low, avg, 5min, mpsh-l2-avg5m/2022/12/sci_mpsh-l2-avg5m_g16_d20221230_v2-0-0.nc)
                    sgps (hi, full, 1min, sgps-l2-avg1m/2022/12/sci_sgps-l2-avg1m_g17_d20221230_v3-0-0.nc)
                    sgps (low, avg, 5min, sgps-l2-avg5m/2022/12/sci_sgps-l2-avg5m_g17_d20221230_v3-0-0.nc)

    EXIS (Extreme Ultraviolet and X-ray Sensors), EUVS and XRS
    EUVS: Spectral line irradiances, the Mg II index, and proxy spectra from the EXIS Extreme Ultraviolet Sensor (EUVS)
    EUVS: Daily averages of spectral line irradiances, the Mg II index, and proxy spectra
    XRS: 1-minute averages of XRS measurements
    XRS: High cadence measurements from the EXIS X-Ray Sensor (XRS)
    MAG (Magnetometer)
    MAG: Full resolution magnetic field readings in different coordinate systems
    MAG: Averages of 10 Hz magnetometer field readings
    SEISS (Space Environment In Situ Suite): 1-min and 5-min averages for the Magnetospheric Particle Sensors (MPS-HI and MPS-LO)
            and for the Solar and Galactic Proton Sensor (SGPS)

    Wrappers:
        pyspedas.goes.euvs
        pyspedas.goes.xrs
        pyspedas.goes.mag
        pyspedas.goes.mpsh
        pyspedas.goes.sgps

    Example
    -------
        from pyspedas.goes import load
        trange = ['2023-01-01', '2023-01-02']
        load(trange=trange, probe='16', instrument='mag', datatype='1min', time_clip=True)

    """
    goes_path_dir = 'https://data.ngdc.noaa.gov/platforms/solar-space-observing-satellites/goes/'
    time_var = 'time'
    out_files = []
    tvars = []
    if not isinstance(probe, list):
        probe = [probe]
    for prb in probe:
        remote_path = 'goes' + str(prb) + '/l2/data/'
        if instrument == 'euvs':
            if datatype in ['full', 'hi', '1min', 'avg1m']:
                pathformat = [remote_path + 'euvs-l2-avg1m_science/%Y/%m/sci_euvs-l2-avg1m_g' + str(prb) + '_d%Y%m%d_v?-?-?.nc']
            else:
                pathformat = [remote_path + 'euvs-l2-avg1d_science/%Y/%m/sci_euvs-l2-avg1d_g' + str(prb) + '_d%Y%m%d_v?-?-?.nc']
        elif instrument == 'xrs':
            if datatype in ['full', 'hi', '1sec', 'flx1s']:
                pathformat = [remote_path + 'xrsf-l2-flx1s_science/%Y/%m/sci_xrsf-l2-flx1s_g' + str(prb) + '_d%Y%m%d_v?-?-?.nc']
            else:
                pathformat = [remote_path + 'xrsf-l2-avg1m_science/%Y/%m/sci_xrsf-l2-avg1m_g' + str(prb) + '_d%Y%m%d_v?-?-?.nc']
        elif instrument == 'mag':
            if datatype in ['full', 'hi', '0.1sec', 'hires']:
                pathformat = [remote_path + 'magn-l2-hires/%Y/%m/dn_magn-l2-hires_g' + str(prb) + '_d%Y%m%d_v?-?-?.nc']
            else:
                pathformat = [remote_path + 'magn-l2-avg1m/%Y/%m/dn_magn-l2-avg1m_g' + str(prb) + '_d%Y%m%d_v?-?-?.nc']
        elif instrument == 'mpsh':
            time_var = 'L2_SciData_TimeStamp'
            if datatype in ['full', 'hi', '1min', 'avg1m', '1m']:
                pathformat = [remote_path + 'mpsh-l2-avg1m/%Y/%m/sci_mpsh-l2-avg1m_g' + str(prb) + '_d%Y%m%d_v?-?-?.nc']
            else:
                pathformat = [remote_path + 'mpsh-l2-avg5m/%Y/%m/sci_mpsh-l2-avg5m_g' + str(prb) + '_d%Y%m%d_v?-?-?.nc']
        elif instrument == 'sgps':
            if datatype in ['full', 'hi', '1min', 'avg1m', '1m']:
                pathformat = [remote_path + 'sgps-l2-avg1m/%Y/%m/sci_sgps-l2-avg1m_g' + str(prb) + '_d%Y%m%d_v?-?-?.nc']
            else:
                pathformat = [remote_path + 'sgps-l2-avg5m/%Y/%m/sci_sgps-l2-avg5m_g' + str(prb) + '_d%Y%m%d_v?-?-?.nc']
        if not isinstance(pathformat, list):
            pathformat = [pathformat]
        remote_names = []
        for path in pathformat:
            remote_names.extend(dailynames(file_format=path, trange=trange))
        files = download(remote_file=remote_names, remote_path=goes_path_dir, local_path=CONFIG['local_data_dir'], no_download=no_update)
        if files is not None:
            for file in files:
                out_files.append(file)
        tvars_local = []
        if len(files) > 0 and downloadonly is False:
            if prefix == 'probename':
                prefix_local = 'g' + str(prb) + '_'
            else:
                prefix_local = prefix
            tvars_local = netcdf_to_tplot(files, prefix=prefix_local, suffix=suffix, merge=True, time=time_var)
        if len(tvars_local):
            tvars.extend(tvars_local)
    if downloadonly:
        out_files = sorted(out_files)
        return out_files
    if time_clip:
        for new_var in tvars:
            tclip(new_var, trange[0], trange[1], suffix='')
    return tvars

def load(trange=['2013-11-05', '2013-11-06'], probe='15', instrument='fgm', datatype='1min', prefix='', suffix='', downloadonly=False, no_update=False, time_clip=False):
    """
    This function loads GOES L2 data

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str/int or list of strs/ints
            GOES spacecraft #, e.g., probe=15

        instrument: str
            name of the instrument
            (for GOES 8-15: fgm, eps, epead, maged, magpd, hepad, xrs)
            (for GOES-R 16-18: euvs, xrs, mag, mpsh, sgps)

        datatype: str
            Data type; usually instrument resolution, depends on the instrument
            Default is 1min
            (valid for GOES 8-15: hi, low, full, avg, 1min, 5min)
            (valid for GOES-R 16-18: hi, low, full, avg, and other options)

        prefix: str
            The tplot variable names will be given this prefix.
            By default, no prefix is added.
            If 'probename' then the name will be used, for example g16.

        suffix: str
            The tplot variable names will be given this suffix.
            By default, no suffix is added.

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into
            tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    -------
        List of tplot variables created. Or list of filenames downloaded.

    Notes
    -----
    This function loads data from the GOES mission; this function is not meant
    to be called directly; instead, see the wrappers:
        pyspedas.goes.fgm
        pyspedas.goes.eps
        pyspedas.goes.epead
        pyspedas.goes.maged
        pyspedas.goes.magpd
        pyspedas.goes.hepad
        pyspedas.goes.xrs

    """
    if not isinstance(probe, list):
        probe = [probe]
    probe_r = []
    probe_s = []
    out_files_r = []
    out_files = []
    tvars_r = []
    tvars = []
    for prb in probe:
        if int(prb) > 15:
            probe_r.append(str(prb))
        else:
            probe_s.append(str(prb))
    if len(probe_r):
        tvars_r = loadr(trange=trange, probe=probe_r, instrument=instrument, datatype=datatype, prefix=prefix, suffix=suffix, downloadonly=downloadonly, no_update=no_update, time_clip=time_clip)
        if downloadonly:
            out_files_r = tvars_r
    for prb in probe_s:
        avg_path = 'avg/%Y/%m/goes' + str(prb) + '/netcdf/' + 'g' + str(prb)
        full_path = 'full/%Y/%m/goes' + str(prb) + '/netcdf/' + 'g' + str(prb)
        if instrument == 'fgm':
            if datatype == '512ms' or datatype == 'full':
                pathformat = full_path + '_magneto_512ms_%Y%m%d_%Y%m%d.nc'
            elif datatype == '5min':
                pathformat = avg_path + '_magneto_5m_%Y%m01_%Y%m??.nc'
            else:
                pathformat = avg_path + '_magneto_1m_%Y%m01_%Y%m??.nc'
        elif instrument == 'eps':
            if datatype == '1min' or datatype == 'full':
                pathformat = avg_path + '_eps_1m_%Y%m01_%Y%m??.nc'
            else:
                pathformat = avg_path + '_eps_5m_%Y%m01_%Y%m??.nc'
        elif instrument == 'epead':
            if datatype == '1min':
                pathformat = ['_epead_e13ew_1m_%Y%m01_%Y%m??.nc', '_epead_p17ew_1m_%Y%m01_%Y%m??.c', '_epead_a16ew_1m_%Y%m01_%Y%m??.nc']
                pathformat = [avg_path + s for s in pathformat]
            elif datatype == '5min' or datatype == 'low':
                pathformat = ['_epead_e13ew_5m_%Y%m01_%Y%m??.nc', '_epead_p17ew_5m_%Y%m01_%Y%m??.c', '_epead_a16ew_5m_%Y%m01_%Y%m??.nc']
                pathformat = [avg_path + s for s in pathformat]
            else:
                pathformat = ['_epead_a16e_32s_%Y%m%d_%Y%m%d.nc', '_epead_a16w_32s_%Y%m%d_%Y%m%d.nc', '_epead_e1ew_4s_%Y%m%d_%Y%m%d.nc', '_epead_e2ew_16s_%Y%m%d_%Y%m%d.nc', '_epead_e3ew_16s_%Y%m%d_%Y%m%d.nc', '_epead_p1ew_8s_%Y%m%d_%Y%m%d.nc', '_epead_p27e_32s_%Y%m%d_%Y%m%d.nc', '_epead_p27w_32s_%Y%m%d_%Y%m%d.nc']
                pathformat = [full_path + s for s in pathformat]
        elif instrument == 'maged':
            if datatype == '1min':
                pathformat = avg_path + '_maged_19me15_1m_%Y%m01_%Y%m??.nc'
            elif datatype == '5min' or datatype == 'low':
                pathformat = avg_path + '_maged_19me15_5m_%Y%m01_%Y%m??.nc'
            else:
                channels = ['me1', 'me2', 'me3', 'me4', 'me5']
                resolution = ['2', '2', '4', '16', '32']
                pathformat = []
                for idx, channel in enumerate(channels):
                    pathformat.append('_maged_19' + channel + '_' + resolution[idx] + 's_%Y%m%d_%Y%m%d.nc')
                pathformat = [full_path + s for s in pathformat]
        elif instrument == 'magpd':
            if datatype == '1min' or datatype == 'low':
                pathformat = avg_path + '_magpd_19mp15_1m_%Y%m01_%Y%m??.nc'
            else:
                channels = ['mp1', 'mp2', 'mp3', 'mp4', 'mp5']
                resolution = ['16', '16', '16', '32', '32']
                pathformat = []
                for idx, channel in enumerate(channels):
                    pathformat.append('_magpd_19' + channel + '_' + resolution[idx] + 's_%Y%m%d_%Y%m%d.nc')
                pathformat = [full_path + s for s in pathformat]
        elif instrument == 'hepad':
            if datatype == '1min':
                pathformat = ['_hepad_ap_1m_%Y%m01_%Y%m??.nc', '_hepad_s15_1m_%Y%m01_%Y%m??.nc']
                pathformat = [avg_path + s for s in pathformat]
            elif datatype == '5min' or datatype == 'low':
                pathformat = ['_hepad_ap_5m_%Y%m01_%Y%m??.nc', '_hepad_s15_5m_%Y%m01_%Y%m??.nc']
                pathformat = [avg_path + s for s in pathformat]
            else:
                pathformat = ['_hepad_ap_32s_%Y%m%d_%Y%m%d.nc', '_hepad_s15_4s_%Y%m%d_%Y%m%d.nc']
                pathformat = [full_path + s for s in pathformat]
        elif instrument == 'xrs':
            if datatype == '1min':
                pathformat = avg_path + '_xrs_1m_%Y%m01_%Y%m??.nc'
            elif datatype == '5min' or datatype == 'low':
                pathformat = avg_path + '_xrs_5m_%Y%m01_%Y%m??.nc'
            else:
                pathformat = ['_xrs_2s_%Y%m%d_%Y%m%d.nc', '_xrs_3s_%Y%m%d_%Y%m%d.nc']
                pathformat = [full_path + s for s in pathformat]
        if not isinstance(pathformat, list):
            pathformat = [pathformat]
        remote_names = []
        for path in pathformat:
            remote_names.extend(dailynames(file_format=path, trange=trange))
        files = download(remote_file=remote_names, remote_path=CONFIG['remote_data_dir'], local_path=CONFIG['local_data_dir'], no_download=no_update)
        if files is not None:
            for file in files:
                out_files.append(file)
        tvars_local = []
        if len(files) > 0 and downloadonly is False:
            if prefix == 'probename':
                prefix_local = 'g' + str(prb) + '_'
            else:
                prefix_local = prefix
            tvars_local = netcdf_to_tplot(files, prefix=prefix_local, suffix=suffix, merge=True, time='time_tag')
        if len(tvars_local) > 0:
            tvars.extend(tvars_local)
    if downloadonly:
        out_files.extend(out_files_r)
        out_files = sorted(out_files)
        return out_files
    if time_clip:
        for new_var in tvars:
            tclip(new_var, trange[0], trange[1], suffix='')
    if len(tvars_r):
        tvars.extend(tvars_r)
    return tvars