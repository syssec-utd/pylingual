class OssCallbackReq(object):

    def __init__(self, callback, incrementCall, stockCall, scanCall, reviewCall, seed=None):
        """
        :param callback:  回调地址，完整的url
        :param incrementCall:  增量回调，0-不开启，1-开启
        :param stockCall:  存量回调，0-不开启，1-开启
        :param scanCall:  扫描回调，0-不开启，1-开启
        :param reviewCall:  审核回调，0-不开启，1-开启
        :param seed: (Optional) 校验seed，不传或传入空字符串则生成新的seed并返回
        """
        self.callback = callback
        self.incrementCall = incrementCall
        self.stockCall = stockCall
        self.scanCall = scanCall
        self.reviewCall = reviewCall
        self.seed = seed