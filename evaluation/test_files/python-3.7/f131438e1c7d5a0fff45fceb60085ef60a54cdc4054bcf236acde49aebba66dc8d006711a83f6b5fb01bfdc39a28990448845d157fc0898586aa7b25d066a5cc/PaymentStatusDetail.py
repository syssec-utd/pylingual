from paytmpg.pg.constants.MerchantProperty import MerchantProperty
from paytmpg.pg.request.NativePaymentStatusRequestBody import NativePaymentStatusRequestBody
from paytmpg.pg.utils.stringUtil import make_string, equals

class PaymentStatusDetail:

    def __init__(self, payment_status_detail_builder):
        self.__orderId = payment_status_detail_builder.order_id
        self.__readTimeout = payment_status_detail_builder.read_timeout

    def get_order_id(self):
        return self.__orderId

    def get_read_timeout(self):
        return self.__readTimeout

    def __str__(self):
        return ''

    def __eq__(self, other):
        return equals(self)

    def __dir__(self):
        return ''

    def __create_native_payment_status_request_body(self):
        native_payment_status_request_body = NativePaymentStatusRequestBody()
        native_payment_status_request_body.set_mid(MerchantProperty.get_mid())
        native_payment_status_request_body.set_order_id(self.get_order_id())
        return native_payment_status_request_body

class PaymentStatusDetailBuilder:
    order_id = None
    read_timeout = None

    def __init__(self, order_id):
        self.order_id = order_id
        self.read_timeout = 30

    def build(self):
        return PaymentStatusDetail(self)

    def set_read_timeout(self, read_timeout):
        self.read_timeout = read_timeout
        return self

    def __str__(self):
        return make_string(self)

    def __eq__(self, other):
        return equals(self)

    def __setattr__(self, key, value):
        if not hasattr(self, key):
            raise AttributeError(' Can not be set '.format(key))
        self.__dict__[key] = value

    def __dir__(self):
        return ''