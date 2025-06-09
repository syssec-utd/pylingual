def _create_input_transactions(self, addy):
    """
        Creates transactions for the specified input address.
        """
    self._transactions.append(ProposedTransaction(address=addy, tag=self.tag, value=-addy.balance))
    for _ in range(addy.security_level - 1):
        self._transactions.append(ProposedTransaction(address=addy, tag=self.tag, value=0))