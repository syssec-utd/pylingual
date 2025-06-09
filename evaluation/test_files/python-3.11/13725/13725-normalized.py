def invoke_function(self, script_hash, operation, params, **kwargs):
    """ Invokes a contract's function with given parameters and returns the result.

        :param script_hash: contract script hash
        :param operation: name of the operation to invoke
        :param params: list of paramaters to be passed in to the smart contract
        :type script_hash: str
        :type operation: str
        :type params: list
        :return: result of the invocation
        :rtype: dictionary

        """
    contract_params = encode_invocation_params(params)
    raw_result = self._call(JSONRPCMethods.INVOKE_FUNCTION.value, [script_hash, operation, contract_params], **kwargs)
    return decode_invocation_result(raw_result)