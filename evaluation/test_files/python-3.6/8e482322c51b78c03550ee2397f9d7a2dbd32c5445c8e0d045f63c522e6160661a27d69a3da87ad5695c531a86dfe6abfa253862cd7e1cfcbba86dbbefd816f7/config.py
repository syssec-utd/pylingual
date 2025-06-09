import os
CONFIG = {'local_data_dir': 'soho_data/', 'remote_data_dir': 'https://spdf.gsfc.nasa.gov/pub/data/soho/'}
if os.environ.get('SPEDAS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.sep.join([os.environ['SPEDAS_DATA_DIR'], 'soho'])
if os.environ.get('SOHO_DATA_DIR'):
    CONFIG['local_data_dir'] = os.environ['SOHO_DATA_DIR']