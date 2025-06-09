from aliyunsdkcore.request import RpcRequest
from aliyunsdkehpc.endpoint import endpoint_data

class DescribeImagePriceRequest(RpcRequest):

    def __init__(self):
        RpcRequest.__init__(self, 'EHPC', '2018-04-12', 'DescribeImagePrice')
        self.set_method('GET')
        if hasattr(self, 'endpoint_map'):
            setattr(self, 'endpoint_map', endpoint_data.getEndpointMap())
        if hasattr(self, 'endpoint_regional'):
            setattr(self, 'endpoint_regional', endpoint_data.getEndpointRegional())

    def get_Period(self):
        return self.get_query_params().get('Period')

    def set_Period(self, Period):
        self.add_query_param('Period', Period)

    def get_Amount(self):
        return self.get_query_params().get('Amount')

    def set_Amount(self, Amount):
        self.add_query_param('Amount', Amount)

    def get_ImageId(self):
        return self.get_query_params().get('ImageId')

    def set_ImageId(self, ImageId):
        self.add_query_param('ImageId', ImageId)

    def get_SkuCode(self):
        return self.get_query_params().get('SkuCode')

    def set_SkuCode(self, SkuCode):
        self.add_query_param('SkuCode', SkuCode)

    def get_PriceUnit(self):
        return self.get_query_params().get('PriceUnit')

    def set_PriceUnit(self, PriceUnit):
        self.add_query_param('PriceUnit', PriceUnit)

    def get_OrderType(self):
        return self.get_query_params().get('OrderType')

    def set_OrderType(self, OrderType):
        self.add_query_param('OrderType', OrderType)