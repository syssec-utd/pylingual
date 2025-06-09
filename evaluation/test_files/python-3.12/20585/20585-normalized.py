def prepare_communication(self):
    """
        Prepare the buffers to be used for later communications
        """
    RectPartitioner.prepare_communication(self)
    if self.lower_neighbors[0] >= 0:
        self.in_lower_buffers = [zeros(1, float)]
        self.out_lower_buffers = [zeros(1, float)]
    if self.upper_neighbors[0] >= 0:
        self.in_upper_buffers = [zeros(1, float)]
        self.out_upper_buffers = [zeros(1, float)]