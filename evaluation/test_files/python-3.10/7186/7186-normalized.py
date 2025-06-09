def read(self, istream, kmip_version=enums.KMIPVersion.KMIP_1_0):
    """
        Read the data encoding the Certificate object and decode it into its
        constituent parts.

        Args:
            istream (Stream): A data stream containing encoded object data,
                supporting a read method; usually a BytearrayStream object.
            kmip_version (KMIPVersion): An enumeration defining the KMIP
                version with which the object will be decoded. Optional,
                defaults to KMIP 1.0.
        """
    super(Certificate, self).read(istream, kmip_version=kmip_version)
    tstream = BytearrayStream(istream.read(self.length))
    self.certificate_type = CertificateType()
    self.certificate_value = CertificateValue()
    self.certificate_type.read(tstream, kmip_version=kmip_version)
    self.certificate_value.read(tstream, kmip_version=kmip_version)
    self.is_oversized(tstream)