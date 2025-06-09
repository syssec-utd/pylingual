def estimate_tx_gas_with_web3(self, safe_address: str, to: str, value: int, data: bytes) -> int:
    """
        Estimate tx gas using web3
        """
    return self.ethereum_client.estimate_gas(safe_address, to, value, data, block_identifier='pending')