def get_certificate_from_connection(connection):
    """
    Extract an X.509 certificate from a socket connection.
    """
    certificate = connection.getpeercert(binary_form=True)
    if certificate:
        return x509.load_der_x509_certificate(certificate, backends.default_backend())
    return None