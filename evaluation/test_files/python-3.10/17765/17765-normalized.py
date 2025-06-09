def submit(self, block_list):
    """
        Submits transfers.

        block_list (list of AIOBlock)
            The IO blocks to hand off to kernel.

        Returns the number of successfully submitted blocks.
        """
    submitted_count = libaio.io_submit(self._ctx, len(block_list), (libaio.iocb_p * len(block_list))(*[pointer(x._iocb) for x in block_list]))
    submitted = self._submitted
    for block in block_list[:submitted_count]:
        submitted[addressof(block._iocb)] = (block, block._getSubmissionState())
    return submitted_count