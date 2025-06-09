import os
import sys
PATH = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)), 'src')
sys.path.append(PATH)
print(PATH)
from winhye_common.session.database import DatabaseClient

def test_database():
    conn = DatabaseClient('postgresql+psycopg2://xingqiao:Yhth111#@pgm-2zes4j7rsv2xbv789o.pg.rds.aliyuncs.com:1921/winhye_pre')
    sql = 'select * from user_info;'
    res = conn.get_values(sql, {})
    print(res)
    conn.close()
if __name__ == '__main__':
    test_database()