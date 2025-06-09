def create_hb_stream(self, kernel_id):
    """Create a new hb stream."""
    self._check_kernel_id(kernel_id)
    return super(MappingKernelManager, self).create_hb_stream(kernel_id)