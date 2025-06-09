import __init__
import unittest
import datetime
from TDhelper.document.excel.model import model
from TDhelper.document.excel.FieldType import FieldType

class stock(model):
    stock_date = FieldType(datetime.date, 1)
    stock_code = FieldType(str, 2)
    stock_name = FieldType(str, 3)
    stock_close_price = FieldType(float, 4)
    stock_max_price = FieldType(float, 5)
    stock_min_price = FieldType(float, 6)
    stock_open_price = FieldType(float, 7)
    stock_yesterday_close_price = FieldType(float, 8)
    stock_rise_and_fall_amount = FieldType(float, 9)
    stock_rise_and_fall_rate = FieldType(float, 10)
    stock_turnover_rate = FieldType(float, 11)
    stock_volumes = FieldType(float, 12)
    stock_volumes_amount = FieldType(float, 13)
    stock_all_market_cap = FieldType(float, 14)
    stock_circulate_market_cap = FieldType(float, 15)

    def __init__(self, excelPath=None):
        super(stock, self).__init__(excelPath)

class TestDoumentExcel(unittest.TestCase):

    def test_csv(self):
        with stock('C:\\Home\\dev\\Python\\pypi\\src\\2345.csv') as m_result:
            for v in m_result.items():
                self.assertRaises(Exception, m_result)
if __name__ == '__main__':
    unittest.main()