import csv
import os
import threading
from collections import defaultdict
from datetime import datetime as Datetime
from io import StringIO
from itertools import chain, islice
from random import random
from dateutil.relativedelta import relativedelta
from flask import Blueprint, Response, flash, g, make_response, render_template as rtemplate, request
from sqlalchemy import Float, case, cast, false, func, null, or_, select, text, true
from sqlalchemy.orm import joinedload
from werkzeug.exceptions import BadRequest, NotFound
from zish import dumps, loads
import chellow.e.dno_rate_parser
from chellow.e.energy_management import totals_runner
from chellow.models import Batch, BatchFile, Bill, BillType, Channel, ClockInterval, Comm, Contract, Cop, EnergisationStatus, Era, GeneratorType, GspGroup, HhDatum, Laf, Llfc, METER_TYPES, MarketRole, MeasurementRequirement, MeterPaymentType, MeterType, Mtc, MtcLlfc, MtcLlfcSsc, MtcLlfcSscPc, MtcParticipant, MtcSsc, Participant, Party, Pc, RateScript, ReadType, RegisterRead, Report, Scenario, Site, SiteEra, Snag, Source, Ssc, Supply, Tpr, VoltageLevel
from chellow.utils import HH, PropDict, c_months_u, csv_make_val, ct_datetime, ct_datetime_now, hh_after, hh_format, hh_max, hh_min, hh_range, parse_hh_start, parse_mpan_core, req_bool, req_date, req_decimal, req_file, req_hh_date, req_int, req_str, req_zish, to_ct, to_utc, utc_datetime, utc_datetime_now
from chellow.views import chellow_redirect as credirect

def chellow_redirect(path, code=None):
    return credirect(f'/e{path}', code)
e = Blueprint('e', __name__, template_folder='templates', url_prefix='/e')

def render_template(tname, **kwargs):
    return rtemplate(f'e/{tname}', **kwargs)

@e.route('/asset_comparison')
def asset_comparison_get():
    config_contract = Contract.get_non_core_by_name(g.sess, 'configuration')
    props = config_contract.make_properties()
    description = props.get('asset_comparison', '')
    return render_template('asset_comparison.html', description=description)

@e.route('/csv_sites_triad')
def csv_sites_triad_get():
    now = Datetime.utcnow()
    if now.month < 3:
        now -= relativedelta(years=1)
    return render_template('csv_sites_triad.html', year=now.year)

@e.route('/csv_sites_hh_data')
def csv_sites_hh_data_get():
    now = Datetime.utcnow()
    start_date = Datetime(now.year, now.month, 1) - relativedelta(months=1)
    finish_date = Datetime(now.year, now.month, 1) - HH
    return render_template('csv_sites_hh_data.html', start_date=start_date, finish_date=finish_date)

@e.route('/csv_supplies_triad')
def csv_supplies_triad_get():
    now = Datetime.utcnow()
    return render_template('csv_supplies_triad.html', year=now.year - 1)

@e.route('/csv_register_reads')
def csv_register_reads_get():
    init = Datetime.utcnow()
    init = Datetime(init.year, init.month, 1) - relativedelta(months=1)
    return render_template('csv_register_reads.html', init=init)

@e.route('/csv_supplies_hh_data')
def csv_supplies_hh_data_get():
    now = Datetime.utcnow()
    start_date = Datetime(now.year, now.month, 1) - relativedelta(months=1)
    finish_date = Datetime(now.year, now.month, 1) - HH
    return render_template('csv_supplies_hh_data.html', start_date=start_date, finish_date=finish_date)

@e.route('/csv_supplies_snapshot')
def csv_supplies_snapshot_get():
    now = utc_datetime_now()
    return render_template('csv_supplies_snapshot.html', default_timestamp=utc_datetime(now.year, now.month, now.day))

@e.route('/csv_bills')
def csv_bills_get():
    init = Datetime.utcnow()
    init = Datetime(init.year, init.month, 1) - relativedelta(months=1)
    return render_template('csv_bills.html', init=init)

@e.route('/eras/<int:era_id>/add_channel')
def channel_add_get(era_id):
    era = Era.get_by_id(g.sess, era_id)
    channels = g.sess.query(Channel).filter(Channel.era == era).order_by(Channel.imp_related, Channel.channel_type)
    return render_template('channel_add.html', era=era, channels=channels)

@e.route('/eras/<int:era_id>/add_channel', methods=['POST'])
def channel_add_post(era_id):
    try:
        imp_related = req_bool('imp_related')
        channel_type = req_str('channel_type')
        era = Era.get_by_id(g.sess, era_id)
        channel = era.insert_channel(g.sess, imp_related, channel_type)
        g.sess.commit()
        return chellow_redirect(f'/channels/{channel.id}', 303)
    except BadRequest as e:
        flash(e.description)
        channels = g.sess.query(Channel).filter(Channel.era == era).order_by(Channel.imp_related, Channel.channel_type)
        return render_template('channel_add.html', era=era, channels=channels)

@e.route('/channels/<int:channel_id>')
def channel_get(channel_id):
    channel = Channel.get_by_id(g.sess, channel_id)
    page = req_int('page') if 'page' in request.values else 0
    page_size = 3000
    prev_page = None if page == 0 else page - 1
    hh_data = g.sess.query(HhDatum).filter(HhDatum.channel == channel).order_by(HhDatum.start_date).offset(page * page_size).limit(page_size)
    if g.sess.query(HhDatum).filter(HhDatum.channel == channel).order_by(HhDatum.start_date).offset((page + 1) * page_size).limit(page_size).count() > 0:
        next_page = page + 1
    else:
        next_page = None
    snags = g.sess.query(Snag).filter(Snag.channel == channel).order_by(Snag.start_date)
    return render_template('channel.html', channel=channel, hh_data=hh_data, snags=snags, prev_page=prev_page, this_page=page, next_page=next_page)

@e.route('/channels/<int:channel_id>/edit')
def channel_edit_get(channel_id):
    channel = Channel.get_by_id(g.sess, channel_id)
    now = utc_datetime_now()
    return render_template('channel_edit.html', channel=channel, now=now)

@e.route('/channels/<int:channel_id>/edit', methods=['POST'])
def channel_edit_post(channel_id):
    try:
        channel = Channel.get_by_id(g.sess, channel_id)
        if 'delete' in request.values:
            supply_id = channel.era.supply.id
            channel.era.delete_channel(g.sess, channel.imp_related, channel.channel_type)
            g.sess.commit()
            return chellow_redirect(f'/supplies/{supply_id}', 303)
        elif 'delete_data' in request.values:
            start_date = req_hh_date('start')
            finish_date = req_hh_date('finish')
            channel.delete_data(g.sess, start_date, finish_date)
            g.sess.commit()
            flash('Data successfully deleted.')
            return chellow_redirect(f'/channels/{channel_id}/edit', 303)
        elif 'insert' in request.values:
            start_date = req_hh_date('start')
            value = req_decimal('value')
            status = req_str('status')
            if start_date < channel.era.start_date:
                raise BadRequest('The start date is before the start of this era.')
            if hh_after(start_date, channel.era.finish_date):
                raise BadRequest('The finish date is after the end of this era.')
            hh_datum = g.sess.query(HhDatum).filter(HhDatum.channel == channel, HhDatum.start_date == start_date).first()
            if hh_datum is not None:
                raise BadRequest("There's already a datum in this channel at this time.")
            if channel.imp_related:
                mpan_core = channel.era.imp_mpan_core
            else:
                mpan_core = channel.era.exp_mpan_core
            HhDatum.insert(g.sess, [{'start_date': start_date, 'value': value, 'status': status, 'mpan_core': mpan_core, 'channel_type': channel.channel_type}])
            g.sess.commit()
            return chellow_redirect(f'/channels/{channel_id}', 303)
    except BadRequest as e:
        flash(e.description)
        now = utc_datetime_now()
        return render_template('channel_edit.html', channel=channel, now=now)

@e.route('/channel_snags')
def channel_snags_get():
    contract_id = req_int('dc_contract_id')
    contract = Contract.get_dc_by_id(g.sess, contract_id)
    days_hidden = req_int('days_hidden')
    is_ignored = req_bool('is_ignored')
    total_snags = g.sess.query(Snag).join(Channel).join(Era).filter(Snag.is_ignored == false(), Era.dc_contract == contract, Snag.start_date < utc_datetime_now() - relativedelta(days=days_hidden)).count()
    snags = g.sess.query(Snag).join(Channel).join(Era).join(Era.site_eras).join(SiteEra.site).filter(Snag.is_ignored == is_ignored, Era.dc_contract == contract, Snag.start_date < utc_datetime_now() - relativedelta(days=days_hidden)).order_by(Site.code, Era.id, Snag.start_date, Snag.finish_date, Snag.channel_id)
    snag_groups = []
    prev_snag = None
    for snag in islice(snags, 200):
        if prev_snag is None or snag.channel.era != prev_snag.channel.era or snag.start_date != prev_snag.start_date or (snag.finish_date != prev_snag.finish_date) or (snag.description != prev_snag.description):
            era = snag.channel.era
            snag_group = {'snags': [], 'sites': g.sess.query(Site).join(Site.site_eras).filter(SiteEra.era == era).order_by(Site.code), 'era': era, 'description': snag.description, 'start_date': snag.start_date, 'finish_date': snag.finish_date}
            snag_groups.append(snag_group)
        snag_group['snags'].append(snag)
        prev_snag = snag
    return render_template('channel_snags.html', contract=contract, snags=snags, total_snags=total_snags, snag_groups=snag_groups, is_ignored=is_ignored)

@e.route('/channel_snags/<int:snag_id>')
def channel_snag_get(snag_id):
    snag = Snag.get_by_id(g.sess, snag_id)
    return render_template('channel_snag.html', snag=snag)

@e.route('/channel_snags/<int:snag_id>/edit')
def channel_snag_edit_get(snag_id):
    snag = Snag.get_by_id(g.sess, snag_id)
    return render_template('channel_snag_edit.html', snag=snag)

@e.route('/channel_snags/<int:snag_id>/edit', methods=['POST'])
def channel_snag_edit_post(snag_id):
    try:
        ignore = req_bool('ignore')
        snag = Snag.get_by_id(g.sess, snag_id)
        snag.set_is_ignored(ignore)
        g.sess.commit()
        return chellow_redirect(f'/channel_snags/{snag.id}', 303)
    except BadRequest as e:
        g.sess.rollback()
        flash(e.description)
        return make_response(render_template('channel_snag_edit.html', snag=snag), 400)

@e.route('/comms')
def comms_get():
    comms = g.sess.execute(select(Cop).order_by(Cop.code)).scalars()
    return render_template('comms.html', comms=comms)

@e.route('/comms/<int:comm_id>')
def comm_get(comm_id):
    comm = Comm.get_by_id(g.sess, comm_id)
    return render_template('comm.html', comm=comm)

@e.route('/cops')
def cops_get():
    cops = g.sess.query(Cop).order_by(Cop.code)
    return render_template('cops.html', cops=cops)

@e.route('/cops/<int:cop_id>')
def cop_get(cop_id):
    cop = Cop.get_by_id(g.sess, cop_id)
    return render_template('cop.html', cop=cop)

@e.route('/dc_contracts/<int:contract_id>/auto_importer')
def dc_auto_importer_get(contract_id):
    contract = Contract.get_dc_by_id(g.sess, contract_id)
    task = chellow.e.hh_importer.get_hh_import_task(contract)
    return render_template('dc_auto_importer.html', contract=contract, task=task)

@e.route('/dc_contracts/<int:contract_id>/auto_importer', methods=['POST'])
def dc_auto_importer_post(contract_id):
    try:
        contract = Contract.get_dc_by_id(g.sess, contract_id)
        task = chellow.e.hh_importer.get_hh_import_task(contract)
        task.go()
        return chellow_redirect(f'/dc_contracts/{contract.id}/auto_importer', 303)
    except BadRequest as e:
        flash(e.description)
        return make_response(render_template('dc_auto_importer.html', contract=contract, task=task), 400)

@e.route('/dc_batches')
def dc_batches_get():
    contract_id = req_int('dc_contract_id')
    contract = Contract.get_dc_by_id(g.sess, contract_id)
    batches = g.sess.execute(select(Batch, func.count(Bill.id), func.coalesce(func.sum(Bill.net), 0), func.coalesce(func.sum(Bill.vat), 0), func.coalesce(func.sum(Bill.gross), 0)).join(Bill, isouter=True).where(Batch.contract == contract).group_by(Batch.id).order_by(Batch.reference.desc()))
    return render_template('dc_batches.html', contract=contract, batches=batches)

@e.route('/dc_batches/<int:batch_id>')
def dc_batch_get(batch_id):
    batch = Batch.get_by_id(g.sess, batch_id)
    bills = g.sess.query(Bill).filter(Bill.batch == batch).order_by(Bill.reference).all()
    config_contract = Contract.get_non_core_by_name(g.sess, 'configuration')
    properties = config_contract.make_properties()
    importer_ids = sorted(chellow.e.bill_importer.get_bill_import_ids(batch), reverse=True)
    fields = {'batch': batch, 'bills': bills, 'importer_ids': importer_ids}
    if 'batch_reports' in properties:
        batch_reports = []
        for report_id in properties['batch_reports']:
            batch_reports.append(Report.get_by_id(g.sess, report_id))
        fields['batch_reports'] = batch_reports
    return render_template('dc_batch.html', **fields)

@e.route('/dc_batches/<int:batch_id>/csv')
def dc_batch_csv_get(batch_id):
    batch = Batch.get_by_id(g.sess, batch_id)
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['HHDC Contract', 'Batch Reference', 'Bill Reference', 'Account', 'Issued', 'From', 'To', 'kWh', 'Net', 'VAT', 'Gross', 'Type'])
    for bill in g.sess.query(Bill).filter(Bill.batch == batch).order_by(Bill.reference, Bill.start_date).options(joinedload(Bill.bill_type)):
        cw.writerow([batch.contract.name, batch.reference, bill.reference, bill.account, hh_format(bill.issue_date), hh_format(bill.start_date), hh_format(bill.finish_date), str(bill.kwh), str(bill.net), str(bill.vat), str(bill.gross), bill.bill_type.code])
    output = make_response(si.getvalue())
    output.headers['Content-Disposition'] = 'attachment; filename="batch.csv"'
    output.headers['Content-type'] = 'text/csv'
    return output

@e.route('/dc_batches/<int:batch_id>', methods=['POST'])
def dc_batch_post(batch_id):
    try:
        batch = Batch.get_by_id(g.sess, batch_id)
        if 'import_bills' in request.values:
            import_id = chellow.e.bill_importer.start_bill_import(batch)
            return chellow_redirect(f'/dc_bill_imports/{import_id}', 303)
        elif 'delete_bills' in request.values:
            g.sess.query(Bill).filter(Bill.batch == batch).delete(False)
            g.sess.commit()
            return chellow_redirect(f'/dc_batches/{batch.id}', 303)
        elif 'delete_import_bills' in request.values:
            g.sess.query(Bill).filter(Bill.batch == batch).delete(False)
            g.sess.commit()
            import_id = chellow.e.bill_importer.start_bill_import(batch)
            return chellow_redirect(f'/dc_bill_imports/{import_id}', 303)
    except BadRequest as e:
        flash(e.description)
        importer_ids = sorted(chellow.e.bill_importer.get_bill_import_ids(batch), reverse=True)
        parser_names = chellow.e.bill_importer.find_parser_names()
        return make_response(render_template('dc_batch.html', batch=batch, importer_ids=importer_ids, parser_names=parser_names), 400)

@e.route('/dc_contracts/<int:contract_id>/add_batch')
def dc_batch_add_get(contract_id):
    contract = Contract.get_dc_by_id(g.sess, contract_id)
    batches = g.sess.query(Batch).filter(Batch.contract == contract).order_by(Batch.reference.desc())
    next_batch_reference, next_batch_description = contract.get_next_batch_details(g.sess)
    return render_template('dc_batch_add.html', contract=contract, batches=batches, next_batch_reference=next_batch_reference, next_batch_description=next_batch_description)

@e.route('/dc_contracts/<int:contract_id>/add_batch', methods=['POST'])
def dc_batch_add_post(contract_id):
    try:
        contract = Contract.get_dc_by_id(g.sess, contract_id)
        reference = req_str('reference')
        description = req_str('description')
        batch = contract.insert_batch(g.sess, reference, description)
        g.sess.commit()
        return chellow_redirect(f'/dc_batches/{batch.id}', 303)
    except BadRequest as e:
        flash(e.description)
        batches = g.sess.query(Batch).filter(Batch.contract == contract).order_by(Batch.reference.desc())
        return make_response(render_template('dc_batch_add.html', contract=contract, batches=batches), 400)

@e.route('/dc_batches/<int:batch_id>/edit')
def dc_batch_edit_get(batch_id):
    batch = Batch.get_by_id(g.sess, batch_id)
    return render_template('dc_batch_edit.html', batch=batch)

@e.route('/dc_batches/<int:batch_id>/edit', methods=['POST'])
def dc_batch_edit_post(batch_id):
    try:
        batch = Batch.get_by_id(g.sess, batch_id)
        if 'delete' in request.values:
            contract = batch.contract
            batch.delete(g.sess)
            g.sess.commit()
            return chellow_redirect(f'/dc_batches?dc_contract_id={contract.id}', 303)
        elif 'delete_bills' in request.values:
            g.sess.query(Bill).filter(Bill.batch == batch).delete(False)
            g.sess.commit()
            return chellow_redirect(f'/dc_batches/{batch.id}', 303)
        else:
            reference = req_str('reference')
            description = req_str('description')
            batch.update(g.sess, reference, description)
            g.sess.commit()
            return chellow_redirect(f'/dc_batches/{batch.id}', 303)
    except BadRequest as e:
        flash(e.description)
        return make_response(render_template('dc_batch_edit.html', batch=batch), 400)

@e.route('/dc_batches/<int:batch_id>/upload_file')
def dc_batch_upload_file_get(batch_id):
    batch = Batch.get_by_id(g.sess, batch_id)
    parser_names = chellow.e.bill_importer.find_parser_names()
    return render_template('dc_batch_upload_file.html', batch=batch, parser_names=parser_names)

@e.route('/dc_batches/<int:batch_id>/upload_file', methods=['POST'])
def dc_batch_upload_file_post(batch_id):
    batch = None
    try:
        batch = Batch.get_by_id(g.sess, batch_id)
        file_item = request.files['import_file']
        parser_name = req_str('parser_name')
        batch_file = batch.insert_file(g.sess, file_item.filename, file_item.stream.read(), parser_name)
        g.sess.commit()
        return chellow_redirect(f'/dc_batches/{batch.id}#batch_file_{batch_file.id}', 303)
    except BadRequest as e:
        flash(e.description)
        parser_names = chellow.e.bill_importer.find_parser_names()
        return make_response(render_template('dc_batch_upload_file.html', batch=batch, parser_names=parser_names), 400)

@e.route('/dc_batch_files/<int:file_id>')
def dc_batch_file_get(file_id):
    batch_file = BatchFile.get_by_id(g.sess, file_id)
    importer_ids = sorted(chellow.e.bill_importer.get_bill_import_ids(batch_file), reverse=True)
    return render_template('dc_batch_file.html', batch_file=batch_file, importer_ids=importer_ids)

@e.route('/dc_batch_files/<int:file_id>/download')
def dc_batch_file_download_get(file_id):
    batch_file = BatchFile.get_by_id(g.sess, file_id)
    output = make_response(batch_file.data)
    output.headers['Content-Disposition'] = f'attachment; filename="{batch_file.filename}"'
    output.headers['Content-type'] = 'application/octet-stream'
    return output

@e.route('/dc_batch_files/<int:file_id>/edit')
def dc_batch_file_edit_get(file_id):
    batch_file = BatchFile.get_by_id(g.sess, file_id)
    parser_names = chellow.e.bill_importer.find_parser_names()
    return render_template('dc_batch_file_edit.html', batch_file=batch_file, parser_names=parser_names)

@e.route('/dc_batch_files/<int:file_id>/edit', methods=['POST'])
def dc_batch_file_edit_post(file_id):
    batch_file = None
    try:
        batch_file = BatchFile.get_by_id(g.sess, file_id)
        if 'delete' in request.values:
            batch_id = batch_file.batch.id
            batch_file.delete(g.sess)
            g.sess.commit()
            flash('Deletion successful')
            return chellow_redirect(f'/dc_batches/{batch_id}', 303)
        else:
            parser_name = req_str('parser_name')
            batch_file.update(parser_name)
            g.sess.commit()
            flash('Update successful')
            return chellow_redirect(f'/dc_batch_files/{batch_file.id}', 303)
    except BadRequest as e:
        flash(e.description)
        parser_names = chellow.bill_importer.find_parser_names()
        return make_response(render_template('dc_batch_file_edit.html', batch_file=batch_file, parser_names=parser_names), 400)

@e.route('/dc_batches/<int:batch_id>/add_bill')
def dc_bill_add_get(batch_id):
    batch = Batch.get_by_id(g.sess, batch_id)
    bill_types = g.sess.query(BillType).order_by(BillType.code)
    bills = g.sess.query(Bill).filter(Bill.batch == batch).order_by(Bill.start_date)
    return render_template('dc_bill_add.html', batch=batch, bill_types=bill_types, bills=bills)

@e.route('/dc_batches/<int:batch_id>/add_bill', methods=['POST'])
def dc_bill_add_post(batch_id):
    try:
        batch = Batch.get_by_id(g.sess, batch_id)
        mpan_core = req_str('mpan_core')
        mpan_core = parse_mpan_core(mpan_core)
        account = req_str('account')
        reference = req_str('reference')
        issue_date = req_date('issue')
        start_date = req_hh_date('start')
        finish_date = req_hh_date('finish')
        kwh = req_decimal('kwh')
        net = req_decimal('net')
        vat = req_decimal('vat')
        gross = req_decimal('gross')
        bill_type_id = req_int('bill_type_id')
        bill_type = BillType.get_by_id(g.sess, bill_type_id)
        breakdown_str = req_str('breakdown')
        breakdown = loads(breakdown_str)
        bill_type = BillType.get_by_id(g.sess, bill_type_id)
        bill = batch.insert_bill(g.sess, account, reference, issue_date, start_date, finish_date, kwh, net, vat, gross, bill_type, breakdown, Supply.get_by_mpan_core(g.sess, mpan_core))
        g.sess.commit()
        return chellow_redirect(f'/dc_bills/{bill.id}', 303)
    except BadRequest as e:
        g.sess.rollback()
        flash(e.description)
        bill_types = g.sess.query(BillType).order_by(BillType.code)
        bills = g.sess.query(Bill).filter(Bill.batch == batch).order_by(Bill.start_date)
        return make_response(render_template('dc_bill_add.html', batch=batch, bill_types=bill_types, bills=bills), 400)

@e.route('/dc_bill_imports/<int:import_id>')
def dc_bill_import_get(import_id):
    importer = chellow.e.bill_importer.get_bill_import(import_id)
    batch = Batch.get_by_id(g.sess, importer.batch_id)
    fields = {'batch': batch}
    if importer is not None:
        imp_fields = importer.make_fields()
        if 'successful_bills' in imp_fields and len(imp_fields['successful_bills']) > 0:
            fields['successful_max_registers'] = max((len(bill['reads']) for bill in imp_fields['successful_bills']))
        fields.update(imp_fields)
        fields['status'] = importer.status()
    return render_template('dc_bill_import.html', **fields)

@e.route('/dc_bills/<int:bill_id>')
def dc_bill_get(bill_id):
    bill = Bill.get_by_id(g.sess, bill_id)
    fields = {'bill': bill}
    try:
        breakdown_dict = loads(bill.breakdown)
        raw_lines = []
        for key in ('raw_lines', 'raw-lines'):
            try:
                raw_lines += breakdown_dict[key]
                del breakdown_dict[key]
            except KeyError:
                pass
        rows = set()
        columns = set()
        grid = defaultdict(dict)
        for k, v in tuple(breakdown_dict.items()):
            if k.endswith('-gbp'):
                columns.add('gbp')
                row_name = k[:-4]
                rows.add(row_name)
                grid[row_name]['gbp'] = v
                del breakdown_dict[k]
        for k, v in tuple(breakdown_dict.items()):
            for row_name in sorted(list(rows), key=len, reverse=True):
                if k.startswith(row_name + '-'):
                    col_name = k[len(row_name) + 1:]
                    columns.add(col_name)
                    grid[row_name][col_name] = csv_make_val(v)
                    del breakdown_dict[k]
                    break
        for k, v in breakdown_dict.items():
            pair = k.split('-')
            row_name = '-'.join(pair[:-1])
            column_name = pair[-1]
            rows.add(row_name)
            columns.add(column_name)
            grid[row_name][column_name] = csv_make_val(v)
        column_list = sorted(list(columns))
        for rate_name in [col for col in column_list if col.endswith('rate')]:
            column_list.remove(rate_name)
            column_list.append(rate_name)
        if 'gbp' in column_list:
            column_list.remove('gbp')
            column_list.append('gbp')
        row_list = sorted(list(rows))
        fields.update({'raw_lines': raw_lines, 'row_list': row_list, 'column_list': column_list, 'grid': grid})
    except SyntaxError:
        pass
    return render_template('dc_bill.html', **fields)

@e.route('/dc_bills/<int:bill_id>/edit')
def dc_bill_edit_get(bill_id):
    bill = Bill.get_by_id(g.sess, bill_id)
    bill_types = g.sess.query(BillType).order_by(BillType.code)
    return render_template('dc_bill_edit.html', bill=bill, bill_types=bill_types)

@e.route('/dc_bills/<int:bill_id>/edit', methods=['POST'])
def dc_bill_edit_post(bill_id):
    try:
        bill = Bill.get_by_id(g.sess, bill_id)
        if 'delete' in request.values:
            bill.delete(g.sess)
            g.sess.commit()
            return chellow_redirect(f'/dc_batches/{bill.batch.id}', 303)
        else:
            account = req_str('account')
            reference = req_str('reference')
            issue_date = req_date('issue')
            start_date = req_date('start')
            finish_date = req_date('finish')
            kwh = req_decimal('kwh')
            net = req_decimal('net')
            vat = req_decimal('vat')
            gross = req_decimal('gross')
            type_id = req_int('bill_type_id')
            breakdown = req_zish('breakdown')
            bill_type = BillType.get_by_id(g.sess, type_id)
            bill.update(account, reference, issue_date, start_date, finish_date, kwh, net, vat, gross, bill_type, breakdown)
            g.sess.commit()
            return chellow_redirect(f'/dc_bills/{bill.id}', 303)
    except BadRequest as e:
        flash(e.description)
        bill_types = g.sess.query(BillType).order_by(BillType.code).all()
        return render_template('dc_bill_edit.html', bill=bill, bill_types=bill_types)

@e.route('/dc_contracts')
def dc_contracts_get():
    dc_contracts = g.sess.execute(select(Contract).join(MarketRole).where(MarketRole.code == 'C').order_by(Contract.name)).scalars()
    return render_template('dc_contracts.html', dc_contracts=dc_contracts)

@e.route('/dc_contracts/add', methods=['POST'])
def dc_contracts_add_post():
    try:
        participant_id = req_int('participant_id')
        name = req_str('name')
        start_date = req_date('start')
        participant = Participant.get_by_id(g.sess, participant_id)
        contract = Contract.insert_dc(g.sess, name, participant, '{}', {}, start_date, None, {})
        g.sess.commit()
        chellow.e.hh_importer.startup_contract(contract.id)
        return chellow_redirect(f'/dc_contracts/{contract.id}', 303)
    except BadRequest as e:
        flash(e.description)
        initial_date = utc_datetime_now()
        initial_date = Datetime(initial_date.year, initial_date.month, 1)
        parties = g.sess.query(Party).join(MarketRole).join(Participant).filter(MarketRole.code == 'C').order_by(Participant.code).all()
        return make_response(render_template('dc_contracts_add.html', initial_date=initial_date, parties=parties), 400)

@e.route('/dc_contracts/add')
def dc_contracts_add_get():
    initial_date = utc_datetime_now()
    initial_date = Datetime(initial_date.year, initial_date.month, 1)
    parties = g.sess.execute(select(Party).join(MarketRole).join(Participant).where(MarketRole.code == 'C').order_by(Participant.code)).scalars()
    return render_template('dc_contracts_add.html', initial_date=initial_date, parties=parties)

@e.route('/dc_contracts/<int:dc_contract_id>')
def dc_contract_get(dc_contract_id):
    rate_scripts = None
    try:
        contract = Contract.get_dc_by_id(g.sess, dc_contract_id)
        rate_scripts = g.sess.query(RateScript).filter(RateScript.contract == contract).order_by(RateScript.start_date.desc()).all()
        now = utc_datetime_now()
        last_month_finish = Datetime(now.year, now.month, 1) - relativedelta(minutes=30)
        return render_template('dc_contract.html', dc_contract=contract, rate_scripts=rate_scripts, last_month_finish=last_month_finish)
    except BadRequest as e:
        desc = e.description
        flash(desc)
        if desc.startswith("There isn't a contract"):
            raise e
        else:
            return render_template('dc_contract.html', contract=contract, rate_scripts=rate_scripts, last_month_finish=last_month_finish)

@e.route('/dc_contracts/<int:dc_contract_id>/edit')
def dc_contract_edit_get(dc_contract_id):
    parties = g.sess.query(Party).join(MarketRole).join(Participant).filter(MarketRole.code == 'C').order_by(Participant.code).all()
    dc_contract = Contract.get_dc_by_id(g.sess, dc_contract_id)
    initial_date = utc_datetime_now()
    return render_template('dc_contract_edit.html', parties=parties, initial_date=initial_date, dc_contract=dc_contract)

@e.route('/dc_contracts/<int:contract_id>/edit', methods=['POST'])
def dc_contract_edit_post(contract_id):
    contract = None
    try:
        contract = Contract.get_dc_by_id(g.sess, contract_id)
        if 'update_state' in request.form:
            state = req_zish('state')
            contract.update_state(state)
            g.sess.commit()
            return chellow_redirect(f'/dc_contracts/{contract.id}', 303)
        elif 'ignore_snags' in request.form:
            ignore_date = req_date('ignore')
            g.sess.execute(text('update snag set is_ignored = true from channel, era where snag.channel_id = channel.id and channel.era_id = era.id and era.dc_contract_id = :contract_id and snag.finish_date < :ignore_date'), params=dict(contract_id=contract.id, ignore_date=ignore_date))
            g.sess.commit()
            return chellow_redirect(f'/dc_contracts/{contract.id}', 303)
        elif 'delete' in request.form:
            contract.delete(g.sess)
            g.sess.commit()
            return chellow_redirect('/dc_contracts', 303)
        else:
            party_id = req_int('party_id')
            name = req_str('name')
            charge_script = req_str('charge_script')
            properties = req_zish('properties')
            party = Party.get_by_id(g.sess, party_id)
            contract.update(name, party, charge_script, properties)
            g.sess.commit()
            return chellow_redirect(f'/dc_contracts/{contract.id}', 303)
    except BadRequest as e:
        flash(e.description)
        if contract is None:
            raise e
        else:
            parties = g.sess.query(Party).join(MarketRole).join(Participant).filter(MarketRole.code == 'C').order_by(Participant.code).all()
            initial_date = utc_datetime_now()
            return make_response(render_template('dc_contract_edit.html', parties=parties, initial_date=initial_date, dc_contract=contract), 400)

@e.route('/dc_contracts/<int:contract_id>/hh_imports')
def dc_contracts_hh_imports_get(contract_id):
    contract = Contract.get_dc_by_id(g.sess, contract_id)
    processes = chellow.e.hh_importer.get_hh_import_processes(contract.id)
    return render_template('dc_contract_hh_imports.html', contract=contract, processes=processes, parser_names=', '.join(chellow.e.hh_importer.extensions))

@e.route('/dc_contracts/<int:contract_id>/hh_imports', methods=['POST'])
def dc_contracts_hh_imports_post(contract_id):
    try:
        contract = Contract.get_dc_by_id(g.sess, contract_id)
        file_item = req_file('import_file')
        f = StringIO(str(file_item.stream.read(), 'utf-8'))
        f.seek(0, os.SEEK_END)
        file_size = f.tell()
        f.seek(0)
        hh_import_process = chellow.e.hh_importer.start_hh_import_process(contract_id, f, file_item.filename, file_size)
        return chellow_redirect(f'/dc_contracts/{contract.id}/hh_imports/{hh_import_process.id}', 303)
    except BadRequest as e:
        if contract is None:
            raise e
        else:
            flash(e.description)
            processes = chellow.e.hh_importer.get_hh_import_processes(contract.id)
            return make_response(render_template('dc_contract_hh_imports.html', contract=contract, processes=processes), 400)

@e.route('/dc_contracts/<int:contract_id>/hh_imports/<int:import_id>')
def dc_contracts_hh_import_get(contract_id, import_id):
    contract = Contract.get_dc_by_id(g.sess, contract_id)
    process = chellow.e.hh_importer.get_hh_import_processes(contract_id)[import_id]
    return render_template('dc_contract_hh_import.html', contract=contract, process=process)

@e.route('/dc_contracts/<int:contract_id>/add_rate_script')
def dc_rate_script_add_get(contract_id):
    now = utc_datetime_now()
    initial_date = utc_datetime(now.year, now.month)
    contract = Contract.get_dc_by_id(g.sess, contract_id)
    return render_template('dc_rate_script_add.html', now=now, contract=contract, initial_date=initial_date)

@e.route('/dc_contracts/<int:contract_id>/add_rate_script', methods=['POST'])
def dc_rate_script_add_post(contract_id):
    try:
        contract = Contract.get_dc_by_id(g.sess, contract_id)
        start_date = req_date('start')
        rate_script = contract.insert_rate_script(g.sess, start_date, {})
        g.sess.commit()
        return chellow_redirect(f'/dc_rate_scripts/{rate_script.id}', 303)
    except BadRequest as e:
        flash(e.description)
        now = utc_datetime_now()
        initial_date = utc_datetime(now.year, now.month)
        return render_template('dc_rate_script_add.html', now=now, contract=contract, initial_date=initial_date)

@e.route('/dc_rate_scripts/<int:dc_rate_script_id>')
def dc_rate_script_get(dc_rate_script_id):
    rate_script = RateScript.get_dc_by_id(g.sess, dc_rate_script_id)
    contract = rate_script.contract
    next_rate_script = g.sess.query(RateScript).filter(RateScript.contract == contract, RateScript.start_date > rate_script.start_date).order_by(RateScript.start_date).first()
    previous_rate_script = g.sess.query(RateScript).filter(RateScript.contract == contract, RateScript.start_date < rate_script.start_date).order_by(RateScript.start_date.desc()).first()
    return render_template('dc_rate_script.html', dc_rate_script=rate_script, previous_rate_script=previous_rate_script, next_rate_script=next_rate_script)

@e.route('/dc_rate_scripts/<int:dc_rate_script_id>/edit')
def dc_rate_script_edit_get(dc_rate_script_id):
    dc_rate_script = RateScript.get_dc_by_id(g.sess, dc_rate_script_id)
    rs_example_func = chellow.e.computer.contract_func({}, dc_rate_script.contract, 'rate_script_example')
    rs_example = None if rs_example_func is None else rs_example_func()
    return render_template('dc_rate_script_edit.html', dc_rate_script=dc_rate_script, rate_script_example=rs_example)

@e.route('/dc_rate_scripts/<int:dc_rate_script_id>/edit', methods=['POST'])
def dc_rate_script_edit_post(dc_rate_script_id):
    try:
        dc_rate_script = RateScript.get_dc_by_id(g.sess, dc_rate_script_id)
        dc_contract = dc_rate_script.contract
        if 'delete' in request.form:
            dc_contract.delete_rate_script(g.sess, dc_rate_script)
            g.sess.commit()
            return chellow_redirect(f'/dc_contracts/{dc_contract.id}', 303)
        else:
            script = req_zish('script')
            start_date = req_date('start')
            has_finished = req_bool('has_finished')
            finish_date = req_date('finish') if has_finished else None
            dc_contract.update_rate_script(g.sess, dc_rate_script, start_date, finish_date, script)
            g.sess.commit()
            return chellow_redirect(f'/dc_rate_scripts/{dc_rate_script.id}', 303)
    except BadRequest as e:
        flash(e.description)
        return render_template('dc_rate_script_edit.html', dc_rate_script=dc_rate_script)

@e.route('/dno_rate_scripts/<int:dno_rate_script_id>')
def dno_rate_script_get(dno_rate_script_id):
    rate_script = RateScript.get_dno_by_id(g.sess, dno_rate_script_id)
    contract = rate_script.contract
    dno = Party.get_dno_by_code(g.sess, contract.name, rate_script.start_date)
    next_rate_script = g.sess.query(RateScript).filter(RateScript.contract == contract, RateScript.start_date > rate_script.start_date).order_by(RateScript.start_date).first()
    previous_rate_script = g.sess.query(RateScript).filter(RateScript.contract == contract, RateScript.start_date < rate_script.start_date).order_by(RateScript.start_date.desc()).first()
    return render_template('dno_rate_script.html', dno=dno, rate_script=rate_script, previous_rate_script=previous_rate_script, next_rate_script=next_rate_script)

@e.route('/dno_rate_scripts/<int:dno_rate_script_id>/edit')
def dno_rate_script_edit_get(dno_rate_script_id):
    dno_rate_script = RateScript.get_dno_by_id(g.sess, dno_rate_script_id)
    dno = Party.get_dno_by_code(g.sess, dno_rate_script.contract.name, dno_rate_script.start_date)
    return render_template('dno_rate_script_edit.html', rate_script=dno_rate_script, dno=dno)

@e.route('/dno_rate_scripts/<int:dno_rate_script_id>/edit', methods=['DELETE'])
def dno_rate_script_edit_delete(dno_rate_script_id):
    try:
        rate_script = RateScript.get_dno_by_id(g.sess, dno_rate_script_id)
        contract = rate_script.contract
        dno = Party.get_dno_by_code(g.sess, contract.name, rate_script.start_date)
        contract.delete_rate_script(g.sess, rate_script)
        g.sess.commit()
        res = make_response()
        res.headers['HX-Redirect'] = f'{chellow.utils.url_root}/e/dnos/{dno.id}'
        return res
    except BadRequest as e:
        flash(e.description)
        return render_template('dno_rate_script_edit.html', rate_script=rate_script, dno=dno)

@e.route('/dno_rate_scripts/<int:dno_rate_script_id>/edit', methods=['POST'])
def dno_rate_script_edit_post(dno_rate_script_id):
    try:
        rate_script = RateScript.get_dno_by_id(g.sess, dno_rate_script_id)
        contract = rate_script.contract
        dno = Party.get_dno_by_code(g.sess, contract.name, rate_script.start_date)
        script = req_zish('script')
        start_date = req_date('start')
        has_finished = req_bool('has_finished')
        finish_date = req_date('finish') if has_finished else None
        contract.update_rate_script(g.sess, rate_script, start_date, finish_date, script)
        g.sess.commit()
        return chellow_redirect(f'/dno_rate_scripts/{rate_script.id}', 303)
    except BadRequest as e:
        flash(e.description)
        return render_template('dno_rate_script_edit.html', rate_script=rate_script, dno=dno)

@e.route('/dnos/<int:dno_id>/add_rate_script')
def dno_rate_script_add_get(dno_id):
    now = ct_datetime_now()
    initial_date = to_utc(ct_datetime(now.year, now.month))
    dno = Party.get_dno_by_id(g.sess, dno_id)
    return render_template('dno_rate_script_add.html', now=now, dno=dno, initial_date=initial_date)

@e.route('/dnos/<int:dno_id>/add_rate_script', methods=['POST'])
def dno_rate_script_add_post(dno_id):
    try:
        dno = Party.get_dno_by_id(g.sess, dno_id)
        contract = Contract.get_dno_by_name(g.sess, dno.dno_code)
        start_date = req_date('start')
        rate_script = contract.insert_rate_script(g.sess, start_date, {})
        g.sess.commit()
        return chellow_redirect(f'/dno_rate_scripts/{rate_script.id}', 303)
    except BadRequest as e:
        flash(e.description)
        now = ct_datetime_now()
        initial_date = to_utc(ct_datetime(now.year, now.month))
        return render_template('dno_rate_script_add.html', dno=dno, now=now, contract=contract, initial_date=initial_date)

@e.route('/dnos')
def dnos_get():
    dnos = []
    for dno in g.sess.query(Party).join(MarketRole).filter(MarketRole.code == 'R').order_by(Party.dno_code):
        dno_contract = Contract.get_dno_by_name(g.sess, dno.dno_code)
        dno_dict = {'party': dno, 'contract': dno_contract}
        dnos.append(dno_dict)
    gsp_groups = g.sess.query(GspGroup).order_by(GspGroup.code)
    return render_template('dnos.html', dnos=dnos, gsp_groups=gsp_groups)

@e.route('/dnos/<int:dno_id>')
def dno_get(dno_id):
    dno = Party.get_dno_by_id(g.sess, dno_id)
    dno_contract = Contract.get_dno_by_name(g.sess, dno.dno_code)
    rate_scripts = g.sess.execute(select(RateScript).where(RateScript.contract == dno_contract).order_by(RateScript.start_date.desc())).scalars()
    return render_template('dno.html', dno=dno, dno_contract=dno_contract, rate_scripts=rate_scripts)

@e.route('/dtc_meter_types')
def dtc_meter_types_get():
    return render_template('dtc_meter_types.html', dtc_meter_types=METER_TYPES)

@e.route('/dtc_meter_types/<code>')
def dtc_meter_type_get(code):
    desc = METER_TYPES[code]
    return render_template('dtc_meter_type.html', dtc_meter_type_code=code, dtc_meter_type_description=desc)

@e.route('/duration_report')
def duration_report_get(ct_now=None):
    ct_now = ct_datetime_now() if ct_now is None else ct_now
    ct_last = ct_now - relativedelta(months=1)
    months = list(c_months_u(start_year=ct_last.year, start_month=ct_last.month))
    month_start, month_finish = months[0]
    return render_template('duration_report.html', month_start=month_start, month_finish=month_finish)

@e.route('/energisation_statuses')
def energisation_statuses_get():
    energisation_statuses = g.sess.query(EnergisationStatus).order_by(EnergisationStatus.code)
    return render_template('energisation_statuses.html', energisation_statuses=energisation_statuses)

@e.route('/energisation_statuses/<int:energisation_status_id>')
def energisation_status_get(energisation_status_id):
    energisation_status = EnergisationStatus.get_by_id(g.sess, energisation_status_id)
    return render_template('energisation_status.html', energisation_status=energisation_status)

@e.route('/eras/<int:era_id>/edit')
def era_edit_get(era_id):
    era = Era.get_by_id(g.sess, era_id)
    energisation_statuses = g.sess.query(EnergisationStatus).order_by(EnergisationStatus.code)
    pcs = g.sess.query(Pc).order_by(Pc.code)
    cops = g.sess.query(Cop).order_by(Cop.code)
    comms = g.sess.query(Comm).order_by(Comm.code)
    gsp_groups = g.sess.query(GspGroup).order_by(GspGroup.code)
    mop_contracts = g.sess.query(Contract).join(MarketRole).filter(MarketRole.code == 'M').order_by(Contract.name)
    dc_contracts = g.sess.query(Contract).join(MarketRole).filter(MarketRole.code == 'C').order_by(Contract.name)
    supplier_contracts = g.sess.query(Contract).join(MarketRole).filter(MarketRole.code == 'X').order_by(Contract.name)
    site_eras = g.sess.query(SiteEra).join(Site).filter(SiteEra.era == era).order_by(Site.code).all()
    return render_template('era_edit.html', era=era, energisation_statuses=energisation_statuses, pcs=pcs, cops=cops, comms=comms, gsp_groups=gsp_groups, mop_contracts=mop_contracts, dc_contracts=dc_contracts, supplier_contracts=supplier_contracts, site_eras=site_eras)

@e.route('/eras/<int:era_id>/edit', methods=['POST'])
def era_edit_post(era_id):
    try:
        era = Era.get_by_id(g.sess, era_id)
        if 'delete' in request.form:
            supply = era.supply
            supply.delete_era(g.sess, era)
            g.sess.commit()
            return chellow_redirect(f'/supplies/{supply.id}', 303)
        elif 'attach' in request.form:
            site_code = req_str('site_code')
            site = Site.get_by_code(g.sess, site_code)
            era.attach_site(g.sess, site)
            g.sess.commit()
            return chellow_redirect(f'/supplies/{era.supply.id}', 303)
        elif 'detach' in request.form:
            site_id = req_int('site_id')
            site = Site.get_by_id(g.sess, site_id)
            era.detach_site(g.sess, site)
            g.sess.commit()
            return chellow_redirect(f'/supplies/{era.supply.id}', 303)
        elif 'locate' in request.form:
            site_id = req_int('site_id')
            site = Site.get_by_id(g.sess, site_id)
            era.set_physical_location(g.sess, site)
            g.sess.commit()
            return chellow_redirect(f'/supplies/{era.supply.id}', 303)
        else:
            start_date = req_date('start')
            is_ended = req_bool('is_ended')
            if is_ended:
                finish_date = req_hh_date('finish')
            else:
                finish_date = None
            mop_contract_id = req_int('mop_contract_id')
            mop_contract = Contract.get_mop_by_id(g.sess, mop_contract_id)
            mop_account = req_str('mop_account')
            dc_contract_id = req_int('dc_contract_id')
            dc_contract = Contract.get_dc_by_id(g.sess, dc_contract_id)
            dc_account = req_str('dc_account')
            msn = req_str('msn')
            pc_id = req_int('pc_id')
            pc = Pc.get_by_id(g.sess, pc_id)
            mtc_code = req_str('mtc_code')
            cop_id = req_int('cop_id')
            cop = Cop.get_by_id(g.sess, cop_id)
            comm_id = req_int('comm_id')
            comm = Comm.get_by_id(g.sess, comm_id)
            ssc_code = req_str('ssc_code')
            ssc_code = ssc_code.strip()
            energisation_status_id = req_int('energisation_status_id')
            energisation_status = EnergisationStatus.get_by_id(g.sess, energisation_status_id)
            properties = req_zish('properties')
            if len(ssc_code) == 0:
                ssc = None
            else:
                ssc = Ssc.get_by_code(g.sess, ssc_code, start_date)
            if 'imp_mpan_core' in request.values:
                imp_mpan_core_raw = req_str('imp_mpan_core')
            else:
                imp_mpan_core_raw = None
            if imp_mpan_core_raw is None or len(imp_mpan_core_raw.strip()) == 0:
                imp_mpan_core = None
                imp_sc = None
                imp_supplier_contract = None
                imp_supplier_account = None
                imp_llfc_code = None
            else:
                imp_mpan_core = parse_mpan_core(imp_mpan_core_raw)
                imp_llfc_code = req_str('imp_llfc_code')
                imp_supplier_contract_id = req_int('imp_supplier_contract_id')
                imp_supplier_contract = Contract.get_supplier_by_id(g.sess, imp_supplier_contract_id)
                imp_supplier_account = req_str('imp_supplier_account')
                imp_sc = req_int('imp_sc')
            if 'exp_mpan_core' in request.form:
                exp_mpan_core_raw = req_str('exp_mpan_core')
            else:
                exp_mpan_core_raw = None
            if exp_mpan_core_raw is None or len(exp_mpan_core_raw.strip()) == 0:
                exp_mpan_core = None
                exp_llfc_code = None
                exp_sc = None
                exp_supplier_contract = None
                exp_supplier_account = None
            else:
                exp_mpan_core = parse_mpan_core(exp_mpan_core_raw)
                exp_llfc_code = req_str('exp_llfc_code')
                exp_sc = req_int('exp_sc')
                exp_supplier_contract_id = req_int('exp_supplier_contract_id')
                exp_supplier_contract = Contract.get_supplier_by_id(g.sess, exp_supplier_contract_id)
                exp_supplier_account = req_str('exp_supplier_account')
            era.supply.update_era(g.sess, era, start_date, finish_date, mop_contract, mop_account, dc_contract, dc_account, msn, pc, mtc_code, cop, comm, ssc, energisation_status, properties, imp_mpan_core, imp_llfc_code, imp_supplier_contract, imp_supplier_account, imp_sc, exp_mpan_core, exp_llfc_code, exp_supplier_contract, exp_supplier_account, exp_sc)
            g.sess.commit()
            return chellow_redirect(f'/supplies/{era.supply.id}', 303)
    except BadRequest as e:
        flash(e.description)
        energisation_statuses = g.sess.query(EnergisationStatus).order_by(EnergisationStatus.code)
        pcs = g.sess.query(Pc).order_by(Pc.code)
        cops = g.sess.query(Cop).order_by(Cop.code)
        comms = g.sess.execute(select(Comm).order_by(Comm.code)).scalars()
        gsp_groups = g.sess.query(GspGroup).order_by(GspGroup.code)
        mop_contracts = g.sess.query(Contract).join(MarketRole).filter(MarketRole.code == 'M').order_by(Contract.name)
        dc_contracts = g.sess.query(Contract).join(MarketRole).filter(MarketRole.code.in_(('C', 'D'))).order_by(Contract.name)
        supplier_contracts = g.sess.query(Contract).join(MarketRole).filter(MarketRole.code == 'X').order_by(Contract.name)
        site_eras = g.sess.query(SiteEra).join(Site).filter(SiteEra.era == era).order_by(Site.code).all()
        return make_response(render_template('era_edit.html', era=era, pcs=pcs, cops=cops, comms=comms, gsp_groups=gsp_groups, mop_contracts=mop_contracts, dc_contracts=dc_contracts, supplier_contracts=supplier_contracts, site_eras=site_eras, energisation_statuses=energisation_statuses), 400)

@e.route('/eras/<int:era_id>/add_supplier_bill')
def era_supplier_bill_add_get(era_id):
    era = Era.get_by_id(g.sess, era_id)
    bill_types = g.sess.query(BillType).order_by(BillType.code)
    start_date = account = None
    normal_bill_type_id = g.sess.query(BillType.id).filter(BillType.code == 'N').scalar()
    latest_bill = g.sess.query(Bill).join(Batch).join(Contract).join(MarketRole).filter(Bill.supply == era.supply, MarketRole.code == 'X').order_by(Bill.start_date.desc()).first()
    if latest_bill is None:
        next_batch_reference = next_batch_description = ''
    else:
        start_date = latest_bill.finish_date + HH
        account = latest_bill.account
        next_batch_reference, next_batch_description = latest_bill.batch.contract.get_next_batch_details(g.sess)
    return render_template('era_supplier_bill_add.html', era=era, bill_types=bill_types, start_date=start_date, account=account, normal_bill_type_id=normal_bill_type_id, next_batch_reference=next_batch_reference, next_batch_description=next_batch_description)

@e.route('/eras/<int:era_id>/add_supplier_bill', methods=['POST'])
def era_supplier_bill_add_post(era_id):
    try:
        era = Era.get_by_id(g.sess, era_id)
        batch_reference = req_str('batch_reference')
        batch_description = req_str('batch_description')
        batch = era.imp_supplier_contract.insert_batch(g.sess, batch_reference, batch_description)
        account = req_str('account')
        bill_reference = req_str('bill_reference')
        issue_date = req_date('issue')
        start_date = req_hh_date('start')
        finish_date = req_hh_date('finish')
        kwh = req_decimal('kwh')
        net = req_decimal('net')
        vat = req_decimal('vat')
        gross = req_decimal('gross')
        bill_type_id = req_int('bill_type_id')
        bill_type = BillType.get_by_id(g.sess, bill_type_id)
        breakdown_str = req_str('breakdown')
        breakdown = loads(breakdown_str)
        bill_type = BillType.get_by_id(g.sess, bill_type_id)
        batch.insert_bill(g.sess, account, bill_reference, issue_date, start_date, finish_date, kwh, net, vat, gross, bill_type, breakdown, era.supply)
        g.sess.commit()
        return chellow_redirect(f'/supplies/{era.supply.id}', 303)
    except BadRequest as e:
        g.sess.rollback()
        flash(e.description)
        bill_types = g.sess.query(BillType).order_by(BillType.code)
        return make_response(render_template('era_supplier_bill_add.html', era=era, bill_types=bill_types, start_date=None, account=None), 400)

@e.route('/generator_types')
def generator_types_get():
    generator_types = g.sess.query(GeneratorType).order_by(GeneratorType.code)
    return render_template('generator_types.html', generator_types=generator_types)

@e.route('/generator_types/<int:generator_type_id>')
def generator_type_get(generator_type_id):
    generator_type = GeneratorType.get_by_id(g.sess, generator_type_id)
    return render_template('generator_type.html', generator_type=generator_type)

@e.route('/gsp_groups')
def gsp_groups_get():
    return render_template('gsp_groups.html', groups=g.sess.query(GspGroup).order_by(GspGroup.code).all())

@e.route('/gsp_groups/<int:group_id>')
def gsp_group_get(group_id):
    group = GspGroup.get_by_id(g.sess, group_id)
    return render_template('gsp_group.html', gsp_group=group)

@e.route('/hh_data/<int:datum_id>/edit')
def hh_datum_edit_get(datum_id):
    hh = HhDatum.get_by_id(g.sess, datum_id)
    return render_template('hh_datum_edit.html', hh=hh)

@e.route('/hh_data/<int:datum_id>/edit', methods=['POST'])
def hh_datum_edit_post(datum_id):
    try:
        hh = HhDatum.get_by_id(g.sess, datum_id)
        channel_id = hh.channel.id
        if 'delete' in request.values:
            hh.channel.delete_data(g.sess, hh.start_date, hh.start_date)
            g.sess.commit()
            return chellow_redirect(f'/channels/{channel_id}', 303)
        else:
            value = req_decimal('value')
            status = req_str('status')
            channel = hh.channel
            era = channel.era
            imp_mpan_core = era.imp_mpan_core
            exp_mpan_core = era.exp_mpan_core
            mpan_core = imp_mpan_core if channel.imp_related else exp_mpan_core
            HhDatum.insert(g.sess, [{'mpan_core': mpan_core, 'channel_type': channel.channel_type, 'start_date': hh.start_date, 'value': value, 'status': status}])
            g.sess.commit()
            return chellow_redirect(f'/channels/{channel_id}', 303)
    except BadRequest as e:
        flash(e.description)
        return make_response(render_template('hh_datum_edit.html', hh=hh), 400)

@e.route('/lafs')
def lafs_get():
    llfc_id = req_int('llfc_id')
    year = req_int('year')
    month = req_int('month')
    llfc = Llfc.get_by_id(g.sess, llfc_id)
    dno = llfc.dno
    start_date, finish_date = next(c_months_u(start_year=year, start_month=month, months=1))
    lafs = g.sess.execute(select(Laf).where(Laf.llfc == llfc, Laf.timestamp >= start_date, Laf.timestamp <= finish_date).order_by(Laf.timestamp)).scalars().all()
    return render_template('lafs.html', dno=dno, llfc=llfc, lafs=lafs)

@e.route('/llfcs')
def llfcs_get():
    dno_id = req_int('dno_id')
    dno = Party.get_dno_by_id(g.sess, dno_id)
    llfcs = g.sess.query(Llfc).filter(Llfc.dno == dno).order_by(Llfc.code)
    return render_template('llfcs.html', llfcs=llfcs, dno=dno)

def _csv_response(fname, titles, rows):
    with StringIO() as f:
        writer = csv.writer(f)
        writer.writerow(titles)
        for row in rows:
            writer.writerow([csv_make_val(v) for v in row])
        return Response(f.getvalue(), mimetype='text/csv', headers={'Content-disposition': f'attachment; filename="{fname}"'})

@e.route('/llfcs/csv')
def llfcs_csv_get():
    dno_id = req_int('dno_id')
    dno = Party.get_dno_by_id(g.sess, dno_id)
    rows = g.sess.execute(select(Party.dno_code, Llfc.code, Llfc.description, VoltageLevel.code, Llfc.is_substation, Llfc.is_import, Llfc.valid_from, Llfc.valid_to).join(Party).join(VoltageLevel).where(Llfc.dno == dno).order_by(Llfc.code)).all()
    titles = ('dno_code', 'code', 'description', 'voltage_level', 'is_substation', 'is_import', 'valid_from', 'valid_to')
    return _csv_response(f'llfcs_{dno.dno_code}.csv', titles, rows)

@e.route('/llfcs/<int:llfc_id>')
def llfc_get(llfc_id):
    llfc = Llfc.get_by_id(g.sess, llfc_id)
    now = ct_datetime_now()
    return render_template('llfc.html', llfc=llfc, now=now)

@e.route('/llfcs/<int:llfc_id>/edit')
def llfc_edit_get(llfc_id):
    llfc = Llfc.get_by_id(g.sess, llfc_id)
    voltage_levels = g.sess.query(VoltageLevel).order_by(VoltageLevel.code).all()
    return render_template('llfc_edit.html', llfc=llfc, voltage_levels=voltage_levels)

@e.route('/llfcs/<int:llfc_id>/edit', methods=['POST'])
def llfc_edit_post(llfc_id):
    try:
        llfc = Llfc.get_by_id(g.sess, llfc_id)
        voltage_level_id = req_int('voltage_level_id')
        voltage_level = VoltageLevel.get_by_id(g.sess, voltage_level_id)
        is_substation = req_bool('is_substation')
        llfc.update(llfc.description, voltage_level, is_substation, llfc.is_import, llfc.valid_from, llfc.valid_to)
        g.sess.commit()
        return chellow_redirect(f'/llfcs/{llfc.id}', 303)
    except BadRequest as e:
        g.sess.rollback()
        flash(e.description)
        return make_response(render_template('llfc_edit.html', llfc=llfc), 400)

@e.route('/market_roles/<int:market_role_id>')
def market_role_get(market_role_id):
    market_role = MarketRole.get_by_id(g.sess, market_role_id)
    return render_template('market_role.html', market_role=market_role)

@e.route('/market_roles')
def market_roles_get():
    market_roles = g.sess.query(MarketRole).order_by(MarketRole.code).all()
    return render_template('market_roles.html', market_roles=market_roles)

@e.route('/meter_payment_types')
def meter_payment_types_get():
    meter_payment_types = g.sess.query(MeterPaymentType).order_by(MeterPaymentType.code).all()
    return render_template('meter_payment_types.html', meter_payment_types=meter_payment_types)

@e.route('/meter_payment_types/<int:type_id>')
def meter_payment_type_get(type_id):
    meter_payment_type = MeterPaymentType.get_by_id(g.sess, type_id)
    return render_template('meter_payment_type.html', meter_payment_type=meter_payment_type)

@e.route('/meter_types')
def meter_types_get():
    meter_types = g.sess.query(MeterType).order_by(MeterType.code)
    return render_template('meter_types.html', meter_types=meter_types)

@e.route('/meter_types/<int:meter_type_id>')
def meter_type_get(meter_type_id):
    meter_type = MeterType.get_by_id(g.sess, meter_type_id)
    return render_template('meter_type.html', meter_type=meter_type)

@e.route('/mop_batches')
def mop_batches_get():
    contract_id = req_int('mop_contract_id')
    contract = Contract.get_mop_by_id(g.sess, contract_id)
    batches = g.sess.execute(select(Batch, func.count(Bill.id), func.coalesce(func.sum(Bill.net), 0), func.coalesce(func.sum(Bill.vat), 0), func.coalesce(func.sum(Bill.gross), 0)).join(Bill, isouter=True).where(Batch.contract == contract).group_by(Batch.id).order_by(Batch.reference.desc()))
    return render_template('mop_batches.html', contract=contract, batches=batches)

@e.route('/mop_contracts/<int:contract_id>/add_batch')
def mop_batch_add_get(contract_id):
    contract = Contract.get_mop_by_id(g.sess, contract_id)
    batches = g.sess.query(Batch).filter(Batch.contract == contract).order_by(Batch.reference.desc())
    next_batch_reference, next_batch_description = contract.get_next_batch_details(g.sess)
    return render_template('mop_batch_add.html', contract=contract, batches=batches, next_batch_reference=next_batch_reference, next_batch_description=next_batch_description)

@e.route('/mop_contracts/<int:contract_id>/add_batch', methods=['POST'])
def mop_batch_add_post(contract_id):
    try:
        contract = Contract.get_mop_by_id(g.sess, contract_id)
        reference = req_str('reference')
        description = req_str('description')
        batch = contract.insert_batch(g.sess, reference, description)
        g.sess.commit()
        return chellow_redirect(f'/mop_batches/{batch.id}', 303)
    except BadRequest as e:
        flash(e.description)
        batches = g.sess.query(Batch).filter(Batch.contract == contract).order_by(Batch.reference.desc())
        return make_response(render_template('mop_batch_add.html', contract=contract, batches=batches), 303)

@e.route('/mop_batches/<int:batch_id>/edit')
def mop_batch_edit_get(batch_id):
    batch = Batch.get_by_id(g.sess, batch_id)
    return render_template('mop_batch_edit.html', batch=batch)

@e.route('/mop_batches/<int:batch_id>/edit', methods=['POST'])
def mop_batch_edit_post(batch_id):
    try:
        batch = Batch.get_by_id(g.sess, batch_id)
        if 'delete' in request.values:
            contract = batch.contract
            batch.delete(g.sess)
            g.sess.commit()
            return chellow_redirect(f'/mop_contracts/{contract.id}', 303)
        elif 'delete_bills' in request.values:
            g.sess.query(Bill).filter(Bill.batch_id == batch.id).delete(False)
            g.sess.commit()
            return chellow_redirect(f'/mop_batches/{batch.id}', 303)
        else:
            reference = req_str('reference')
            description = req_str('description')
            batch.update(g.sess, reference, description)
            g.sess.commit()
            return chellow_redirect(f'/mop_batches/{batch.id}', 303)
    except BadRequest as e:
        flash(e.description)
        return render_template('mop_batch_edit.html', batch=batch)

@e.route('/mop_batches/<int:batch_id>')
def mop_batch_get(batch_id):
    batch = Batch.get_mop_by_id(g.sess, batch_id)
    bills = g.sess.query(Bill).filter(Bill.batch == batch).order_by(Bill.reference).all()
    config_contract = Contract.get_non_core_by_name(g.sess, 'configuration')
    properties = config_contract.make_properties()
    importer_ids = sorted(chellow.e.bill_importer.get_bill_import_ids(batch), reverse=True)
    fields = {'batch': batch, 'bills': bills, 'importer_ids': importer_ids}
    if 'batch_reports' in properties:
        batch_reports = []
        for report_id in properties['batch_reports']:
            batch_reports.append(Report.get_by_id(g.sess, report_id))
        fields['batch_reports'] = batch_reports
    return render_template('mop_batch.html', **fields)

@e.route('/mop_batches/<int:batch_id>', methods=['POST'])
def mop_batch_post(batch_id):
    try:
        batch = Batch.get_by_id(g.sess, batch_id)
        if 'import_bills' in request.values:
            import_id = chellow.e.bill_importer.start_bill_import(batch)
            return chellow_redirect(f'/mop_bill_imports/{import_id}', 303)
        elif 'delete_bills' in request.values:
            g.sess.query(Bill).filter(Bill.batch_id == batch.id).delete(False)
            g.sess.commit()
            return chellow_redirect(f'/mop_batches/{batch.id}', 303)
        elif 'delete_import_bills' in request.values:
            g.sess.query(Bill).filter(Bill.batch_id == batch.id).delete(False)
            g.sess.commit()
            import_id = chellow.bill_importer.start_bill_import(batch)
            return chellow_redirect(f'/mop_bill_imports/{import_id}', 303)
    except BadRequest as e:
        flash(e.description)
        importer_ids = sorted(chellow.e.bill_importer.get_bill_import_ids(batch), reverse=True)
        parser_names = chellow.e.bill_importer.find_parser_names()
        return make_response(render_template('mop_batch.html', batch=batch, importer_ids=importer_ids, parser_names=parser_names), 400)

@e.route('/mop_batches/<int:batch_id>/csv')
def mop_batch_csv_get(batch_id):
    batch = Batch.get_by_id(g.sess, batch_id)
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['MOP Contract', 'Batch Reference', 'Bill Reference', 'Account', 'Issued', 'From', 'To', 'kWh', 'Net', 'VAT', 'Gross', 'Type'])
    for bill in g.sess.query(Bill).filter(Bill.batch == batch).order_by(Bill.reference, Bill.start_date).options(joinedload(Bill.bill_type)):
        cw.writerow([batch.contract.name, batch.reference, bill.reference, bill.account, hh_format(bill.issue_date), hh_format(bill.start_date), hh_format(bill.finish_date), str(bill.kwh), str(bill.net), str(bill.vat), str(bill.gross), bill.bill_type.code])
    output = make_response(si.getvalue())
    output.headers['Content-Disposition'] = 'attachment; filename="batch.csv"'
    output.headers['Content-type'] = 'text/csv'
    return output

@e.route('/mop_batches/<int:batch_id>/upload_file')
def mop_batch_upload_file_get(batch_id):
    batch = Batch.get_by_id(g.sess, batch_id)
    parser_names = chellow.e.bill_importer.find_parser_names()
    return render_template('mop_batch_upload_file.html', batch=batch, parser_names=parser_names)

@e.route('/mop_batches/<int:batch_id>/upload_file', methods=['POST'])
def mop_batch_upload_file_post(batch_id):
    batch = None
    try:
        batch = Batch.get_by_id(g.sess, batch_id)
        file_item = request.files['import_file']
        parser_name = req_str('parser_name')
        batch_file = batch.insert_file(g.sess, file_item.filename, file_item.stream.read(), parser_name)
        g.sess.commit()
        return chellow_redirect(f'/mop_batches/{batch.id}#batch_file_{batch_file.id}', 303)
    except BadRequest as e:
        flash(e.description)
        parser_names = chellow.e.bill_importer.find_parser_names()
        return make_response(render_template('mop_batch_upload_file.html', batch=batch, parser_names=parser_names), 400)

@e.route('/mop_batch_files/<int:file_id>')
def mop_batch_file_get(file_id):
    batch_file = BatchFile.get_by_id(g.sess, file_id)
    importer_ids = sorted(chellow.e.bill_importer.get_bill_import_ids(batch_file), reverse=True)
    return render_template('mop_batch_file.html', batch_file=batch_file, importer_ids=importer_ids)

@e.route('/mop_batch_files/<int:file_id>/download')
def mop_batch_file_download_get(file_id):
    batch_file = BatchFile.get_by_id(g.sess, file_id)
    output = make_response(batch_file.data)
    output.headers['Content-Disposition'] = f'attachment; filename="{batch_file.filename}"'
    output.headers['Content-type'] = 'application/octet-stream'
    return output

@e.route('/mop_batch_files/<int:file_id>/edit')
def mop_batch_file_edit_get(file_id):
    batch_file = BatchFile.get_by_id(g.sess, file_id)
    parser_names = chellow.e.bill_importer.find_parser_names()
    return render_template('mop_batch_file_edit.html', batch_file=batch_file, parser_names=parser_names)

@e.route('/mop_batch_files/<int:file_id>/edit', methods=['POST'])
def mop_batch_file_edit_post(file_id):
    batch_file = None
    try:
        batch_file = BatchFile.get_by_id(g.sess, file_id)
        if 'delete' in request.values:
            batch_id = batch_file.batch.id
            batch_file.delete(g.sess)
            g.sess.commit()
            flash('Deletion successful')
            return chellow_redirect(f'/mop_batches/{batch_id}', 303)
        else:
            parser_name = req_str('parser_name')
            batch_file.update(parser_name)
            g.sess.commit()
            flash('Update successful')
            return chellow_redirect(f'/mop_batch_files/{batch_file.id}', 303)
    except BadRequest as e:
        flash(e.description)
        parser_names = chellow.e.bill_importer.find_parser_names()
        return make_response(render_template('mop_batch_file_edit.html', batch_file=batch_file, parser_names=parser_names), 400)

@e.route('/mop_bills/<int:bill_id>')
def mop_bill_get(bill_id):
    bill = Bill.get_by_id(g.sess, bill_id)
    register_reads = g.sess.query(RegisterRead).filter(RegisterRead.bill == bill).order_by(RegisterRead.present_date.desc())
    fields = {'bill': bill, 'register_reads': register_reads}
    try:
        breakdown_dict = loads(bill.breakdown)
        raw_lines = []
        for key in ('raw_lines', 'raw-lines'):
            try:
                raw_lines += breakdown_dict[key]
                del breakdown_dict[key]
            except KeyError:
                pass
        rows = set()
        columns = set()
        grid = defaultdict(dict)
        for k, v in tuple(breakdown_dict.items()):
            if k.endswith('-gbp'):
                columns.add('gbp')
                row_name = k[:-4]
                rows.add(row_name)
                grid[row_name]['gbp'] = v
                del breakdown_dict[k]
        for k, v in tuple(breakdown_dict.items()):
            for row_name in sorted(list(rows), key=len, reverse=True):
                if k.startswith(row_name + '-'):
                    col_name = k[len(row_name) + 1:]
                    columns.add(col_name)
                    grid[row_name][col_name] = csv_make_val(v)
                    del breakdown_dict[k]
                    break
        for k, v in breakdown_dict.items():
            pair = k.split('-')
            row_name = '-'.join(pair[:-1])
            column_name = pair[-1]
            rows.add(row_name)
            columns.add(column_name)
            grid[row_name][column_name] = csv_make_val(v)
        column_list = sorted(list(columns))
        for rate_name in [col for col in column_list if col.endswith('rate')]:
            column_list.remove(rate_name)
            column_list.append(rate_name)
        if 'gbp' in column_list:
            column_list.remove('gbp')
            column_list.append('gbp')
        row_list = sorted(list(rows))
        fields.update({'raw_lines': raw_lines, 'row_list': row_list, 'column_list': column_list, 'grid': grid})
    except SyntaxError:
        pass
    return render_template('mop_bill.html', **fields)

@e.route('/mop_bills/<int:bill_id>/edit')
def mop_bill_edit_get(bill_id):
    bill_types = g.sess.query(BillType).order_by(BillType.code).all()
    bill = Bill.get_by_id(g.sess, bill_id)
    return render_template('mop_bill_edit.html', bill=bill, bill_types=bill_types)

@e.route('/mop_bills/<int:bill_id>/edit', methods=['POST'])
def mop_bill_edit_post(bill_id):
    try:
        bill = Bill.get_by_id(g.sess, bill_id)
        if 'delete' in request.values:
            bill.delete(g.sess)
            g.sess.commit()
            return chellow_redirect(f'/mop_batches/{bill.batch.id}', 303)
        else:
            account = req_str('account')
            reference = req_str('reference')
            issue_date = req_date('issue')
            start_date = req_date('start')
            finish_date = req_date('finish')
            kwh = req_decimal('kwh')
            net = req_decimal('net')
            vat = req_decimal('vat')
            gross = req_decimal('gross')
            type_id = req_int('bill_type_id')
            breakdown = req_zish('breakdown')
            bill_type = BillType.get_by_id(g.sess, type_id)
            bill.update(account, reference, issue_date, start_date, finish_date, kwh, net, vat, gross, bill_type, breakdown)
            g.sess.commit()
            return chellow_redirect(f'/mop_bills/{bill.id}', 303)
    except BadRequest as e:
        flash(e.description)
        bill_types = g.sess.query(BillType).order_by(BillType.code).all()
        return render_template('mop_bill_edit.html', bill=bill, bill_types=bill_types)

@e.route('/mop_bill_imports/<int:import_id>')
def mop_bill_import_get(import_id):
    importer = chellow.e.bill_importer.get_bill_import(import_id)
    batch = Batch.get_by_id(g.sess, importer.batch_id)
    fields = {'batch': batch}
    if importer is not None:
        imp_fields = importer.make_fields()
        if 'successful_bills' in imp_fields and len(imp_fields['successful_bills']) > 0:
            fields['successful_max_registers'] = max((len(bill['reads']) for bill in imp_fields['successful_bills']))
        fields.update(imp_fields)
        fields['status'] = importer.status()
    return render_template('mop_bill_import.html', **fields)

@e.route('/mop_batches/<int:batch_id>/add_bill')
def mop_bill_add_get(batch_id):
    batch = Batch.get_by_id(g.sess, batch_id)
    bill_types = g.sess.query(BillType).order_by(BillType.code)
    bills = g.sess.query(Bill).filter(Bill.batch == batch).order_by(Bill.start_date)
    return render_template('mop_bill_add.html', batch=batch, bill_types=bill_types, bills=bills)

@e.route('/mop_batches/<int:batch_id>/add_bill', methods=['POST'])
def mop_bill_add_post(batch_id):
    try:
        batch = Batch.get_by_id(g.sess, batch_id)
        mpan_core = req_str('mpan_core')
        mpan_core = parse_mpan_core(mpan_core)
        account = req_str('account')
        reference = req_str('reference')
        issue_date = req_date('issue')
        start_date = req_hh_date('start')
        finish_date = req_hh_date('finish')
        kwh = req_decimal('kwh')
        net = req_decimal('net')
        vat = req_decimal('vat')
        gross = req_decimal('gross')
        bill_type_id = req_int('bill_type_id')
        bill_type = BillType.get_by_id(g.sess, bill_type_id)
        breakdown_str = req_str('breakdown')
        breakdown = loads(breakdown_str)
        bill_type = BillType.get_by_id(g.sess, bill_type_id)
        bill = batch.insert_bill(g.sess, account, reference, issue_date, start_date, finish_date, kwh, net, vat, gross, bill_type, breakdown, Supply.get_by_mpan_core(g.sess, mpan_core))
        g.sess.commit()
        return chellow_redirect(f'/mop_bills/{bill.id}', 303)
    except BadRequest as e:
        g.sess.rollback()
        flash(e.description)
        bill_types = g.sess.query(BillType).order_by(BillType.code)
        bills = g.sess.query(Bill).filter(Bill.batch == batch).order_by(Bill.start_date)
        return make_response(render_template('mop_bill_add.html', batch=batch, bill_types=bill_types, bills=bills), 400)

@e.route('/mop_contracts/<int:contract_id>/edit')
def mop_contract_edit_get(contract_id):
    parties = g.sess.query(Party).join(MarketRole).join(Participant).filter(MarketRole.code == 'M').order_by(Participant.code).all()
    initial_date = utc_datetime_now()
    contract = Contract.get_mop_by_id(g.sess, contract_id)
    return render_template('mop_contract_edit.html', contract=contract, parties=parties, initial_date=initial_date)

@e.route('/mop_contracts/<int:contract_id>/edit', methods=['POST'])
def mop_contract_edit_post(contract_id):
    try:
        contract = Contract.get_mop_by_id(g.sess, contract_id)
        if 'update_state' in request.form:
            state = req_zish('state')
            contract.update_state(state)
            g.sess.commit()
            return chellow_redirect(f'/mop_contracts/{contract.id}', 303)
        elif 'ignore_snags' in request.form:
            ignore_date = req_date('ignore')
            g.sess.execute(text('update snag set is_ignored = true from channel, era where snag.channel_id = channel.id and channel.era_id = era.id and era.dc_contract_id = :contract_id and snag.finish_date < :ignore_date'), params=dict(contract_id=contract.id, ignore_date=ignore_date))
            g.sess.commit()
            return chellow_redirect(f'/mop_contracts/{contract.id}', 303)
        elif 'delete' in request.form:
            contract.delete(g.sess)
            g.sess.commit()
            return chellow_redirect('/mop_contracts', 303)
        else:
            party_id = req_int('party_id')
            name = req_str('name')
            charge_script = req_str('charge_script')
            properties = req_zish('properties')
            party = Party.get_by_id(g.sess, party_id)
            contract.update(name, party, charge_script, properties)
            g.sess.commit()
            return chellow_redirect(f'/mop_contracts/{contract.id}', 303)
    except BadRequest as e:
        flash(e.description)
        parties = g.sess.query(Party).join(MarketRole).join(Participant).filter(MarketRole.code == 'M').order_by(Participant.code).all()
        initial_date = utc_datetime_now()
        contract = Contract.get_mop_by_id(g.sess, contract_id)
        return make_response(render_template('mop_contract_edit.html', contract=contract, parties=parties, initial_date=initial_date), 400)

@e.route('/mop_rate_scripts/<int:rate_script_id>')
def mop_rate_script_get(rate_script_id):
    rate_script = RateScript.get_mop_by_id(g.sess, rate_script_id)
    contract = rate_script.contract
    next_rate_script = g.sess.query(RateScript).filter(RateScript.contract == contract, RateScript.start_date > rate_script.start_date).order_by(RateScript.start_date).first()
    previous_rate_script = g.sess.query(RateScript).filter(RateScript.contract == contract, RateScript.start_date < rate_script.start_date).order_by(RateScript.start_date.desc()).first()
    return render_template('mop_rate_script.html', rate_script=rate_script, previous_rate_script=previous_rate_script, next_rate_script=next_rate_script)

@e.route('/mop_rate_scripts/<int:rate_script_id>/edit')
def mop_rate_script_edit_get(rate_script_id):
    rate_script = RateScript.get_mop_by_id(g.sess, rate_script_id)
    rs_example_func = chellow.e.computer.contract_func({}, rate_script.contract, 'rate_script_example')
    rs_example = None if rs_example_func is None else rs_example_func()
    return render_template('mop_rate_script_edit.html', rate_script=rate_script, rate_script_example=rs_example)

@e.route('/mop_rate_scripts/<int:rate_script_id>/edit', methods=['POST'])
def mop_rate_script_edit_post(rate_script_id):
    rate_script = RateScript.get_mop_by_id(g.sess, rate_script_id)
    contract = rate_script.contract
    if 'delete' in request.form:
        contract.delete_rate_script(g.sess, rate_script)
        g.sess.commit()
        return chellow_redirect(f'/mop_contracts/{contract.id}', 303)
    else:
        try:
            script = req_zish('script')
            start_date = req_date('start')
            if 'has_finished' in request.form:
                finish_date = req_date('finish')
            else:
                finish_date = None
            contract.update_rate_script(g.sess, rate_script, start_date, finish_date, script)
            g.sess.commit()
            return chellow_redirect(f'/mop_rate_scripts/{rate_script.id}', 303)
        except BadRequest as e:
            flash(e.description)
            return make_response(render_template('mop_rate_script_edit.html', rate_script=rate_script), 400)

@e.route('/mop_contracts')
def mop_contracts_get():
    mop_contracts = g.sess.query(Contract).join(MarketRole).filter(MarketRole.code == 'M').order_by(Contract.name).all()
    return render_template('mop_contracts.html', mop_contracts=mop_contracts)

@e.route('/mop_contracts/add', methods=['POST'])
def mop_contract_add_post():
    try:
        participant_id = req_int('participant_id')
        name = req_str('name')
        start_date = req_date('start')
        participant = Participant.get_by_id(g.sess, participant_id)
        contract = Contract.insert_mop(g.sess, name, participant, '{}', {}, start_date, None, {})
        g.sess.commit()
        return chellow_redirect(f'/mop_contracts/{contract.id}', 303)
    except BadRequest as e:
        flash(e.description)
        initial_date = utc_datetime_now()
        initial_date = Datetime(initial_date.year, initial_date.month, 1)
        parties = g.sess.query(Party).join(MarketRole).join(Participant).filter(MarketRole.code == 'M').order_by(Participant.code).all()
        return make_response(render_template('mop_contract_add.html', inital_date=initial_date, parties=parties), 400)

@e.route('/mop_contracts/add')
def mop_contract_add_get():
    initial_date = utc_datetime_now()
    initial_date = Datetime(initial_date.year, initial_date.month, 1)
    parties = g.sess.query(Party).join(MarketRole).join(Participant).filter(MarketRole.code == 'M').order_by(Participant.code).all()
    return render_template('mop_contract_add.html', inital_date=initial_date, parties=parties)

@e.route('/mop_contracts/<int:contract_id>')
def mop_contract_get(contract_id):
    contract = Contract.get_mop_by_id(g.sess, contract_id)
    rate_scripts = g.sess.query(RateScript).filter(RateScript.contract == contract).order_by(RateScript.start_date.desc()).all()
    now = utc_datetime_now()
    last_month_start = utc_datetime(now.year, now.month) - relativedelta(months=1)
    last_month_finish = last_month_start + relativedelta(months=1) - HH
    party = contract.party
    return render_template('mop_contract.html', contract=contract, rate_scripts=rate_scripts, last_month_start=last_month_start, last_month_finish=last_month_finish, party=party)

@e.route('/mop_contracts/<int:contract_id>/add_rate_script')
def mop_rate_script_add_get(contract_id):
    contract = Contract.get_mop_by_id(g.sess, contract_id)
    now = utc_datetime_now()
    initial_date = utc_datetime(now.year, now.month)
    return render_template('mop_rate_script_add.html', contract=contract, initial_date=initial_date)

@e.route('/mop_contracts/<int:contract_id>/add_rate_script', methods=['POST'])
def mop_rate_script_add_post(contract_id):
    try:
        contract = Contract.get_mop_by_id(g.sess, contract_id)
        start_date = req_date('start')
        rate_script = contract.insert_rate_script(g.sess, start_date, {})
        g.sess.commit()
        return chellow_redirect(f'/mop_rate_scripts/{rate_script.id}', 303)
    except BadRequest as e:
        flash(e.description)
        now = utc_datetime_now()
        initial_date = utc_datetime(now.year, now.month)
        return make_response(render_template('mop_rate_script_add.html', contract=contract, initial_date=initial_date), 400)

@e.route('/mtcs')
def mtcs_get():
    mtcs = g.sess.execute(select(Mtc).order_by(Mtc.code)).scalars()
    return render_template('mtcs.html', mtcs=mtcs)

@e.route('/mtcs/<int:mtc_id>')
def mtc_get(mtc_id):
    mtc = g.sess.execute(select(Mtc).where(Mtc.id == mtc_id)).scalar_one()
    return render_template('mtc.html', mtc=mtc)

@e.route('/mtc_participants')
def mtc_participants_get():
    participant_id = req_int('participant_id')
    participant = Participant.get_by_id(g.sess, participant_id)
    mtc_participants = g.sess.execute(select(MtcParticipant).join(Mtc).where(MtcParticipant.participant == participant).order_by(Mtc.code)).scalars()
    dno = participant.get_dno(g.sess)
    return render_template('mtc_participants.html', mtc_participants=mtc_participants, dno=dno)

@e.route('/mtc_participants/csv')
def mtc_participants_csv_get():
    participant_id = req_int('participant_id')
    participant = Participant.get_by_id(g.sess, participant_id)
    titles = ('participant_code', 'code', 'is_common', 'has_related_metering', 'description', 'has_comms', 'is_hh', 'meter_type', 'meter_payment_type', 'tpr_count', 'valid_from', 'valid_to')
    rows = g.sess.execute(select(Participant.code, Mtc.code, Mtc.is_common, Mtc.has_related_metering, MtcParticipant.description, MtcParticipant.has_comms, MtcParticipant.is_hh, MeterType.code, MeterPaymentType.code, MtcParticipant.tpr_count, MtcParticipant.valid_from, MtcParticipant.valid_to).join(Participant).join(Mtc).join(MeterType).join(MeterPaymentType).where(MtcParticipant.participant == participant).order_by(Mtc.code)).all()
    return _csv_response(f'mtc_participants_{participant.code}.csv', titles, rows)

@e.route('/mtc_participants/<int:mtc_participant_id>')
def mtc_participant_get(mtc_participant_id):
    mtc_participant = MtcParticipant.get_by_id(g.sess, mtc_participant_id)
    dno = mtc_participant.participant.get_dno(g.sess)
    return render_template('mtc_participant.html', mtc_participant=mtc_participant, dno=dno)

@e.route('/mtc_sscs')
def mtc_sscs_get():
    participant_id = req_int('participant_id')
    participant = Participant.get_by_id(g.sess, participant_id)
    only_ongoing = req_bool('only_ongoing')
    q = select(MtcSsc).join(MtcParticipant).join(Mtc).join(Ssc).where(MtcParticipant.participant == participant).order_by(Mtc.code, Ssc.code)
    if only_ongoing:
        q = q.where(MtcSsc.valid_to == null())
    mtc_sscs = g.sess.execute(q).scalars()
    dno = participant.get_dno(g.sess)
    return render_template('mtc_sscs.html', mtc_sscs=mtc_sscs, dno=dno)

@e.route('/mtc_sscs/csv')
def mtc_sscs_csv_get():
    participant_id = req_int('participant_id')
    participant = Participant.get_by_id(g.sess, participant_id)
    titles = ('participant_code', 'mtc_code', 'ssc_code', 'valid_from', 'valid_to')
    rows = g.sess.execute(select(Participant.code, Mtc.code, Ssc.code, MtcSsc.valid_from, MtcSsc.valid_to).select_from(MtcSsc).join(MtcParticipant).join(MtcParticipant.participant).join(Mtc).join(Ssc).where(MtcParticipant.participant == participant).order_by(Mtc.code, Ssc.code)).all()
    return _csv_response(f'mtc_sscs_{participant.code}.csv', titles, rows)

@e.route('/mtc_sscs/<int:mtc_ssc_id>')
def mtc_ssc_get(mtc_ssc_id):
    mtc_ssc = MtcSsc.get_by_id(g.sess, mtc_ssc_id)
    dno = mtc_ssc.mtc_participant.participant.get_dno(g.sess)
    return render_template('mtc_ssc.html', mtc_ssc=mtc_ssc, dno=dno)

@e.route('/mtc_llfcs')
def mtc_llfcs_get():
    participant_id = req_int('participant_id')
    participant = Participant.get_by_id(g.sess, participant_id)
    only_ongoing = req_bool('only_ongoing')
    q = select(MtcLlfc).join(MtcParticipant).join(Mtc).join(Llfc).where(MtcParticipant.participant == participant).order_by(Mtc.code, Llfc.code)
    if only_ongoing:
        q = q.where(MtcLlfc.valid_to == null())
    mtc_llfcs = g.sess.execute(q).scalars()
    dno = participant.get_dno(g.sess)
    return render_template('mtc_llfcs.html', mtc_llfcs=mtc_llfcs, dno=dno)

@e.route('/mtc_llfcs/csv')
def mtc_llfcs_csv_get():
    participant_id = req_int('participant_id')
    participant = Participant.get_by_id(g.sess, participant_id)
    titles = ('participant_code', 'mtc_code', 'llfc_code', 'valid_from', 'valid_to')
    rows = g.sess.execute(select(Participant.code, Mtc.code, Llfc.code, MtcLlfc.valid_from, MtcLlfc.valid_to).select_from(MtcLlfc).join(MtcParticipant).join(Participant).join(Mtc).join(Llfc).where(MtcParticipant.participant == participant).order_by(Mtc.code, Llfc.code)).all()
    return _csv_response(f'mtc_sscs_{participant.code}.csv', titles, rows)

@e.route('/mtc_llfcs/<int:mtc_llfc_id>')
def mtc_llfc_get(mtc_llfc_id):
    mtc_llfc = MtcLlfc.get_by_id(g.sess, mtc_llfc_id)
    dno = mtc_llfc.mtc_participant.participant.get_dno(g.sess)
    return render_template('mtc_llfc.html', mtc_llfc=mtc_llfc, dno=dno)

@e.route('/mtc_llfc_ssc_pcs')
def mtc_llfc_ssc_pcs_get():
    dno_id = req_int('dno_id')
    dno = Party.get_dno_by_id(g.sess, dno_id)
    only_ongoing = req_bool('only_ongoing')
    q = select(MtcLlfcSscPc).join(Pc).join(MtcLlfcSsc).join(Llfc).join(MtcSsc).join(Ssc).join(MtcParticipant).join(Mtc).where(Llfc.dno == dno).order_by(Pc.code, Llfc.code, Ssc.code, Mtc.code, MtcLlfcSscPc.valid_from.desc()).options(joinedload(MtcLlfcSscPc.pc), joinedload(MtcLlfcSscPc.mtc_llfc_ssc), joinedload(MtcLlfcSscPc.mtc_llfc_ssc).joinedload(MtcLlfcSsc.llfc), joinedload(MtcLlfcSscPc.mtc_llfc_ssc).joinedload(MtcLlfcSsc.mtc_ssc), joinedload(MtcLlfcSscPc.mtc_llfc_ssc).joinedload(MtcLlfcSsc.mtc_ssc).joinedload(MtcSsc.ssc), joinedload(MtcLlfcSscPc.mtc_llfc_ssc).joinedload(MtcLlfcSsc.mtc_ssc).joinedload(MtcSsc.mtc_participant), joinedload(MtcLlfcSscPc.mtc_llfc_ssc).joinedload(MtcLlfcSsc.mtc_ssc).joinedload(MtcSsc.mtc_participant).joinedload(MtcParticipant.mtc))
    if only_ongoing:
        q = q.where(MtcLlfcSscPc.valid_to == null())
    combos = g.sess.execute(q).scalars()
    return render_template('mtc_llfc_ssc_pcs.html', mtc_llfc_ssc_pcs=combos, dno=dno)

@e.route('/mtc_llfc_ssc_pcs/csv')
def mtc_llfc_ssc_pcs_csv_get():
    dno_id = req_int('dno_id')
    dno = Party.get_dno_by_id(g.sess, dno_id)
    titles = ('dno_code', 'pc_code', 'llfc_code', 'ssc_code', 'mtc_code', 'valid_from', 'valid_to')
    rows = g.sess.execute(select(Party.dno_code, Pc.code, Llfc.code, Ssc.code, Mtc.code, MtcLlfcSscPc.valid_from, MtcLlfcSscPc.valid_to).select_from(MtcLlfcSscPc).join(Pc).join(MtcLlfcSsc).join(Llfc).join(Party).join(MtcSsc).join(Ssc).join(MtcParticipant).join(Mtc).where(Llfc.dno == dno).order_by(Pc.code, Llfc.code, Ssc.code, Mtc.code, MtcLlfcSscPc.valid_from.desc())).all()
    return _csv_response(f'mtc_llfc_ssc_pcs_{dno.dno_code}.csv', titles, rows)

@e.route('/mtc_llfc_ssc_pcs/<int:combo_id>')
def mtc_llfc_ssc_pc_get(combo_id):
    combo = MtcLlfcSscPc.get_by_id(g.sess, combo_id)
    return render_template('mtc_llfc_ssc_pc.html', mtc_llfc_ssc_pc=combo)

@e.route('/mtc_llfc_sscs')
def mtc_llfc_sscs_get():
    participant_id = req_int('participant_id')
    participant = Participant.get_by_id(g.sess, participant_id)
    only_ongoing = req_bool('only_ongoing')
    q = select(MtcLlfcSsc).join(Llfc).join(MtcSsc).join(Ssc).join(MtcParticipant).join(Mtc).where(MtcParticipant.participant == participant).order_by(Llfc.code, Ssc.code, Mtc.code, MtcLlfcSsc.valid_from.desc()).options(joinedload(MtcLlfcSsc.llfc), joinedload(MtcLlfcSsc.mtc_ssc), joinedload(MtcLlfcSsc.mtc_ssc).joinedload(MtcSsc.ssc), joinedload(MtcLlfcSsc.mtc_ssc).joinedload(MtcSsc.mtc_participant), joinedload(MtcLlfcSsc.mtc_ssc).joinedload(MtcSsc.mtc_participant).joinedload(MtcParticipant.mtc))
    if only_ongoing:
        q = q.where(MtcLlfcSsc.valid_to == null())
    combos = g.sess.execute(q).scalars()
    dno = participant.get_dno(g.sess)
    return render_template('mtc_llfc_sscs.html', mtc_llfc_sscs=combos, dno=dno)

@e.route('/mtc_llfc_sscs/csv')
def mtc_llfc_sscs_csv_get():
    participant_id = req_int('participant_id')
    participant = Participant.get_by_id(g.sess, participant_id)
    titles = ('participant_code', 'llfc_code', 'ssc_code', 'mtc_code', 'valid_from', 'valid_to')
    rows = g.sess.execute(select(Participant.code, Llfc.code, Ssc.code, Mtc.code, MtcLlfcSsc.valid_from, MtcLlfcSsc.valid_to).select_from(MtcLlfcSsc).join(MtcSsc).join(MtcParticipant).join(Participant).join(Mtc).join(Llfc).join(Ssc).where(MtcParticipant.participant == participant).order_by(Llfc.code, Ssc.code, Mtc.code, MtcLlfcSsc.valid_from.desc())).all()
    return _csv_response(f'mtc_llfc_sscs_{participant.code}.csv', titles, rows)

@e.route('/mtc_llfc_sscs/<int:combo_id>')
def mtc_llfc_ssc_get(combo_id):
    combo = MtcLlfcSsc.get_by_id(g.sess, combo_id)
    dno = combo.mtc_ssc.mtc_participant.participant.get_dno(g.sess)
    return render_template('mtc_llfc_ssc.html', mtc_llfc_ssc=combo, dno=dno)

@e.route('/ods_monthly_duration')
def ods_monthly_duration_get():
    now = Datetime.utcnow()
    month_start = Datetime(now.year, now.month, 1) - relativedelta(months=1)
    month_finish = Datetime(now.year, now.month, 1) - HH
    return render_template('ods_monthly_duration.html', month_start=month_start, month_finish=month_finish)

@e.route('/participants/<int:participant_id>')
def participant_get(participant_id):
    participant = Participant.get_by_id(g.sess, participant_id)
    return render_template('participant.html', participant=participant)

@e.route('/participants')
def participants_get():
    participants = g.sess.query(Participant).order_by(Participant.code).all()
    return render_template('participants.html', participants=participants)

@e.route('/parties/<int:party_id>')
def party_get(party_id):
    party = Party.get_by_id(g.sess, party_id)
    return render_template('party.html', party=party)

@e.route('/parties')
def parties_get():
    return render_template('parties.html', parties=g.sess.query(Party).join(MarketRole).order_by(Party.name, MarketRole.code).all())

@e.route('/pcs')
def pcs_get():
    return render_template('pcs.html', pcs=g.sess.query(Pc).order_by(Pc.code))

@e.route('/pcs/<int:pc_id>')
def pc_get(pc_id):
    pc = Pc.get_by_id(g.sess, pc_id)
    return render_template('pc.html', pc=pc)

@e.route('/supplier_bills/<int:bill_id>/add_read')
def read_add_get(bill_id):
    read_types = g.sess.query(ReadType).order_by(ReadType.code)
    estimated_read_type_id = g.sess.query(ReadType.id).filter(ReadType.code == 'E').scalar()
    tprs = g.sess.query(Tpr).order_by(Tpr.code)
    bill = Bill.get_by_id(g.sess, bill_id)
    coefficient = 1
    mpan_str = msn = previous_date = previous_value = previous_type_id = None
    era = bill.supply.find_era_at(g.sess, bill.start_date)
    if era is not None:
        era_properties = PropDict(f'{chellow.utils.url_root}eras/{era.id}', loads(era.properties))
        try:
            coefficient = float(era_properties['coefficient'])
        except KeyError:
            pass
        mpan_str = era.imp_mpan_core
        msn = era.msn
    prev_read = g.sess.query(RegisterRead).join(Bill).filter(Bill.supply == bill.supply, RegisterRead.present_date <= bill.finish_date).order_by(RegisterRead.present_date.desc()).first()
    if prev_read is not None:
        previous_date = prev_read.present_date
        previous_value = prev_read.present_value
        previous_type_id = prev_read.present_type.id
    return render_template('read_add.html', bill=bill, read_types=read_types, tprs=tprs, coefficient=coefficient, mpan_str=mpan_str, msn=msn, previous_date=previous_date, previous_value=previous_value, previous_type_id=previous_type_id, estimated_read_type_id=estimated_read_type_id)

@e.route('/supplier_bills/<int:bill_id>/add_read', methods=['POST'])
def read_add_post(bill_id):
    try:
        bill = Bill.get_by_id(g.sess, bill_id)
        tpr_id = req_int('tpr_id')
        tpr = Tpr.get_by_id(g.sess, tpr_id)
        coefficient = req_decimal('coefficient')
        units_str = req_str('units')
        msn = req_str('msn')
        mpan_str = req_str('mpan')
        previous_date = req_date('previous')
        previous_value = req_decimal('previous_value')
        previous_type_id = req_int('previous_type_id')
        previous_type = ReadType.get_by_id(g.sess, previous_type_id)
        present_date = req_date('present')
        present_value = req_decimal('present_value')
        present_type_id = req_int('present_type_id')
        present_type = ReadType.get_by_id(g.sess, present_type_id)
        bill.insert_read(g.sess, tpr, coefficient, units_str, msn, mpan_str, previous_date, previous_value, previous_type, present_date, present_value, present_type)
        g.sess.commit()
        return chellow_redirect(f'/supplier_bills/{bill.id}', 303)
    except BadRequest as e:
        flash(e.description)
        read_types = g.sess.query(ReadType).order_by(ReadType.code)
        tprs = g.sess.query(Tpr).order_by(Tpr.code)
        return make_response(render_template('read_add.html', bill=bill, read_types=read_types, tprs=tprs), 400)

@e.route('/reads/<int:read_id>/edit')
def read_edit_get(read_id):
    read = RegisterRead.get_by_id(g.sess, read_id)
    read_types = g.sess.query(ReadType).order_by(ReadType.code).all()
    tprs = g.sess.query(Tpr).order_by(Tpr.code).all()
    return render_template('read_edit.html', read=read, read_types=read_types, tprs=tprs)

@e.route('/reads/<int:read_id>/edit', methods=['POST'])
def read_edit_post(read_id):
    try:
        read = RegisterRead.get_by_id(g.sess, read_id)
        if 'update' in request.values:
            tpr_id = req_int('tpr_id')
            tpr = Tpr.get_by_id(g.sess, tpr_id)
            coefficient = req_decimal('coefficient')
            units = req_str('units')
            msn = req_str('msn')
            mpan_str = req_str('mpan')
            previous_date = req_date('previous')
            previous_value = req_decimal('previous_value')
            previous_type_id = req_int('previous_type_id')
            previous_type = ReadType.get_by_id(g.sess, previous_type_id)
            present_date = req_date('present')
            present_value = req_decimal('present_value')
            present_type_id = req_int('present_type_id')
            present_type = ReadType.get_by_id(g.sess, present_type_id)
            read.update(tpr, coefficient, units, msn, mpan_str, previous_date, previous_value, previous_type, present_date, present_value, present_type)
            g.sess.commit()
            return chellow_redirect(f'/supplier_bills/{read.bill.id}', 303)
        elif 'delete' in request.values:
            bill = read.bill
            read.delete(g.sess)
            g.sess.commit()
            return chellow_redirect(f'/supplier_bills/{bill.id}', 303)
    except BadRequest as e:
        flash(e.description)
        read_types = g.sess.query(ReadType).order_by(ReadType.code).all()
        tprs = g.sess.query(Tpr).order_by(Tpr.code).all()
        return make_response(render_template('read_edit.html', read=read, read_types=read_types, tprs=tprs), 400)

@e.route('/read_types')
def read_types_get():
    read_types = g.sess.query(ReadType).order_by(ReadType.code)
    return render_template('read_types.html', read_types=read_types)

@e.route('/read_types/<int:read_type_id>')
def read_type_get(read_type_id):
    read_type = ReadType.get_by_id(g.sess, read_type_id)
    return render_template('read_type.html', read_type=read_type)

@e.route('/scenarios')
def scenarios_get():
    scenarios = g.sess.query(Scenario).order_by(Scenario.name).all()
    return render_template('scenarios.html', scenarios=scenarios)

@e.route('/scenarios/add', methods=['POST'])
def scenario_add_post():
    try:
        name = req_str('name')
        properties = req_zish('properties')
        scenario = Scenario.insert(g.sess, name, properties)
        g.sess.commit()
        return chellow_redirect(f'/scenarios/{scenario.id}', 303)
    except BadRequest as e:
        g.sess.rollback()
        flash(e.description)
        scenarios = g.sess.query(Scenario).order_by(Scenario.name)
        return make_response(render_template('scenario_add.html', scenarios=scenarios), 400)

@e.route('/scenarios/add')
def scenario_add_get():
    now = utc_datetime_now()
    props = {'scenario_start_month': now.month, 'scenario_start_year': now.year, 'scenario_duration': 1}
    return render_template('scenario_add.html', initial_props=dumps(props))

@e.route('/scenarios/<int:scenario_id>')
def scenario_get(scenario_id):
    scenario = Scenario.get_by_id(g.sess, scenario_id)
    return render_template('scenario.html', scenario=scenario)

@e.route('/scenarios/<int:scenario_id>/edit')
def scenario_edit_get(scenario_id):
    scenario = Scenario.get_by_id(g.sess, scenario_id)
    return render_template('scenario_edit.html', scenario=scenario)

@e.route('/scenarios/<int:scenario_id>/edit', methods=['POST'])
def scenario_edit_post(scenario_id):
    try:
        scenario = Scenario.get_by_id(g.sess, scenario_id)
        name = req_str('name')
        properties = req_zish('properties')
        scenario.update(name, properties)
        g.sess.commit()
        return chellow_redirect(f'/scenarios/{scenario.id}', 303)
    except BadRequest as e:
        g.sess.rollback()
        description = e.description
        flash(description)
        return make_response(render_template('scenario_edit.html', scenario=scenario), 400)

@e.route('/scenarios/<int:scenario_id>/edit', methods=['DELETE'])
def scenario_edit_delete(scenario_id):
    try:
        scenario = Scenario.get_by_id(g.sess, scenario_id)
        scenario.delete(g.sess)
        g.sess.commit()
        res = make_response()
        res.headers['HX-Redirect'] = f'{chellow.utils.url_root}/e/scenarios'
        return res
    except BadRequest as e:
        g.sess.rollback()
        flash(e.description)
        return make_response(render_template('scenario_edit.html', scenario=scenario), 400)

@e.route('/sites/<int:site_id>/energy_management')
def site_energy_management_get(site_id):
    site = Site.get_by_id(g.sess, site_id)
    now = utc_datetime_now()
    last_month = now - relativedelta(months=1)
    eras = g.sess.execute(select(Era).join(SiteEra).join(Supply).join(Party).where(SiteEra.site == site, Era.finish_date == null(), Party.dno_code != '88')).scalars()
    return render_template('em_site.html', site=site, eras=eras, now=now, last_month=last_month)

@e.route('/site_snags')
def site_snags_get():
    snags = g.sess.query(Snag).filter(Snag.is_ignored == false(), Snag.site_id != null()).order_by(Snag.start_date.desc(), Snag.id).all()
    site_count = g.sess.query(Snag).join(Site).filter(Snag.is_ignored == false()).distinct(Site.id).count()
    return render_template('site_snags.html', snags=snags, site_count=site_count)

@e.route('/site_snags/<int:snag_id>/edit')
def site_snag_edit_get(snag_id):
    snag = Snag.get_by_id(g.sess, snag_id)
    return render_template('site_snag_edit.html', snag=snag)

@e.route('/site_snags/<int:snag_id>/edit', methods=['POST'])
def site_snag_edit_post(snag_id):
    try:
        ignore = req_bool('ignore')
        snag = Snag.get_by_id(g.sess, snag_id)
        snag.set_is_ignored(ignore)
        g.sess.commit()
        return chellow_redirect(f'/site_snags/{snag.id}', 303)
    except BadRequest as e:
        g.sess.rollback()
        flash(e.description)
        return make_response(render_template('site_snag_edit.html', snag=snag), 400)

@e.route('/sites/<int:site_id>/site_snags')
def site_site_snags_get(site_id):
    site = Site.get_by_id(g.sess, site_id)
    snags = g.sess.query(Snag).filter(Snag.is_ignored == false(), Snag.site == site).order_by(Snag.start_date.desc(), Snag.id)
    return render_template('site_site_snags.html', site=site, snags=snags)

@e.route('/site_snags/edit')
def site_snags_edit_get():
    return render_template('site_snags_edit.html')

@e.route('/site_snags/edit', methods=['POST'])
def site_snags_edit_post():
    try:
        finish_date = req_date('ignore')
        g.sess.execute('update snag set is_ignored = true where snag.site_id is not null and snag.finish_date < :finish_date', {'finish_date': finish_date})
        g.sess.commit()
        return chellow_redirect('/site_snags', 303)
    except BadRequest as e:
        flash(e.description)
        return make_response(render_template('site_snags_edit.html'), 400)

@e.route('/site_snags/<int:snag_id>')
def site_snag_get(snag_id):
    snag = Snag.get_by_id(g.sess, snag_id)
    return render_template('site_snag.html', snag=snag)

@e.route('/sites/<int:site_id>/energy_management/hh_data')
def em_hh_data_get(site_id):
    caches = {}
    site = Site.get_by_id(g.sess, site_id)
    year = req_int('year')
    month = req_int('month')
    start_date, finish_date = next(c_months_u(start_year=year, start_month=month, months=1))
    supplies = g.sess.execute(select(Supply).join(Era).join(SiteEra).join(Source).join(Party).where(SiteEra.site == site, SiteEra.is_physical == true(), Era.start_date <= finish_date, or_(Era.finish_date == null(), Era.finish_date >= start_date), Source.code != 'sub', Party.dno_code != '88').order_by(Supply.id).distinct().options(joinedload(Supply.source), joinedload(Supply.generator_type))).scalars().all()
    data = iter(g.sess.query(HhDatum).join(Channel).join(Era).filter(Channel.channel_type == 'ACTIVE', Era.supply_id.in_([s.id for s in supplies]), HhDatum.start_date >= start_date, HhDatum.start_date <= finish_date).order_by(HhDatum.start_date, Era.supply_id).options(joinedload(HhDatum.channel).joinedload(Channel.era).joinedload(Era.supply).joinedload(Supply.source)))
    datum = next(data, None)
    hh_data = []
    for hh_date in hh_range(caches, start_date, finish_date):
        sups = []
        hh_dict = {'start_date': hh_date, 'supplies': sups, 'export_kwh': 0, 'import_kwh': 0, 'parasitic_kwh': 0, 'generated_kwh': 0, 'third_party_import_kwh': 0, 'third_party_export_kwh': 0}
        hh_data.append(hh_dict)
        for supply in supplies:
            sup_hh = {}
            sups.append(sup_hh)
            while datum is not None and datum.start_date == hh_date and (datum.channel.era.supply_id == supply.id):
                channel = datum.channel
                imp_related = channel.imp_related
                hh_float_value = float(datum.value)
                source_code = channel.era.supply.source.code
                prefix = 'import_' if imp_related else 'export_'
                sup_hh[prefix + 'kwh'] = datum.value
                sup_hh[prefix + 'status'] = datum.status
                if not imp_related and source_code in ('net', 'gen-net'):
                    hh_dict['export_kwh'] += hh_float_value
                if imp_related and source_code in ('net', 'gen-net'):
                    hh_dict['import_kwh'] += hh_float_value
                if imp_related and source_code == 'gen' or (not imp_related and source_code == 'gen-net'):
                    hh_dict['generated_kwh'] += hh_float_value
                if not imp_related and source_code == 'gen' or (imp_related and source_code == 'gen-net'):
                    hh_dict['parasitic_kwh'] += hh_float_value
                if imp_related and source_code == '3rd-party' or (not imp_related and source_code == '3rd-party-reverse'):
                    hh_dict['third_party_import_kwh'] += hh_float_value
                if not imp_related and source_code == '3rd-party' or (imp_related and source_code == '3rd-party-reverse'):
                    hh_dict['third_party_export_kwh'] += hh_float_value
                datum = next(data, None)
        hh_dict['displaced_kwh'] = hh_dict['generated_kwh'] - hh_dict['export_kwh'] - hh_dict['parasitic_kwh']
        hh_dict['used_kwh'] = sum((hh_dict['import_kwh'], hh_dict['displaced_kwh'], hh_dict['third_party_import_kwh'] - hh_dict['third_party_export_kwh']))
    return render_template('em_hh_data.html', site=site, supplies=supplies, hh_data=hh_data)

@e.route('/sites/<int:site_id>/energy_management/months')
def site_energy_management_months_get(site_id):
    finish_year = req_int('finish_year')
    finish_month = req_int('finish_month')
    site = Site.get_by_id(g.sess, site_id)
    typs = ('imp_net', 'imp_3p', 'exp_net', 'exp_3p', 'used', 'displaced', 'imp_gen', 'exp_gen')
    months = []
    for month_start, month_finish in c_months_u(finish_year=finish_year, finish_month=finish_month, months=12):
        month = dict(((typ, {'md': 0, 'md_date': None, 'kwh': 0}) for typ in typs))
        month['start_date'] = month_start
        month['start_date_ct'] = to_ct(month_start)
        months.append(month)
        for hh in site.hh_data(g.sess, month_start, month_finish, exclude_virtual=True):
            for tp in typs:
                if hh[tp] * 2 > month[tp]['md']:
                    month[tp]['md'] = hh[tp] * 2
                    month[tp]['md_date'] = hh['start_date']
                month[tp]['kwh'] += hh[tp]
        month['has_site_snags'] = g.sess.query(Snag).filter(Snag.site == site, Snag.start_date <= month_finish, or_(Snag.finish_date == null(), Snag.finish_date > month_start)).count() > 0
    totals = dict(((typ, {'md': 0, 'md_date': None, 'kwh': 0}) for typ in typs))
    for month in months:
        for typ in typs:
            if month[typ]['md'] > totals[typ]['md']:
                totals[typ]['md'] = month[typ]['md']
                totals[typ]['md_date'] = month[typ]['md_date']
            totals[typ]['kwh'] += month[typ]['kwh']
    months.append(totals)
    return render_template('em_months.html', site=site, months=months)

@e.route('/sites/<int:site_id>/energy_management/totals')
def em_totals(site_id):
    site = Site.get_by_id(g.sess, site_id)
    if 'mem_id' in request.values:
        mem_id = req_int('mem_id')
        site_info = chellow.dloads.get_mem_val(mem_id)
        random_number = random()
        status_code = 200 if site_info['status'] == 'running' else 286
        return make_response(render_template('em_totals.html', site=site, site_info=site_info, random_number=random_number), status_code)
    else:
        mem_id = chellow.dloads.get_mem_id()
        chellow.dloads.put_mem_val(mem_id, {'status': 'running', 'progress': 0})
        if 'start_year' in request.values:
            start_date = req_date('start')
        else:
            start_date = None
        args = (mem_id, site.id, start_date)
        threading.Thread(target=totals_runner, args=args).start()
        return render_template('em_totals.html', site=site, site_info=None, mem_id=mem_id)

@e.route('/sources')
def sources_get():
    sources = g.sess.query(Source).order_by(Source.code)
    return render_template('sources.html', sources=sources)

@e.route('/sources/<int:source_id>')
def source_get(source_id):
    source = Source.get_by_id(g.sess, source_id)
    return render_template('source.html', source=source)

@e.route('/sscs')
def sscs_get():
    sscs = g.sess.query(Ssc).options(joinedload(Ssc.measurement_requirements).joinedload(MeasurementRequirement.tpr)).order_by(Ssc.code)
    return render_template('sscs.html', sscs=sscs)

@e.route('/sscs/<int:ssc_id>')
def ssc_get(ssc_id):
    ssc = Ssc.get_by_id(g.sess, ssc_id)
    return render_template('ssc.html', ssc=ssc)

@e.route('/supplier_contracts/<int:contract_id>/add_batch')
def supplier_batch_add_get(contract_id):
    contract = Contract.get_supplier_by_id(g.sess, contract_id)
    batches = g.sess.query(Batch).filter(Batch.contract == contract).order_by(Batch.reference.desc())
    next_batch_reference, next_batch_description = contract.get_next_batch_details(g.sess)
    return render_template('supplier_batch_add.html', contract=contract, batches=batches, next_batch_reference=next_batch_reference, next_batch_description=next_batch_description)

@e.route('/supplier_contracts/<int:contract_id>/add_batch', methods=['POST'])
def supplier_batch_add_post(contract_id):
    contract = Contract.get_supplier_by_id(g.sess, contract_id)
    try:
        reference = req_str('reference')
        description = req_str('description')
        batch = contract.insert_batch(g.sess, reference, description)
        g.sess.commit()
        return chellow_redirect(f'/supplier_batches/{batch.id}', 303)
    except BadRequest as e:
        flash(e.description)
        g.sess.rollback()
        batches = g.sess.query(Batch).filter(Batch.contract == contract).order_by(Batch.reference.desc())
        return make_response(render_template('supplier_batch_add.html', contract=contract, batches=batches), 400)

@e.route('/supplier_batches')
def supplier_batches_get():
    contract_id = req_int('supplier_contract_id')
    contract = Contract.get_supplier_by_id(g.sess, contract_id)
    batches = g.sess.execute(select(Batch, func.count(Bill.id), func.coalesce(func.sum(Bill.net), 0), func.coalesce(func.sum(Bill.vat), 0), func.coalesce(func.sum(Bill.gross), 0), func.coalesce(func.sum(Bill.kwh), 0)).join(Bill, isouter=True).where(Batch.contract == contract).group_by(Batch.id).order_by(Batch.reference.desc()))
    return render_template('supplier_batches.html', contract=contract, batches=batches)

@e.route('/supplier_batches/<int:batch_id>')
def supplier_batch_get(batch_id):
    batch = Batch.get_by_id(g.sess, batch_id)
    num_bills, sum_net_gbp, sum_vat_gbp, sum_gross_gbp, sum_kwh = g.sess.query(func.count(Bill.id), func.sum(Bill.net), func.sum(Bill.vat), func.sum(Bill.gross), func.sum(Bill.kwh)).filter(Bill.batch == batch).one()
    if sum_net_gbp is None:
        sum_net_gbp = sum_vat_gbp = sum_gross_gbp = sum_kwh = 0
    if 'bill_limit' in request.values and num_bills > req_int('bill_limit'):
        bills = None
    else:
        bills = g.sess.query(Bill).filter(Bill.batch == batch).order_by(Bill.reference, Bill.start_date).options(joinedload(Bill.bill_type)).all()
    config_contract = Contract.get_non_core_by_name(g.sess, 'configuration')
    properties = config_contract.make_properties()
    if 'batch_reports' in properties:
        batch_reports = []
        for report_id in properties['batch_reports']:
            batch_reports.append(Report.get_by_id(g.sess, report_id))
    else:
        batch_reports = None
    importer_ids = sorted(chellow.e.bill_importer.get_bill_import_ids(batch), reverse=True)
    return render_template('supplier_batch.html', batch=batch, bills=bills, batch_reports=batch_reports, num_bills=num_bills, sum_net_gbp=sum_net_gbp, sum_vat_gbp=sum_vat_gbp, sum_gross_gbp=sum_gross_gbp, sum_kwh=sum_kwh, importer_ids=importer_ids)

@e.route('/supplier_batches/<int:batch_id>/edit')
def supplier_batch_edit_get(batch_id):
    batch = Batch.get_by_id(g.sess, batch_id)
    return render_template('supplier_batch_edit.html', batch=batch)

@e.route('/supplier_batches/<int:batch_id>/edit', methods=['POST'])
def supplier_batch_edit_post(batch_id):
    try:
        batch = Batch.get_by_id(g.sess, batch_id)
        if 'update' in request.values:
            reference = req_str('reference')
            description = req_str('description')
            batch.update(g.sess, reference, description)
            g.sess.commit()
            return chellow_redirect(f'/supplier_batches/{batch.id}', 303)
        elif 'delete' in request.values:
            contract_id = batch.contract.id
            batch.delete(g.sess)
            g.sess.commit()
            return chellow_redirect(f'/supplier_batches?supplier_contract_id={contract_id}', 303)
    except BadRequest as e:
        flash(e.description)
        return make_response(render_template('supplier_batch_edit.html', batch=batch), 400)

@e.route('/supplier_batches/<int:batch_id>', methods=['POST'])
def supplier_batch_post(batch_id):
    try:
        batch = Batch.get_by_id(g.sess, batch_id)
        if 'import_bills' in request.values:
            import_id = chellow.e.bill_importer.start_bill_import(batch)
            return chellow_redirect(f'/supplier_bill_imports/{import_id}', 303)
        elif 'delete_bills' in request.values:
            g.sess.query(Bill).filter(Bill.batch_id == batch.id).delete(False)
            g.sess.commit()
            return chellow_redirect(f'/supplier_batches/{batch.id}', 303)
        elif 'delete_import_bills' in request.values:
            g.sess.query(Bill).filter(Bill.batch_id == batch.id).delete(False)
            g.sess.commit()
            import_id = chellow.e.bill_importer.start_bill_import(batch)
            return chellow_redirect(f'/supplier_bill_imports/{import_id}', 303)
    except BadRequest as e:
        flash(e.description)
        importer_ids = sorted(chellow.e.bill_importer.get_bill_import_ids(batch), reverse=True)
        parser_names = chellow.e.bill_importer.find_parser_names()
        return make_response(render_template('supplier_batch.html', batch=batch, importer_ids=importer_ids, parser_names=parser_names), 400)

@e.route('/supplier_batches/<int:batch_id>/upload_file')
def supplier_batch_upload_file_get(batch_id):
    batch = Batch.get_by_id(g.sess, batch_id)
    parser_names = chellow.e.bill_importer.find_parser_names()
    bf = g.sess.query(BatchFile).join(Batch).filter(Batch.contract == batch.contract).order_by(BatchFile.upload_timestamp.desc()).first()
    default_parser_name = bf.parser_name if bf is not None else None
    return render_template('supplier_batch_upload_file.html', batch=batch, parser_names=parser_names, default_parser_name=default_parser_name)

@e.route('/supplier_batches/<int:batch_id>/upload_file', methods=['POST'])
def supplier_batch_upload_file_post(batch_id):
    batch = None
    try:
        batch = Batch.get_by_id(g.sess, batch_id)
        file_item = request.files['import_file']
        parser_name = req_str('parser_name')
        filename = file_item.filename
        if filename == '':
            raise BadRequest('No file selected')
        batch_file = batch.insert_file(g.sess, filename, file_item.stream.read(), parser_name)
        g.sess.commit()
        return chellow_redirect(f'/supplier_batches/{batch.id}#batch_file_{batch_file.id}', 303)
    except BadRequest as e:
        flash(e.description)
        parser_names = chellow.bill_importer.find_parser_names()
        return make_response(render_template('supplier_batch_upload_file.html', batch=batch, parser_names=parser_names), 400)

@e.route('/supplier_batch_files/<int:file_id>')
def supplier_batch_file_get(file_id):
    batch_file = BatchFile.get_by_id(g.sess, file_id)
    return render_template('supplier_batch_file.html', batch_file=batch_file)

@e.route('/supplier_batch_files/<int:file_id>/download')
def supplier_batch_file_download_get(file_id):
    batch_file = BatchFile.get_by_id(g.sess, file_id)
    output = make_response(batch_file.data)
    output.headers['Content-Disposition'] = f'attachment; filename="{batch_file.filename}"'
    output.headers['Content-type'] = 'application/octet-stream'
    return output

@e.route('/supplier_batch_files/<int:file_id>/edit')
def supplier_batch_file_edit_get(file_id):
    batch_file = BatchFile.get_by_id(g.sess, file_id)
    parser_names = chellow.e.bill_importer.find_parser_names()
    return render_template('supplier_batch_file_edit.html', batch_file=batch_file, parser_names=parser_names)

@e.route('/supplier_batch_files/<int:file_id>/edit', methods=['POST'])
def supplier_batch_file_edit_post(file_id):
    batch_file = None
    try:
        batch_file = BatchFile.get_by_id(g.sess, file_id)
        if 'delete' in request.values:
            batch_id = batch_file.batch.id
            batch_file.delete(g.sess)
            g.sess.commit()
            flash('Deletion successful')
            return chellow_redirect(f'/supplier_batches/{batch_id}', 303)
        else:
            parser_name = req_str('parser_name')
            batch_file.update(parser_name)
            g.sess.commit()
            flash('Update successful')
            return chellow_redirect(f'/supplier_batch_files/{batch_file.id}', 303)
    except BadRequest as e:
        flash(e.description)
        parser_names = chellow.bill_importer.find_parser_names()
        return make_response(render_template('supplier_batch_file_edit.html', batch_file=batch_file, parser_names=parser_names), 400)

@e.route('/supplier_batches/<int:batch_id>/add_bill')
def supplier_bill_add_get(batch_id):
    batch = Batch.get_by_id(g.sess, batch_id)
    bill_types = g.sess.query(BillType).order_by(BillType.code)
    supply = start_date = account = None
    normal_bill_type_id = g.sess.query(BillType.id).filter(BillType.code == 'N').scalar()
    try:
        if 'mpan_core' in request.values:
            mpan_core_raw = req_str('mpan_core')
            mpan_core = mpan_core_raw.strip()
            supply = Supply.get_by_mpan_core(g.sess, mpan_core)
            latest_bill = g.sess.query(Bill).join(Batch).join(Contract).join(MarketRole).filter(Bill.supply == supply, MarketRole.code == 'X').order_by(Bill.start_date.desc()).first()
            if latest_bill is not None:
                start_date = latest_bill.finish_date + HH
                account = latest_bill.account
        return render_template('supplier_bill_add.html', batch=batch, bill_types=bill_types, start_date=start_date, account=account, supply=supply, normal_bill_type_id=normal_bill_type_id)
    except BadRequest as e:
        g.sess.rollback()
        flash(e.description)
        return make_response(render_template('supplier_bill_add.html', batch=batch, bill_types=bill_types, supply=supply, start_date=start_date, account=account, normal_bill_type_id=normal_bill_type_id), 400)

@e.route('/supplier_batches/<int:batch_id>/add_bill', methods=['POST'])
def supplier_bill_add_post(batch_id):
    try:
        batch = Batch.get_by_id(g.sess, batch_id)
        mpan_core = req_str('mpan_core')
        mpan_core = parse_mpan_core(mpan_core)
        account = req_str('account')
        reference = req_str('reference')
        issue_date = req_date('issue')
        start_date = req_hh_date('start')
        finish_date = req_hh_date('finish')
        if finish_date > utc_datetime_now():
            raise BadRequest("The finish date can't be in the future.")
        kwh = req_decimal('kwh')
        net = req_decimal('net')
        vat = req_decimal('vat')
        gross = req_decimal('gross')
        bill_type_id = req_int('bill_type_id')
        bill_type = BillType.get_by_id(g.sess, bill_type_id)
        breakdown_str = req_str('breakdown')
        breakdown = loads(breakdown_str)
        bill_type = BillType.get_by_id(g.sess, bill_type_id)
        bill = batch.insert_bill(g.sess, account, reference, issue_date, start_date, finish_date, kwh, net, vat, gross, bill_type, breakdown, Supply.get_by_mpan_core(g.sess, mpan_core))
        g.sess.commit()
        return chellow_redirect(f'/supplier_bills/{bill.id}', 303)
    except BadRequest as e:
        g.sess.rollback()
        flash(e.description)
        bill_types = g.sess.query(BillType).order_by(BillType.code)
        bills = g.sess.query(Bill).filter(Bill.batch == batch).order_by(Bill.start_date)
        return make_response(render_template('supplier_bill_add.html', batch=batch, bill_types=bill_types, bills=bills), 400)

@e.route('/supplier_bill_imports/<int:import_id>')
def supplier_bill_import_get(import_id):
    importer = chellow.e.bill_importer.get_bill_import(import_id)
    batch = Batch.get_by_id(g.sess, importer.batch_id)
    fields = {}
    if importer is not None:
        imp_fields = importer.make_fields()
        if 'successful_bills' in imp_fields and len(imp_fields['successful_bills']) > 0:
            fields['successful_max_registers'] = max((len(bill['reads']) for bill in imp_fields['successful_bills']))
        fields.update(imp_fields)
        fields['status'] = importer.status()
    return render_template('supplier_bill_import.html', batch=batch, importer=importer, **fields)

@e.route('/supplier_bills/<int:bill_id>')
def supplier_bill_get(bill_id):
    bill = Bill.get_by_id(g.sess, bill_id)
    register_reads = g.sess.query(RegisterRead).filter(RegisterRead.bill == bill).order_by(RegisterRead.present_date.desc())
    rate_scripts = g.sess.query(RateScript).filter(RateScript.contract == bill.batch.contract, RateScript.start_date <= bill.finish_date, or_(RateScript.finish_date == null(), RateScript.finish_date >= bill.start_date)).all()
    fields = {'bill': bill, 'register_reads': register_reads, 'rate_scripts': rate_scripts}
    try:
        breakdown_dict = loads(bill.breakdown)
        raw_lines = []
        for key in ('raw_lines', 'raw-lines'):
            try:
                raw_lines += breakdown_dict[key]
                del breakdown_dict[key]
            except KeyError:
                pass
        rows = set()
        columns = set()
        grid = defaultdict(dict)
        for k, v in tuple(breakdown_dict.items()):
            if k.endswith('-gbp'):
                columns.add('gbp')
                row_name = k[:-4]
                rows.add(row_name)
                grid[row_name]['gbp'] = v
                del breakdown_dict[k]
        for k, v in tuple(breakdown_dict.items()):
            for row_name in sorted(list(rows), key=len, reverse=True):
                if k.startswith(row_name + '-'):
                    col_name = k[len(row_name) + 1:]
                    columns.add(col_name)
                    grid[row_name][col_name] = csv_make_val(v)
                    del breakdown_dict[k]
                    break
        for k, v in breakdown_dict.items():
            pair = k.split('-')
            row_name = '-'.join(pair[:-1])
            column_name = pair[-1]
            rows.add(row_name)
            columns.add(column_name)
            grid[row_name][column_name] = csv_make_val(v)
        column_list = sorted(list(columns))
        for rate_name in [col for col in column_list if col.endswith('rate')]:
            column_list.remove(rate_name)
            column_list.append(rate_name)
        if 'gbp' in column_list:
            column_list.remove('gbp')
            column_list.append('gbp')
        row_list = sorted(list(rows))
        fields.update({'raw_lines': raw_lines, 'row_list': row_list, 'column_list': column_list, 'grid': grid})
    except SyntaxError:
        pass
    return render_template('supplier_bill.html', **fields)

@e.route('/supplier_bills/<int:bill_id>/edit')
def supplier_bill_edit_get(bill_id):
    bill_types = g.sess.query(BillType).order_by(BillType.code).all()
    bill = Bill.get_by_id(g.sess, bill_id)
    return render_template('supplier_bill_edit.html', bill=bill, bill_types=bill_types)

@e.route('/supplier_bills/<int:bill_id>/edit', methods=['POST'])
def supplier_bill_edit_post(bill_id):
    try:
        bill = Bill.get_by_id(g.sess, bill_id)
        if 'delete' in request.values:
            batch = bill.batch
            bill.delete(g.sess)
            g.sess.commit()
            return chellow_redirect(f'/supplier_batches/{batch.id}', 303)
        else:
            account = req_str('account')
            reference = req_str('reference')
            issue_date = req_date('issue')
            start_date = req_date('start')
            finish_date = req_date('finish')
            kwh = req_decimal('kwh')
            net = req_decimal('net')
            vat = req_decimal('vat')
            gross = req_decimal('gross')
            type_id = req_int('bill_type_id')
            breakdown = req_zish('breakdown')
            bill_type = BillType.get_by_id(g.sess, type_id)
            bill.update(account, reference, issue_date, start_date, finish_date, kwh, net, vat, gross, bill_type, breakdown)
            g.sess.commit()
            return chellow_redirect(f'/supplier_bills/{bill.id}', 303)
    except BadRequest as e:
        flash(e.description)
        bill_types = g.sess.query(BillType).order_by(BillType.code).all()
        return make_response(render_template('supplier_bill_edit.html', bill=bill, bill_types=bill_types), 400)

@e.route('/supplier_contracts/<int:contract_id>/edit')
def supplier_contract_edit_get(contract_id):
    contract = Contract.get_supplier_by_id(g.sess, contract_id)
    parties = g.sess.query(Party).join(MarketRole).join(Participant).filter(MarketRole.code == 'X').order_by(Participant.code).all()
    return render_template('supplier_contract_edit.html', contract=contract, parties=parties)

@e.route('/supplier_contracts/<int:contract_id>/edit', methods=['POST'])
def supplier_contract_edit_post(contract_id):
    try:
        contract = Contract.get_supplier_by_id(g.sess, contract_id)
        if 'delete' in request.form:
            contract.delete(g.sess)
            g.sess.commit()
            return chellow_redirect('/supplier_contracts', 303)
        else:
            party_id = req_int('party_id')
            party = Party.get_by_id(g.sess, party_id)
            name = req_str('name')
            charge_script = req_str('charge_script')
            properties = req_zish('properties')
            contract.update(name, party, charge_script, properties)
            g.sess.commit()
            return chellow_redirect(f'/supplier_contracts/{contract.id}', 303)
    except BadRequest as e:
        g.sess.rollback()
        description = e.description
        flash(description)
        if description.startswith("There isn't a contract"):
            raise
        else:
            parties = g.sess.query(Party).join(MarketRole).join(Participant).filter(MarketRole.code == 'X').order_by(Participant.code).all()
            return make_response(render_template('supplier_contract_edit.html', contract=contract, parties=parties), 400)

@e.route('/supplier_rate_scripts/<int:rate_script_id>')
def supplier_rate_script_get(rate_script_id):
    rate_script = RateScript.get_supplier_by_id(g.sess, rate_script_id)
    contract = rate_script.contract
    next_rate_script = g.sess.query(RateScript).filter(RateScript.contract == contract, RateScript.start_date > rate_script.start_date).order_by(RateScript.start_date).first()
    previous_rate_script = g.sess.query(RateScript).filter(RateScript.contract == contract, RateScript.start_date < rate_script.start_date).order_by(RateScript.start_date.desc()).first()
    return render_template('supplier_rate_script.html', previous_rate_script=previous_rate_script, next_rate_script=next_rate_script, rate_script=rate_script)

@e.route('/supplier_rate_scripts/<int:rate_script_id>/edit')
def supplier_rate_script_edit_get(rate_script_id):
    rate_script = RateScript.get_supplier_by_id(g.sess, rate_script_id)
    rs_example_func = chellow.e.computer.contract_func({}, rate_script.contract, 'rate_script_example')
    rs_example = None if rs_example_func is None else rs_example_func()
    return render_template('supplier_rate_script_edit.html', supplier_rate_script=rate_script, rate_script_example=rs_example)

@e.route('/supplier_rate_scripts/<int:rate_script_id>/edit', methods=['POST'])
def supplier_rate_script_edit_post(rate_script_id):
    try:
        rate_script = RateScript.get_supplier_by_id(g.sess, rate_script_id)
        contract = rate_script.contract
        if 'delete' in request.values:
            contract.delete_rate_script(g.sess, rate_script)
            g.sess.commit()
            return chellow_redirect(f'/supplier_contracts/{contract.id}', 303)
        else:
            script = req_zish('script')
            start_date = req_date('start')
            has_finished = req_bool('has_finished')
            finish_date = req_date('finish') if has_finished else None
            contract.update_rate_script(g.sess, rate_script, start_date, finish_date, script)
            g.sess.commit()
            return chellow_redirect(f'/supplier_rate_scripts/{rate_script.id}', 303)
    except BadRequest as e:
        g.sess.rollback()
        flash(e.description)
        return make_response(render_template('supplier_rate_script_edit.html', supplier_rate_script=rate_script), 400)

@e.route('/supplier_contracts')
def supplier_contracts_get():
    contracts = g.sess.query(Contract).join(MarketRole).join(Contract.finish_rate_script).filter(MarketRole.code == 'X').order_by(Contract.name)
    ongoing_contracts = contracts.filter(RateScript.finish_date == null())
    ended_contracts = contracts.filter(RateScript.finish_date != null())
    return render_template('supplier_contracts.html', ongoing_supplier_contracts=ongoing_contracts, ended_supplier_contracts=ended_contracts)

@e.route('/supplier_contracts/add', methods=['POST'])
def supplier_contract_add_post():
    try:
        participant_id = req_int('participant_id')
        participant = Participant.get_by_id(g.sess, participant_id)
        name = req_str('name')
        start_date = req_date('start')
        charge_script = req_str('charge_script')
        properties = req_zish('properties')
        contract = Contract.insert_supplier(g.sess, name, participant, charge_script, properties, start_date, None, {})
        g.sess.commit()
        return chellow_redirect(f'/supplier_contracts/{contract.id}', 303)
    except BadRequest as e:
        g.sess.rollback()
        flash(e.description)
        contracts = g.sess.query(Contract).join(MarketRole).filter(MarketRole.code == 'X').order_by(Contract.name)
        parties = g.sess.query(Party).join(MarketRole, Participant).filter(MarketRole.code == 'X').order_by(Participant.code)
        return make_response(render_template('supplier_contract_add.html', contracts=contracts, parties=parties), 400)

@e.route('/supplier_contracts/add')
def supplier_contract_add_get():
    contracts = g.sess.query(Contract).join(MarketRole).filter(MarketRole.code == 'X').order_by(Contract.name)
    parties = g.sess.query(Party).join(MarketRole, Participant).filter(MarketRole.code == 'X').order_by(Participant.code)
    return render_template('supplier_contract_add.html', contracts=contracts, parties=parties)

@e.route('/supplier_contracts/<int:contract_id>')
def supplier_contract_get(contract_id):
    contract = Contract.get_supplier_by_id(g.sess, contract_id)
    rate_scripts = g.sess.query(RateScript).filter(RateScript.contract == contract).order_by(RateScript.start_date.desc()).all()
    now = Datetime.utcnow() - relativedelta(months=1)
    month_start = Datetime(now.year, now.month, 1)
    month_finish = month_start + relativedelta(months=1) - HH
    return render_template('supplier_contract.html', contract=contract, month_start=month_start, month_finish=month_finish, rate_scripts=rate_scripts)

@e.route('/supplier_contracts/<int:contract_id>/add_rate_script')
def supplier_rate_script_add_get(contract_id):
    now = utc_datetime_now()
    initial_date = utc_datetime(now.year, now.month)
    contract = Contract.get_supplier_by_id(g.sess, contract_id)
    return render_template('supplier_rate_script_add.html', now=now, contract=contract, initial_date=initial_date)

@e.route('/supplier_contracts/<int:contract_id>/add_rate_script', methods=['POST'])
def supplier_rate_script_add_post(contract_id):
    try:
        contract = Contract.get_supplier_by_id(g.sess, contract_id)
        start_date = req_date('start')
        rate_script = contract.insert_rate_script(g.sess, start_date, {})
        g.sess.commit()
        return chellow_redirect(f'/supplier_rate_scripts/{rate_script.id}', 303)
    except BadRequest as e:
        flash(e.description)
        now = utc_datetime_now()
        initial_date = utc_datetime(now.year, now.month)
        return render_template('supplier_rate_script_add.html', now=now, contract=contract, initial_date=initial_date)

@e.route('/supplies/<int:supply_id>', methods=['POST'])
def supply_post(supply_id):
    try:
        supply = Supply.get_by_id(g.sess, supply_id)
        if 'new_msn' in request.form:
            start_date_str = req_str('start_date')
            start_date = parse_hh_start(start_date_str)
            msn = req_str('msn')
            era = supply.find_era_at(g.sess, start_date)
            if era is None:
                raise BadRequest(f"There isn't an era at {start_date}")
            if era.msn == msn:
                raise BadRequest(f'The era at {start_date} already has the MSN {msn}')
            if era.start_date != start_date:
                era = supply.insert_era_at(g.sess, start_date)
            era.msn = msn
            g.sess.commit()
            flash('MSN updated successfully')
            return render_template('supply_post.html')
    except BadRequest as e:
        flash(e.description)
        return render_template('supply_post.html')

@e.route('/supplies/<int:supply_id>')
def supply_get(supply_id):
    debug = ''
    supply = g.sess.query(Supply).filter(Supply.id == supply_id).options(joinedload(Supply.source), joinedload(Supply.generator_type), joinedload(Supply.gsp_group), joinedload(Supply.dno)).first()
    if supply is None:
        raise NotFound(f"There isn't a supply with the id {supply_id}")
    supply = Supply.get_by_id(g.sess, supply_id)
    era_bundles = get_era_bundles(g.sess, supply)
    RELATIVE_YEAR = relativedelta(years=1)
    now = Datetime.utcnow()
    triad_year = (now - RELATIVE_YEAR).year if now.month < 3 else now.year
    this_month_start = Datetime(now.year, now.month, 1)
    last_month_start = this_month_start - relativedelta(months=1)
    last_month_finish = this_month_start - relativedelta(minutes=30)
    batch_reports = []
    config_contract = Contract.get_non_core_by_name(g.sess, 'configuration')
    properties = config_contract.make_properties()
    if 'supply_reports' in properties:
        for report_id in properties['supply_reports']:
            batch_reports.append(Report.get_by_id(g.sess, report_id))
    note = truncated_line = None
    supply_note = {'notes': []} if len(supply.note.strip()) == 0 else loads(supply.note)
    notes = supply_note['notes']
    if len(notes) > 0:
        note = notes[-1]
        lines = note['body'].splitlines()
        if len(lines) > 0:
            line0 = lines[0]
            if len(lines) > 1 or len(line0) > 50:
                truncated_line = line0[:50]
    return render_template('supply.html', triad_year=triad_year, now=now, last_month_start=last_month_start, last_month_finish=last_month_finish, era_bundles=era_bundles, supply=supply, system_properties=properties, truncated_line=truncated_line, note=note, this_month_start=this_month_start, batch_reports=batch_reports, debug=debug)

@e.route('/supplies/<int:supply_id>/months')
def supply_months_get(supply_id):
    supply = Supply.get_by_id(g.sess, supply_id)
    is_import = req_bool('is_import')
    year = req_int('year')
    years = req_int('years')
    month_start = utc_datetime(year - years + 1, 1)
    months = []
    for i in range(12 * years):
        next_month_start = month_start + relativedelta(months=1)
        month_finish = next_month_start - HH
        month_data = {}
        months.append(month_data)
        era = supply.find_era_at(g.sess, month_finish)
        if era is not None:
            mpan_core = era.imp_mpan_core if is_import else era.exp_mpan_core
            if mpan_core is not None:
                month_data['mpan_core'] = mpan_core
                month_data['sc'] = era.imp_sc if is_import else era.exp_sc
        md_kvah = 0
        channel_ids = [c.id for c in g.sess.query(Channel).join(Era).filter(Era.supply == supply, Era.start_date <= month_finish, or_(Era.finish_date == null(), Era.finish_date >= month_start), Channel.imp_related == is_import)]
        s = select(cast(func.max(case([(Channel.channel_type == 'ACTIVE', HhDatum.value)], else_=0)), Float).label('max_active'), cast(func.max(case([(Channel.channel_type.in_(('REACTIVE_IMP', 'REACTIVE_EXP')), HhDatum.value)], else_=0)), Float).label('max_reactive'), HhDatum.start_date).join(Channel, HhDatum.channel_id == Channel.id).filter(Channel.id.in_(channel_ids), HhDatum.start_date >= month_start, HhDatum.start_date <= month_finish).group_by(HhDatum.start_date)
        for kwh, kvarh, hh_date in g.sess.execute(s):
            kvah = (kwh ** 2 + kvarh ** 2) ** 0.5
            if kvah > md_kvah:
                md_kvah = kvah
                month_data['md_kva'] = 2 * md_kvah
                month_data['md_kvar'] = kvarh * 2
                month_data['md_kw'] = kwh * 2
                month_data['md_pf'] = kwh / kvah
                month_data['md_date'] = hh_date
        total_kwh = g.sess.query(func.sum(HhDatum.value)).join(Channel).filter(Channel.id.in_(channel_ids), Channel.channel_type == 'ACTIVE', HhDatum.start_date >= month_start, HhDatum.start_date <= month_finish).scalar()
        if total_kwh is not None:
            month_data['total_kwh'] = float(total_kwh)
        month_data['start_date'] = month_start
        month_start = next_month_start
    return render_template('supply_months.html', supply=supply, months=months, is_import=is_import, now=utc_datetime_now())

@e.route('/supplies/<int:supply_id>/edit')
def supply_edit_get(supply_id):
    supply = Supply.get_by_id(g.sess, supply_id)
    sources = g.sess.query(Source).order_by(Source.code)
    generator_types = g.sess.query(GeneratorType).order_by(GeneratorType.code)
    gsp_groups = g.sess.query(GspGroup).order_by(GspGroup.code)
    eras = g.sess.query(Era).filter(Era.supply == supply).order_by(Era.start_date.desc())
    return render_template('supply_edit.html', supply=supply, sources=sources, generator_types=generator_types, gsp_groups=gsp_groups, eras=eras)

@e.route('/supplies/<int:supply_id>/edit', methods=['POST'])
def supply_edit_post(supply_id):
    try:
        supply = Supply.get_by_id(g.sess, supply_id)
        if 'delete' in request.form:
            site_id = None
            for site_era in supply.eras[-1].site_eras:
                if site_era.is_physical:
                    site_id = site_era.site.id
                    break
            supply.delete(g.sess)
            g.sess.commit()
            return credirect(f'/sites/{site_id}', 303)
        elif 'insert_era' in request.form:
            start_date = req_date('start')
            supply.insert_era_at(g.sess, start_date)
            g.sess.commit()
            return chellow_redirect(f'/supplies/{supply.id}', 303)
        else:
            name = req_str('name')
            source_id = req_int('source_id')
            gsp_group_id = req_int('gsp_group_id')
            source = Source.get_by_id(g.sess, source_id)
            if source.code in ('gen', 'gen-net'):
                generator_type_id = req_int('generator_type_id')
                generator_type = GeneratorType.get_by_id(g.sess, generator_type_id)
            else:
                generator_type = None
            gsp_group = GspGroup.get_by_id(g.sess, gsp_group_id)
            supply.update(name, source, generator_type, gsp_group, supply.dno)
            g.sess.commit()
            return chellow_redirect(f'/supplies/{supply.id}', 303)
    except BadRequest as e:
        g.sess.rollback()
        flash(e.description)
        sources = g.sess.query(Source).order_by(Source.code)
        generator_types = g.sess.query(GeneratorType).order_by(GeneratorType.code)
        gsp_groups = g.sess.query(GspGroup).order_by(GspGroup.code)
        eras = g.sess.query(Era).filter(Era.supply == supply).order_by(Era.start_date.desc())
        return make_response(render_template('supply_edit.html', supply=supply, sources=sources, generator_types=generator_types, gsp_groups=gsp_groups, eras=eras), 400)

@e.route('/supplies/<int:supply_id>/notes')
def supply_notes_get(supply_id):
    supply = Supply.get_by_id(g.sess, supply_id)
    if len(supply.note.strip()) > 0:
        supply_note = loads(supply.note)
    else:
        supply_note = {'notes': []}
    return render_template('supply_notes.html', supply=supply, supply_note=supply_note)

@e.route('/supplies/<int:supply_id>/notes/add')
def supply_note_add_get(supply_id):
    supply = Supply.get_by_id(g.sess, supply_id)
    return render_template('supply_note_add.html', supply=supply)

@e.route('/supplies/<int:supply_id>/notes/add', methods=['POST'])
def supply_note_add_post(supply_id):
    try:
        supply = Supply.get_by_id(g.sess, supply_id)
        body = req_str('body')
        if len(supply.note.strip()) == 0:
            note_dict = {'notes': []}
        else:
            note_dict = loads(supply.note)
        note_dict['notes'].append({'body': body, 'timestamp': utc_datetime_now()})
        supply.note = dumps(note_dict)
        g.sess.commit()
        return chellow_redirect(f'/supplies/{supply_id}', 303)
    except BadRequest as e:
        flash(e.description)
        return make_response(render_template('supply_note_add.html', supply=supply), 400)

@e.route('/supplies/<int:supply_id>/notes/<int:index>/edit')
def supply_note_edit_get(supply_id, index):
    supply = Supply.get_by_id(g.sess, supply_id)
    supply_note = loads(supply.note)
    note = supply_note['notes'][index]
    note['index'] = index
    return render_template('supply_note_edit.html', supply=supply, note=note)

@e.route('/supplies/<int:supply_id>/notes/<int:index>/edit', methods=['DELETE'])
def supply_note_edit_delete(supply_id, index):
    try:
        supply = Supply.get_by_id(g.sess, supply_id)
        supply_note = loads(supply.note)
        del supply_note['notes'][index]
        supply.note = dumps(supply_note)
        g.sess.commit()
        res = make_response()
        res.headers['HX-Redirect'] = f'{chellow.utils.url_root}/e/supplies/{supply_id}/notes'
        return res
    except BadRequest as e:
        flash(e.description)
        supply_note = loads(supply.note)
        note = supply_note['notes'][index]
        note['index'] = index
        return render_template('supply_note_edit.html', supply=supply, note=note)

@e.route('/supplies/<int:supply_id>/notes/<int:index>/edit', methods=['POST'])
def supply_note_edit_post(supply_id, index):
    try:
        supply = Supply.get_by_id(g.sess, supply_id)
        supply_note = loads(supply.note)
        body = req_str('body')
        note = supply_note['notes'][index]
        note['body'] = body
        supply.note = dumps(supply_note)
        g.sess.commit()
        return chellow_redirect(f'/supplies/{supply_id}/notes', 303)
    except BadRequest as e:
        flash(e.description)
        supply_note = loads(supply.note)
        note = supply_note['notes'][index]
        note['index'] = index
        return render_template('supply_note_edit.html', supply=supply, note=note)

@e.route('/supplies/<int:supply_id>/hh_data')
def supply_hh_data_get(supply_id):
    caches = {}
    months = req_int('months')
    finish_year = req_int('finish_year')
    finish_month = req_int('finish_month')
    supply = Supply.get_by_id(g.sess, supply_id)
    month_pairs = list(c_months_u(finish_year=finish_year, finish_month=finish_month, months=months))
    start_date, finish_date = (month_pairs[0][0], month_pairs[-1][1])
    era = g.sess.query(Era).filter(Era.supply == supply, Era.start_date <= finish_date, or_(Era.finish_date == null(), Era.finish_date >= start_date)).order_by(Era.start_date.desc()).first()
    keys = {True: {'ACTIVE': 'import_active', 'REACTIVE_IMP': 'import_reactive_imp', 'REACTIVE_EXP': 'import_reactive_exp'}, False: {'ACTIVE': 'export_active', 'REACTIVE_IMP': 'export_reactive_imp', 'REACTIVE_EXP': 'export_reactive_exp'}}
    hh_data = iter(g.sess.query(HhDatum).join(Channel).join(Era).filter(Era.supply == supply, HhDatum.start_date >= start_date, HhDatum.start_date <= finish_date).order_by(HhDatum.start_date).options(joinedload(HhDatum.channel)))
    hh_lines = []
    hh_datum = next(hh_data, None)
    for hh_date in hh_range(caches, start_date, finish_date):
        hh_line = {'timestamp': hh_date}
        hh_lines.append(hh_line)
        while hh_datum is not None and hh_datum.start_date == hh_date:
            channel = hh_datum.channel
            hh_line[keys[channel.imp_related][channel.channel_type]] = hh_datum
            hh_datum = next(hh_data, None)
    return render_template('supply_hh_data.html', supply=supply, era=era, hh_lines=hh_lines, start_date=start_date, finish_date=finish_date)

@e.route('/supplies/<int:supply_id>/virtual_bill')
def supply_virtual_bill_get(supply_id):
    supply = Supply.get_by_id(g.sess, supply_id)
    start_date = req_date('start')
    finish_date = req_date('finish')
    forecast_date = chellow.computer.forecast_date()
    net_gbp = 0
    caches = {}
    meras = []
    debug = ''
    month_start = utc_datetime(start_date.year, start_date.month)
    while not month_start > finish_date:
        month_finish = month_start + relativedelta(months=1) - HH
        chunk_start = hh_max(start_date, month_start)
        chunk_finish = hh_min(finish_date, month_finish)
        for era in g.sess.query(Era).filter(Era.supply == supply, Era.imp_mpan_core != null(), Era.start_date <= chunk_finish, or_(Era.finish_date == null(), Era.finish_date >= chunk_start)):
            block_start = hh_max(era.start_date, chunk_start)
            block_finish = hh_min(era.finish_date, chunk_finish)
            debug += 'found an era'
            contract = era.imp_supplier_contract
            data_source = chellow.computer.SupplySource(g.sess, block_start, block_finish, forecast_date, era, True, caches)
            headings = ['id', 'supplier_contract', 'account', 'start date', 'finish date']
            data = [data_source.id, contract.name, data_source.supplier_account, data_source.start_date, data_source.finish_date]
            mera = {'headings': headings, 'data': data, 'skip': False}
            meras.append(mera)
            chellow.computer.contract_func(caches, contract, 'virtual_bill')(data_source)
            bill = data_source.supplier_bill
            net_gbp += bill['net-gbp']
            for title in chellow.computer.contract_func(caches, contract, 'virtual_bill_titles')():
                if title == 'consumption-info':
                    del bill[title]
                    continue
                headings.append(title)
                if title in bill:
                    data.append(bill[title])
                    del bill[title]
                else:
                    data.append('')
            for k in sorted(bill.keys()):
                headings.append(k)
                data.append(bill[k])
            if len(meras) > 1 and meras[-2]['headings'] == mera['headings']:
                mera['skip'] = True
        month_start += relativedelta(months=1)
    return render_template('supply_virtual_bill.html', supply=supply, start_date=start_date, finish_date=finish_date, meras=meras, net_gbp=net_gbp)

@e.route('/tprs')
def tprs_get():
    tprs = g.sess.query(Tpr).order_by(Tpr.code).all()
    return render_template('tprs.html', tprs=tprs)

@e.route('/tprs/<int:tpr_id>')
def tpr_get(tpr_id):
    tpr = Tpr.get_by_id(g.sess, tpr_id)
    clock_intervals = g.sess.query(ClockInterval).filter(ClockInterval.tpr == tpr).order_by(ClockInterval.id)
    return render_template('tpr.html', tpr=tpr, clock_intervals=clock_intervals)

def get_era_bundles(sess, supply):
    era_bundles = []
    eras = sess.query(Era).filter(Era.supply == supply).order_by(Era.start_date.desc()).options(joinedload(Era.pc), joinedload(Era.imp_supplier_contract), joinedload(Era.exp_supplier_contract), joinedload(Era.ssc), joinedload(Era.mtc_participant), joinedload(Era.mop_contract), joinedload(Era.dc_contract), joinedload(Era.imp_llfc), joinedload(Era.exp_llfc), joinedload(Era.supply).joinedload(Supply.dno)).all()
    for era in eras:
        imp_mpan_core = era.imp_mpan_core
        exp_mpan_core = era.exp_mpan_core
        physical_site = sess.query(Site).join(SiteEra).filter(SiteEra.is_physical == true(), SiteEra.era == era).one()
        other_sites = sess.query(Site).join(SiteEra).filter(SiteEra.is_physical != true(), SiteEra.era == era).all()
        imp_channels = sess.query(Channel).filter(Channel.era == era, Channel.imp_related == true()).order_by(Channel.channel_type).all()
        exp_channels = sess.query(Channel).filter(Channel.era == era, Channel.imp_related == false()).order_by(Channel.channel_type).all()
        era_bundle = {'era': era, 'physical_site': physical_site, 'other_sites': other_sites, 'imp_channels': imp_channels, 'exp_channels': exp_channels, 'imp_bills': {'bill_dicts': []}, 'exp_bills': {'bill_dicts': []}, 'dc_bills': {'bill_dicts': []}, 'mop_bills': {'bill_dicts': []}}
        era_bundles.append(era_bundle)
        if imp_mpan_core is not None:
            era_bundle['imp_shared_supplier_accounts'] = sess.query(Supply).distinct().join(Era).filter(Supply.id != supply.id, Era.imp_supplier_account == era.imp_supplier_account, Era.imp_supplier_contract == era.imp_supplier_contract).all()
        if exp_mpan_core is not None:
            era_bundle['exp_shared_supplier_accounts'] = sess.query(Supply).join(Era).filter(Era.supply != supply, Era.exp_supplier_account == era.exp_supplier_account, Era.exp_supplier_contract == era.exp_supplier_contract).all()
        if era.pc.code != '00':
            inner_headers = [tpr for tpr in sess.query(Tpr).join(MeasurementRequirement).filter(MeasurementRequirement.ssc == era.ssc).order_by(Tpr.code)]
            if era.pc.code in ['05', '06', '07', '08']:
                inner_headers.append(None)
            era_bundle['imp_bills']['inner_headers'] = inner_headers
            inner_header_codes = [tpr.code if tpr is not None else 'md' for tpr in inner_headers]
        bills = sess.query(Bill).filter(Bill.supply == supply).order_by(Bill.start_date.desc(), Bill.issue_date.desc(), Bill.reference.desc()).options(joinedload(Bill.batch).joinedload(Batch.contract).joinedload(Contract.party).joinedload(Party.market_role), joinedload(Bill.bill_type))
        if era.finish_date is not None and era != eras[0]:
            bills = bills.filter(Bill.start_date <= era.finish_date)
        if era != eras[-1]:
            bills = bills.filter(Bill.start_date >= era.start_date)
        num_outer_cols = 0
        for bill in bills:
            bill_contract = bill.batch.contract
            bill_role_code = bill_contract.party.market_role.code
            if bill_role_code == 'X':
                if exp_mpan_core is not None and bill_contract == era.exp_supplier_contract:
                    bill_group_name = 'exp_bills'
                else:
                    bill_group_name = 'imp_bills'
            elif bill_role_code in ('C', 'D'):
                bill_group_name = 'dc_bills'
            elif bill_role_code == 'M':
                bill_group_name = 'mop_bills'
            else:
                raise BadRequest(f'Bill group name not found for bill_contract_id {bill_contract.id}.')
            bill_group = era_bundle[bill_group_name]
            rows_high = 1
            bill_dict = {'bill': bill}
            bill_group['bill_dicts'].append(bill_dict)
            if bill_group_name == 'imp_bills' and era.pc.code != '00':
                inner_tpr_map = dict(((code, []) for code in inner_header_codes))
                outer_tpr_map = defaultdict(list)
                for read, tpr in sess.query(RegisterRead, Tpr).join(Tpr).filter(RegisterRead.bill == bill).order_by(Tpr.id, RegisterRead.present_date.desc()).options(joinedload(RegisterRead.previous_type), joinedload(RegisterRead.present_type), joinedload(RegisterRead.tpr)):
                    tpr_code = 'md' if tpr is None else tpr.code
                    try:
                        inner_tpr_map[tpr_code].append(read)
                    except KeyError:
                        outer_tpr_map[tpr_code].append(read)
                rows_high = max(chain(map(len, chain(inner_tpr_map.values(), outer_tpr_map.values())), [rows_high]))
                read_rows = []
                bill_dict['read_rows'] = read_rows
                for i in range(rows_high):
                    inner_reads = []
                    row_dict = {'inner_reads': inner_reads, 'outer_reads': []}
                    read_rows.append(row_dict)
                    for tpr_code in inner_header_codes:
                        try:
                            inner_reads.append(inner_tpr_map[tpr_code][i])
                        except IndexError:
                            row_dict['inner_reads'].append(None)
                    for tpr_code, read_list in outer_tpr_map.items():
                        try:
                            row_dict['outer_reads'].append(read_list[i])
                        except IndexError:
                            row_dict['outer_reads'].append(None)
                num_outer_cols = max(num_outer_cols, len(outer_tpr_map))
                bill_dict['rows_high'] = rows_high
        era_bundle['imp_bills']['num_outer_cols'] = num_outer_cols
        era_bundle['exp_bills']['num_outer_cols'] = 0
        for bill_group_name in ('imp_bills', 'exp_bills', 'dc_bills', 'mop_bills'):
            b_dicts = list(reversed(era_bundle[bill_group_name]['bill_dicts']))
            for i, b_dict in enumerate(b_dicts):
                if i < len(b_dicts) - 1:
                    bill = b_dict['bill']
                    next_b_dict = b_dicts[i + 1]
                    next_bill = next_b_dict['bill']
                    if (bill.start_date, bill.finish_date, bill.kwh, bill.net, bill.vat) == (next_bill.start_date, next_bill.finish_date, -1 * next_bill.kwh, -1 * next_bill.net, next_bill.vat) and (not (bill.kwh, bill.net, bill.vat) == (0, 0, 0)) and ('collapsible' not in b_dict):
                        b_dict['collapsible'] = True
                        next_b_dict['first_collapsible'] = True
                        next_b_dict['collapsible'] = True
                        b_dict['collapse_id'] = next_b_dict['collapse_id'] = bill.id
    return era_bundles