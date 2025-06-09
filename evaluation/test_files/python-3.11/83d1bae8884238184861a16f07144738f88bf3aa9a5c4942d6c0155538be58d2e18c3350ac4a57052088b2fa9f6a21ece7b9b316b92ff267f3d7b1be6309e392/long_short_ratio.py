from datetime import datetime

class LongShortRatio:

    def __init__(self):
        self.symbol = None
        self.long_short_ratio = None
        self.long_accounts = None
        self.short_accounts = None
        self.timestamp = None
        self.datetime = None

    @staticmethod
    def create_instance_for_binance(data, symbol: str):
        instance = LongShortRatio()
        instance.symbol = symbol
        instance.long_short_ratio = float(data['longShortRatio'])
        instance.long_accounts = float(data['longAccount'])
        instance.short_accounts = float(data['shortAccount'])
        instance.timestamp = int(data['timestamp'])
        instance.datetime = datetime.fromtimestamp(instance.timestamp / 1000)
        return instance