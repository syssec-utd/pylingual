def _action_network(self, h_t):
    """
        Parameters:
            h_t - 256x1 vector
        Returns:
            10x1 vector
        """
    z = self._relu(T.dot(h_t, self.W_a) + self.B_a)
    return self._softmax(z)