def send_transfer(self, transfers, depth=3, inputs=None, change_address=None, min_weight_magnitude=None, security_level=None):
    """
        Prepares a set of transfers and creates the bundle, then
        attaches the bundle to the Tangle, and broadcasts and stores the
        transactions.

        :param transfers:
            Transfers to include in the bundle.

        :param depth:
            Depth at which to attach the bundle.
            Defaults to 3.

        :param inputs:
            List of inputs used to fund the transfer.
            Not needed for zero-value transfers.

        :param change_address:
            If inputs are provided, any unspent amount will be sent to
            this address.

            If not specified, a change address will be generated
            automatically.

        :param min_weight_magnitude:
            Min weight magnitude, used by the node to calibrate Proof of
            Work.

            If not provided, a default value will be used.

        :param security_level:
            Number of iterations to use when generating new addresses
            (see :py:meth:`get_new_addresses`).

            This value must be between 1 and 3, inclusive.

            If not set, defaults to
            :py:attr:`AddressGenerator.DEFAULT_SECURITY_LEVEL`.

        :return:
            Dict with the following structure::

                {
                    'bundle': Bundle,
                        The newly-published bundle.
                }

        References:

        - https://github.com/iotaledger/wiki/blob/master/api-proposal.md#sendtransfer
        """
    if min_weight_magnitude is None:
        min_weight_magnitude = self.default_min_weight_magnitude
    return extended.SendTransferCommand(self.adapter)(seed=self.seed, depth=depth, transfers=transfers, inputs=inputs, changeAddress=change_address, minWeightMagnitude=min_weight_magnitude, securityLevel=security_level)