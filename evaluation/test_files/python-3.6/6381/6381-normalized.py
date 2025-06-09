def isometric_remesh(script, SamplingRate=10):
    """Isometric parameterization: remeshing

    """
    filter_xml = ''.join(['  <filter name="Iso Parametrization Remeshing">\n', '    <Param name="SamplingRate"', 'value="%d"' % SamplingRate, 'description="Sampling Rate"', 'type="RichInt"', 'tooltip="This specify the sampling rate for remeshing."', '/>\n', '  </filter>\n'])
    util.write_filter(script, filter_xml)
    return None