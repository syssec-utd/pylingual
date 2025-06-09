def _build_cryptographic_parameters(self, value):
    """
        Build a CryptographicParameters struct from a dictionary.

        Args:
            value (dict): A dictionary containing the key/value pairs for a
                CryptographicParameters struct.

        Returns:
            None: if value is None
            CryptographicParameters: a CryptographicParameters struct

        Raises:
            TypeError: if the input argument is invalid
        """
    if value is None:
        return None
    elif not isinstance(value, dict):
        raise TypeError('Cryptographic parameters must be a dictionary.')
    cryptographic_parameters = CryptographicParameters(block_cipher_mode=value.get('block_cipher_mode'), padding_method=value.get('padding_method'), hashing_algorithm=value.get('hashing_algorithm'), key_role_type=value.get('key_role_type'), digital_signature_algorithm=value.get('digital_signature_algorithm'), cryptographic_algorithm=value.get('cryptographic_algorithm'), random_iv=value.get('random_iv'), iv_length=value.get('iv_length'), tag_length=value.get('tag_length'), fixed_field_length=value.get('fixed_field_length'), invocation_field_length=value.get('invocation_field_length'), counter_length=value.get('counter_length'), initial_counter_value=value.get('initial_counter_value'))
    return cryptographic_parameters