class CertificateSpec(object):

    def __init__(self, certificateId, isDefault=None):
        """
        :param certificateId:  证书Id
        :param isDefault: (Optional) 是否为默认证书，取值为True或False,默认为True，目前此字段暂不支持设置
        """
        self.certificateId = certificateId
        self.isDefault = isDefault