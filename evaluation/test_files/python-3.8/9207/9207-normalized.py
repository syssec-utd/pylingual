def _refined_glimpse_sensor(self, x_t, l_p):
    """
        Parameters:
            x_t - 28x28 image
            l_p - 2x1 focus vector
        Returns:
            7*14 matrix
        """
    l_p = l_p * 14 + 14 - 4
    l_p = T.cast(T.round(l_p), 'int32')
    l_p = l_p * (l_p >= 0)
    l_p = l_p * (l_p < 21) + (l_p >= 21) * 20
    glimpse_1 = x_t[l_p[0]:l_p[0] + 7][:, l_p[1]:l_p[1] + 7]
    return glimpse_1