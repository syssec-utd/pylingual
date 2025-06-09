from functools import partial
import asyncio
import datetime
from jotdx.hq import TdxHq_API
from jotdx.exhq import TdxExHq_API
from jotdx.utils.best_ip import stock_ip, future_ip

def ping_stock(ip, port):
    api = TdxHq_API()
    r_dict = {'ip': ip, 'port': port, 'cost_time': None}
    with api.connect(ip, port, time_out=0.7):
        __time1 = datetime.datetime.now()
        res = api.get_security_list(0, 1)
        if res is not None:
            if len(res) > 800:
                print('GOOD RESPONSE {}'.format(ip))
                r_dict['cost_time'] = datetime.datetime.now() - __time1
                return r_dict
            else:
                print('BAD RESPONSE {}'.format(ip))
                r_dict['cost_time'] = datetime.timedelta(9, 9, 0)
                return r_dict
        else:
            print('BAD RESPONSE {}'.format(ip))
            r_dict['cost_time'] = datetime.timedelta(9, 9, 0)
            return r_dict

def ping_future(ip, port):
    apix = TdxExHq_API()
    r_dict = {'ip': ip, 'port': port, 'cost_time': None}
    with apix.connect(ip, port, time_out=0.7):
        __time1 = datetime.datetime.now()
        res = apix.get_instrument_count()
        if res is not None:
            if res > 20000:
                print('GOOD RESPONSE {}'.format(ip))
                r_dict['cost_time'] = datetime.datetime.now() - __time1
                return r_dict
            else:
                print('️Bad FUTUREIP REPSONSE {}'.format(ip))
                r_dict['cost_time'] = datetime.timedelta(9, 9, 0)
                return r_dict
        else:
            print('️Bad FUTUREIP REPSONSE {}'.format(ip))
            r_dict['cost_time'] = datetime.timedelta(9, 9, 0)
            return r_dict

async def ping_aync(ip, port=7709, type_='stock'):
    loop = asyncio.get_event_loop()
    params = {'ip': ip, 'port': port}
    try:
        if type_ in ['stock']:
            return await loop.run_in_executor(None, partial(ping_stock, **params))
        elif type_ in ['future']:
            return await loop.run_in_executor(None, partial(ping_future, **params))
    except Exception as e:
        if isinstance(e, TypeError):
            print(e)
            print('Tushare内置的pytdx版本和最新的pytdx 版本不同, 请重新安装pytdx以解决此问题')
            print('pip uninstall pytdx')
            print('pip install pytdx')
        else:
            print('BAD RESPONSE {}'.format(ip))
            params['cost_time'] = datetime.timedelta(9, 9, 0)
            return params

def select_best_ip_async(_type='stock'):
    """目前这里给的是单线程的选优, 如果需要多进程的选优/ 最优ip缓存 可以参考
    https://github.com/QUANTAXIS/QUANTAXIS/blob/master/QUANTAXIS/QAFetch/QATdx.py#L106
    """
    ip_list = stock_ip if _type == 'stock' else future_ip
    data = [ping_aync(x['ip'], x['port'], _type) for x in ip_list]
    loop = asyncio.get_event_loop()
    (done, _) = loop.run_until_complete(asyncio.wait(data))
    results = [d.result() for d in done if d.result()['cost_time'] < datetime.timedelta(0, 9, 0)]
    results = sorted(results, key=lambda x: x['cost_time'])
    return results[0]
if __name__ == '__main__':
    ip_port_time = select_best_ip_async('stock')
    print(1)
    ip = select_best_ip_async('future')
    print(ip)