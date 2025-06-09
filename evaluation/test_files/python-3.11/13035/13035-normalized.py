def capacity_meyerhof_and_hanna_1978(sl_0, sl_1, h0, fd, gwl=1000000.0, verbose=0):
    """
    Calculates the two-layered foundation capacity according Meyerhof and Hanna (1978)

    :param sl_0: Top Soil object
    :param sl_1: Base Soil object
    :param h0: Height of top soil layer
    :param fd: Foundation object
    :param wtl: water table level
    :param verbose: verbosity
    :return: ultimate bearing stress
    """
    sp = sm.SoilProfile()
    sp.add_layer(0, sl_0)
    sp.add_layer(h0, sl_1)
    sp.gwl = gwl
    return capacity_sp_meyerhof_and_hanna_1978(sp, fd)