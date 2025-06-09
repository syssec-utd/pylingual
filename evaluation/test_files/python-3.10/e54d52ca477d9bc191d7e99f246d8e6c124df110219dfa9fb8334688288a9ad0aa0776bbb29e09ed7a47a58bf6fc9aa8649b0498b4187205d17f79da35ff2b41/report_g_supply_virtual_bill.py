import csv
import os
import threading
import traceback
from flask import g
from sqlalchemy import or_
from sqlalchemy.sql.expression import null, true
from werkzeug.exceptions import BadRequest
import chellow.dloads
from chellow.computer import forecast_date
from chellow.gas.engine import GDataSource, g_contract_func
from chellow.models import GEra, GSupply, Session, Site, SiteGEra
from chellow.utils import csv_make_val, hh_format, hh_max, hh_min, req_date, req_int
from chellow.views import chellow_redirect

def content(g_supply_id, file_name, start_date, finish_date, user):
    caches = {}
    sess = None
    try:
        sess = Session()
        (running_name, finished_name) = chellow.dloads.make_names(f'g_supply_virtual_bill_{g_supply_id}.csv', user)
        f = open(running_name, mode='w', newline='')
        writer = csv.writer(f, lineterminator='\n')
        g_supply = GSupply.get_by_id(sess, g_supply_id)
        forecast_dt = forecast_date()
        prev_titles = None
        for g_era in sess.query(GEra).filter(GEra.g_supply == g_supply, GEra.start_date < finish_date, or_(GEra.finish_date == null(), GEra.finish_date > start_date)).order_by(GEra.start_date):
            chunk_start = hh_max(g_era.start_date, start_date)
            chunk_finish = hh_min(g_era.finish_date, finish_date)
            site = sess.query(Site).join(SiteGEra).filter(SiteGEra.g_era == g_era, SiteGEra.is_physical == true()).one()
            ds = GDataSource(sess, chunk_start, chunk_finish, forecast_dt, g_era, caches, None)
            titles = ['MPRN', 'Site Code', 'Site Name', 'Account', 'From', 'To', '']
            output_line = [g_supply.mprn, site.code, site.name, ds.account, hh_format(ds.start_date), hh_format(ds.finish_date), '']
            contract_titles = g_contract_func(caches, g_era.g_contract, 'virtual_bill_titles')()
            titles.extend(contract_titles)
            g_contract_func(caches, g_era.g_contract, 'virtual_bill')(ds)
            bill = ds.bill
            for title in contract_titles:
                if title in bill:
                    output_line.append(csv_make_val(bill[title]))
                    del bill[title]
                else:
                    output_line.append('')
            for k in sorted(bill.keys()):
                output_line.extend([k, bill[k]])
            if titles != prev_titles:
                prev_titles = titles
                writer.writerow([str(v) for v in titles])
            writer.writerow(output_line)
    except BadRequest as e:
        writer.writerow(['Problem: ' + e.description])
    except BaseException:
        writer.writerow([traceback.format_exc()])
    finally:
        if sess is not None:
            sess.close()
        if f is not None:
            f.close()
            os.rename(running_name, finished_name)

def do_get(sess):
    g_supply_id = req_int('g_supply_id')
    file_name = 'g_supply_virtual_bill_' + str(g_supply_id) + '.csv'
    start_date = req_date('start')
    finish_date = req_date('finish')
    args = (g_supply_id, file_name, start_date, finish_date, g.user)
    threading.Thread(target=content, args=args).start()
    return chellow_redirect('/downloads', 303)