import json
import pandas as pd

def select_rand_db(self, types=None):
    if types:
        sql = "select ip,port,types from eie_ip where types='{}' order by rand() limit 1".format(types)
    else:
        sql = 'select ip,port,types from eie_ip order by rand() limit 1 '
    df = pd.read_sql(sql, self.engine)
    results = json.loads(df.to_json(orient='records'))
    if results and len(results) == 1:
        return results[0]
    return None