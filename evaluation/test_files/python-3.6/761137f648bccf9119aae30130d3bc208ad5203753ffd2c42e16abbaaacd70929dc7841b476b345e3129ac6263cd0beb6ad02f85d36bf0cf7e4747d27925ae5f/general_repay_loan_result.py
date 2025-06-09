from huobi.constant import *

class GeneralRepayLoanResult:
    """
    The margin order information.

    :member
        id: Inner id.
        type: The account type.
        state: The account state.
        symbol: The symbol, like "btcusdt".
        fl_price: The trigger price.
        fl_type: The trigger type.
        risk_rate: The risk rate.
        list:Balance Object list
    """

    def __init__(self):
        self.repayId = 0
        self.repayTime = 0

    def print_object(self, format_data=''):
        from huobi.utils.print_mix_object import PrintBasic
        PrintBasic.print_basic(self.repayId, format_data + 'repayId')
        PrintBasic.print_basic(self.repayTime, format_data + 'repayTime')
        print()