def update_policy(self, policyid, policy_description):
    """**Description**
            Update the policy with the given id

        **Arguments**
            - policyid: Unique identifier associated with this policy.
            - policy_description: A dictionary with the policy description.

        **Success Return Value**
            A JSON object containing the policy description.
        """
    url = self.url + '/api/scanning/v1/policies/' + policyid
    data = json.dumps(policy_description)
    res = requests.put(url, headers=self.hdrs, data=data, verify=self.ssl_verify)
    if not self._checkResponse(res):
        return [False, self.lasterr]
    return [True, res.json()]