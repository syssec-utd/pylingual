from operator import xor
import lal
import lalsimulation as lalsim
import numpy as np
from astropy import units as u
from . import parameter_conventions as pc
import warnings

def from_lal_value(val):
    """
    Read and return a value from LALDict

    Parameters
    ----------
    val : `lal.DictValues` value
        Output from a lal.DictValues

    Returns
    -------
    lal.Value'(val) :
    """
    ltype = lal.ValueGetType(val)
    if ltype == lal.CHAR_TYPE_CODE:
        size = lal.ValueGetSize(val)
        if size == 1:
            return lal.ValueGetCHAR(val)
        else:
            return lal.ValueGetString(val)
    if ltype == lal.I2_TYPE_CODE:
        return lal.ValueGetINT2(val)
    if ltype == lal.I4_TYPE_CODE:
        return lal.ValueGetINT4(val)
    if ltype == lal.I8_TYPE_CODE:
        return lal.ValueGetINT8(val)
    if ltype == lal.U2_TYPE_CODE:
        return lal.ValueGetUINT2(val)
    if ltype == lal.U4_TYPE_CODE:
        return lal.ValueGetUINT4(val)
    if ltype == lal.U8_TYPE_CODE:
        return lal.ValueGetUINT8(val)
    if ltype == lal.S_TYPE_CODE:
        return lal.ValueGetREAL4(val)
    if ltype == lal.D_TYPE_CODE:
        return lal.ValueGetREAL8(val)
    if ltype == lal.C_TYPE_CODE:
        return lal.ValueGetCOMPLEX8(val)
    if ltype == lal.Z_TYPE_CODE:
        return lal.ValueGetCOMPLEX16(val)
    else:
        raise TypeError('invalid lal typecode %d' % ltype)

def to_lal_dict(d):
    """
    Convert Python dictionary to LALDict object readble by LAL

    Parameters
    ----------
    d : `dict`
        Python dictionary of input parameters

    Returns
    -------
    ldict : `LALDict`
        LALDict object readable by LAL
    """
    if d is None:
        return None
    ldict = lal.CreateDict()
    for k, v in d.items():
        if k == 'ModeArray':
            lalsim.SimInspiralWaveformParamsInsertModeArrayFromModeString(ldict, v)
        elif k == 'ModeArrayJframe':
            lalsim.SimInspiralWaveformParamsInsertModeArrayJframeFromModeString(ldict, v)
        else:
            if isinstance(v, np.generic):
                v = v.item()
            elif type(v) is u.quantity.Quantity:
                v_val = v.si.value
                lal.DictInsertREAL8Value(ldict, k, v_val)
                continue
            if type(v) is float or lalsim.SimInspiralCheckKnownREAL8Key(k):
                lal.DictInsertREAL8Value(ldict, k, v)
            elif type(v) is int:
                lal.DictInsertINT4Value(ldict, k, v)
            elif type(v) is str:
                lal.DictInsertStringValue(ldict, k, v)
            else:
                raise TypeError
    return ldict

def from_lal_dict(ldict):
    """
    Convert LALDict object to a Python dictionary

    Parameters
    ----------
    d : `LALDict`
        LALDict object

    Returns
    -------
    d : `dict`
        Python dictionary
    """
    if ldict is None:
        return None
    d = dict()
    keys = lal.DictKeys(ldict)
    vals = lal.DictValues(ldict)
    size = lal.ListSize(keys)
    for i in range(size):
        key = lal.ListItemGetStringValue(lal.ListPop(keys))
        lal_item = lal.ListPop(vals)
        if 'ModeArray' in key:
            val = lalsim.SimInspiralModeArrayToModeString(lal.ListItemGetValue(lal_item))
        else:
            val = from_lal_value(lal.ListItemGetValue(lal_item))
        d[key] = val
    return d

def check_dict_parameters(waveform_dict, generic_param_dict=None):
    """Checks the parameters used in the waveform generation routine.

    Parameters
    ----------
        waveform_dict (dict): The dictionary of parameters used to generate the template.

        generic_param_dict (dict,optional): Dictionary of extra parameter names to be accepted in order to generate
                            non-standard waveforms. It should not include standard waveform parameters as they will
                            be ignored. The form should be parameter_name:parameter_units and the values should be just
                            added in the waveform_dict.
    Raises
    ------
        AssertionError: If a parameter has the wrong units.
        TypeError: If a parameter is not available to use or a dimensional parameter
                   is passed as dimensionless.

    """
    CheckDeterminationOfMasses(waveform_dict)
    CheckDeterminationOfSpins(waveform_dict)
    default_unit_sys = 'S.I.'
    if generic_param_dict is not None:
        full_parameter_list = np.concatenate([pc.full_parameter_list, list(generic_param_dict.keys())])
    else:
        full_parameter_list = pc.full_parameter_list
    for k in waveform_dict.keys():
        if k not in full_parameter_list:
            raise TypeError('Parameter %s not in accepted list of parameters' % k)
        elif k in pc.units_dict[default_unit_sys].keys():
            try:
                waveform_dict[k].unit
            except:
                raise TypeError('Parameter {} does not have units, please pass a parameter with astropy units equivalent to u.[{}]'.format(k, pc.units_dict[default_unit_sys][k]))
            assert waveform_dict[k].unit.is_equivalent(pc.units_dict[default_unit_sys][k]), 'Parameter {} does not have proper units, units should be equivalent to u.[{}]'.format(k, pc.units_dict[default_unit_sys][k])
        elif k == 'condition':
            if int(waveform_dict[k]) == 0 or int(waveform_dict[k]) == 1:
                continue
            else:
                raise TypeError('Condition should only be 0 or 1')
        elif k == 'lmax':
            if waveform_dict[k] < 0:
                raise ValueError('lmax must be >=0')
            continue
        elif generic_param_dict is not None:
            try:
                waveform_dict[k].unit
            except:
                raise TypeError('Parameter {} does not have units, please pass a parameter with astropy units equivalent to u.[{}]'.format(k, generic_param_dict[k]))
            assert waveform_dict[k].unit.is_equivalent(generic_param_dict[k]), 'Parameter {} does not have proper units, units should be equivalent to u.[{}]'.format(k, generic_param_dict[k])

def add_params_units(waveform_dict, units_sys='S.I.', generic_param_dict=None):
    """Add units or convert to desired units system to the waveform parameters dictionary

    Parameters
    ----------
        waveform_dict (dict): The dictionary of parameters used to generate the template.
        units_sys (:obj:`str`, optional): System of units chosen for the given parameters.
                   Defaults to None. If a unit system is given, try to convert and provide
                   units to the parameters in `waveform_dict`. If default checks the parameters in `waveform_dict`
                   have the appropriate units.
        generic_param_dict (dict,optional): Dictionary of extra parameter names to be accepted in order to generate
                            non-standard waveforms. It should not include standard waveform parameters as they will
                            be ignored. The form should be parameter_name:parameter_units and the values should be just
                            added in the waveform_dict.
    Returns
    -------
        A dict the corresponding conversions to the
        specified `units_sys` system.

    Raises
    ------
        AssertionError: If a parameter has wrong units

    """
    if units_sys in pc.units_dict.keys():
        dict_tmp = {key: u.Quantity(value, pc.units_dict[units_sys][key]) for key, value in waveform_dict.items() if key in pc.units_dict[units_sys].keys()}
    else:
        raise TypeError('The units system specified is not available. Available systems are {}'.format([key for key in pc.units_dict.keys()]))
    if generic_param_dict is not None:
        dict_tmp = {**dict_tmp, **{key: u.Quantity(value, generic_param_dict[key]) for key, value in waveform_dict.items() if key in generic_param_dict.keys()}}
    dict_tmp = {**waveform_dict, **dict_tmp}
    for par in pc.mass_params_[0:4]:
        if par in dict_tmp.keys():
            if dict_tmp[par] >= 2 * 10 ** 30 * u.solMass:
                warn_string = 'Are you sure you want to have a {} of {} Solar Masses?'.format(par, u.Quantity(dict_tmp[par], u.solMass).value)
                warnings.warn(warn_string)
        if 'mass_ratio' in dict_tmp.keys():
            if dict_tmp['mass_ratio'] < 0.001 or dict_tmp['mass_ratio'] > 1000.0:
                warn_string = 'Are you sure you want to have a q of {}?'.format(dict_tmp['mass_ratio'])
                warnings.warn(warn_string)
    return dict_tmp

def CheckDeterminationOfMasses(waveform_dict):
    """Check mass parameters are consistent and enough to fully characterize the binary masses

    Parameters
    ----------
        waveform_dict (dict): The dictionary of parameters used to generate the template.

    Raises
    ------
        TypeError: whenever mass parameters are over or underspecified

    """
    dim_number = 0
    nodim_number = 0
    sym_number = 0
    dimensionless_masses = ['mass_ratio', 'sym_mass_ratio']
    dimensionful_masses = ['mass1', 'mass2', 'total_mass', 'chirp_mass', 'mass_difference', 'reduced_mass']
    symetric_masses = ['mass1', 'mass2', 'total_mass', 'chirp_mass', 'sym_mass_ratio', 'reduced_mass']
    for param in dimensionful_masses:
        if param in waveform_dict.keys():
            dim_number += 1
    for param in dimensionless_masses:
        if param in waveform_dict.keys():
            nodim_number += 1
    for param in symetric_masses:
        if param in waveform_dict.keys():
            sym_number += 1
    if ('mass1' in waveform_dict.keys()) & ('mass2' in waveform_dict.keys()):
        sym_number = 0
    if dim_number == 2 and nodim_number == 0 or (dim_number == 1 and nodim_number == 1):
        if sym_number == 2:
            warn_string = 'The larger object cannot be determined, assuming m1 >= m2.'
            warnings.warn(warn_string)
    elif dim_number == 1 and nodim_number == 0 or dim_number == 0:
        raise TypeError('Mass parameters are underspecified. Please include one dimensionless and one dimensionful mass parameters, or two dimensionful masses.')
    else:
        raise TypeError('Mass parameters are overspecified. Please include one dimensionless and one dimensionful mass parameters, or two dimensionful masses.')

def CheckDeterminationOfSpins(waveform_dict):
    """Check spin parameters are consistent and enough to fully characterize the binary spins

    Parameters
    ----------
        waveform_dict (dict): The dictionary of parameters used to generate the template.

    Raises
    ------
        TypeError: whenever spin parameters are over or underspecified or system of coordinates is mixed

    """
    spin1_number = 0
    spin2_number = 0
    cartesian_1 = False
    cartesian_2 = False
    spherical_1 = False
    spherical_2 = False
    cartesian = ['x', 'y', 'z']
    spherical = ['_norm', '_tilt', '_phi']
    for sfx in cartesian:
        if 'spin1' + sfx in waveform_dict.keys():
            spin1_number += 1
        if 'spin2' + sfx in waveform_dict.keys():
            spin2_number += 1
    if spin1_number > 0:
        cartesian_1 = True
    if spin2_number > 0:
        cartesian_2 = True
    spin1_number = 0
    spin2_number = 0
    for sfx in spherical:
        if 'spin1' + sfx in waveform_dict.keys():
            spin1_number += 1
        if 'spin2' + sfx in waveform_dict.keys():
            spin2_number += 1
    if spin1_number > 0:
        spherical_1 = True
    if spin2_number > 0:
        spherical_2 = True
    if not xor(cartesian_1, spherical_1) or not xor(cartesian_2, spherical_2):
        raise TypeError('Please specify the 3 spin parameters in either spherical or cartesian coordinates.')