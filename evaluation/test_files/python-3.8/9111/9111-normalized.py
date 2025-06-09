def set_payment_method(self, method=PAYMENT_METHOD.CASH_ON_DELIVERY):
    """
        Select the payment method going to be used to make a purchase.

        :param int method: Payment method id.
        :return: A response having set the payment option.
        :rtype: requests.Response
        """
    params = {'paymentMethod': method}
    return self.__post('/PaymentOptions/SetPaymentMethod', json=params)