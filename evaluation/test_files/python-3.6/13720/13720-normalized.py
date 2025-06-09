def get_contract_state(self, script_hash, **kwargs):
    """ Returns the contract information associated with a specific script hash.

        :param script_hash: contract script hash
        :type script_hash: str
        :return: dictionary containing the contract information
        :rtype: dict

        """
    return self._call(JSONRPCMethods.GET_CONTRACT_STATE.value, [script_hash], **kwargs)