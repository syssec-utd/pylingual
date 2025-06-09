class Order:

    def __init__(self):
        self.price = 0.0
        self.qty = 0.0

class OrderBookEvent:

    def __init__(self):
        self.eventType = ''
        self.eventTime = ''
        self.transactionTime = ''
        self.symbol = ''
        self.firstUpdateId = 0
        self.lastUpdateId = 0
        self.lastUpdateIdInlastStream = 0
        self.bids = list()
        self.asks = list()

    @staticmethod
    def json_parse(json_data):
        result = OrderBookEvent()
        result.eventType = json_data.get_string('e')
        result.eventTime = json_data.get_int('E')
        result.transactionTime = json_data.get_int('T')
        result.symbol = json_data.get_string('s')
        result.firstUpdateId = json_data.get_int('U')
        result.lastUpdateId = json_data.get_int('u')
        result.lastUpdateIdInlastStream = json_data.get_int('pu')
        list_array = json_data.get_array('b')
        bid_list = list()
        for item in list_array.get_items():
            order = Order()
            val = item.convert_2_list()
            order.price = val[0]
            order.qty = val[1]
            bid_list.append(order)
        result.bids = bid_list
        list_array = json_data.get_array('a')
        ask_list = list()
        for item in list_array.get_items():
            order = Order()
            val = item.convert_2_list()
            order.price = val[0]
            order.qty = val[1]
            ask_list.append(order)
        result.asks = ask_list
        return result