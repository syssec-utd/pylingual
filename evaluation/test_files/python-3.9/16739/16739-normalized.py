def detect_devices(soapy_args=''):
    """Returns detected SoapySDR devices"""
    devices = simplesoapy.detect_devices(soapy_args, as_string=True)
    text = []
    text.append('Detected SoapySDR devices:')
    if devices:
        for (i, d) in enumerate(devices):
            text.append('  {}'.format(d))
    else:
        text.append('  No devices found!')
    return (devices, '\n'.join(text))