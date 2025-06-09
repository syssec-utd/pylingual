def change(script, layer_num=None):
    """ Change the current layer by specifying the new layer number.

    Args:
        script: the mlx.FilterScript object or script filename to write
            the filter to.
        layer_num (int): the number of the layer to change to. Default is the
            last layer if script is a mlx.FilterScript object; if script is a
            filename the default is the first layer.

    Layer stack:
        Modifies current layer

    MeshLab versions:
        2016.12
        1.3.4BETA
    """
    if layer_num is None:
        if isinstance(script, mlx.FilterScript):
            layer_num = script.last_layer()
        else:
            layer_num = 0
    filter_xml = ''.join(['  <filter name="Change the current layer">\n', '    <Param name="mesh" ', 'value="{:d}" '.format(layer_num), 'description="Mesh" ', 'type="RichMesh" ', '/>\n', '  </filter>\n'])
    util.write_filter(script, filter_xml)
    if isinstance(script, mlx.FilterScript):
        script.set_current_layer(layer_num)
    return None