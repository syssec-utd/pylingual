import numpy as np

def read_one_spectrum(file_input, **kwargs) -> dict:
    """
    A generator to read one spectrum from .mzml file.

    :param filename_input: The file path of input file, can be str or Path.
    :param obo_version: The version of obo file, default is "4.1.33".
    :return: a dict contains one spectrum information.    
    """
    import pymzml
    run = pymzml.run.Reader(file_input)
    for _scan_number, raw_spectrum_info in enumerate(run):
        spectrum_info = {'_ms_level': raw_spectrum_info.ms_level, '_scan_number': _scan_number + 1, 'peaks': np.asarray(raw_spectrum_info.peaks('centroided'), dtype=np.float32, order='C'), 'rt': raw_spectrum_info.scan_time_in_minutes() * 60, 'precursor_mz': raw_spectrum_info.selected_precursors[0].get('mz', None) if len(raw_spectrum_info.selected_precursors) > 0 else None, 'precursor_charge': raw_spectrum_info.selected_precursors[0].get('charge', None) if len(raw_spectrum_info.selected_precursors) > 0 else None}
        if spectrum_info['precursor_charge'] is None:
            if raw_spectrum_info['negative scan']:
                spectrum_info['precursor_charge'] = -1
            elif raw_spectrum_info['positive scan']:
                spectrum_info['precursor_charge'] = 1
        else:
            try:
                spectrum_info['precursor_charge'] = int(spectrum_info['precursor_charge'])
                if raw_spectrum_info['negative scan']:
                    spectrum_info['precursor_charge'] = -abs(spectrum_info['precursor_charge'])
                elif raw_spectrum_info['positive scan']:
                    spectrum_info['precursor_charge'] = abs(spectrum_info['precursor_charge'])
            except ValueError:
                print('Warning: precursor charge is not an integer: {}'.format(spectrum_info['precursor_charge']))
        yield spectrum_info
    run.close()