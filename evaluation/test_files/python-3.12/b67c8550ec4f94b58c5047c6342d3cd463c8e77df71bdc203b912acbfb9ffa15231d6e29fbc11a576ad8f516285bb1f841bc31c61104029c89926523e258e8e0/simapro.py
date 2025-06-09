from ..compatibility import SIMAPRO_BIO_SUBCATEGORIES, SIMAPRO_BIOSPHERE, SIMAPRO_SYSTEM_MODELS
from ..data import get_valid_geonames
from .generic import link_iterable_by_fields, link_technosphere_by_activity_hash
from .locations import GEO_UPDATE
from ..utils import load_json_data_file, rescale_exchange
import copy
import re
import numpy as np
from stats_arrays import LognormalUncertainty
detoxify_pattern = '^(?P<name>.+?)/(?P<geo>[A-Za-z]{2,10})(/I)? [SU]$'
detoxify_re = re.compile(detoxify_pattern)

def sp_allocate_products(db):
    """Create a dataset from each product in a raw SimaPro dataset"""
    new_db = []
    for ds in db:
        products = [exc for exc in ds.get('exchanges', []) if exc['type'] == 'production']
        if ds.get('reference product'):
            new_db.append(ds)
        elif not products:
            ds['error'] = True
            new_db.append(ds)
        elif len(products) == 1:
            product = products[0]
            ds['name'] = ds['reference product'] = product['name']
            ds['unit'] = product['unit']
            ds['production amount'] = product['amount']
            new_db.append(ds)
        else:
            ds['exchanges'] = [exc for exc in ds['exchanges'] if exc['type'] != 'production']
            for product in products:
                product = copy.deepcopy(product)
                if product['allocation']:
                    product['amount'] = product['amount'] * 1 / (product['allocation'] / 100)
                else:
                    product['amount'] = 0
                copied = copy.deepcopy(ds)
                copied['exchanges'].append(product)
                copied['name'] = copied['reference product'] = product['name']
                copied['unit'] = product['unit']
                copied['production amount'] = product['amount']
                new_db.append(copied)
    return new_db

def fix_zero_allocation_products(db):
    """Drop all inputs from allocated products which had zero allocation factors.

    The final production amount is the initial amount times the allocation factor. If this is zero, a singular technosphere matrix is created. We fix this by setting the production amount to one, and deleting all inputs.

    Does not modify datasets with more than one production exchange."""
    for ds in db:
        if len([exc for exc in ds.get('exchanges', []) if exc['type'] == 'production']) == 1 and all((exc['amount'] == 0 for exc in ds.get('exchanges', []) if exc['type'] == 'production')):
            ds['exchanges'] = [exc for exc in ds['exchanges'] if exc['type'] == 'production']
            exc = ds['exchanges'][0]
            exc['amount'] = exc['loc'] = 1
            exc['uncertainty type'] = 0
    return db

def link_technosphere_based_on_name_unit_location(db, external_db_name=None):
    """Link technosphere exchanges based on name, unit, and location. Can't use categories because we can't reliably extract categories from SimaPro exports, only exchanges.

    If ``external_db_name``, link against a different database; otherwise link internally."""
    return link_technosphere_by_activity_hash(db, external_db_name=external_db_name, fields=('name', 'location', 'unit'))

def split_simapro_name_geo(db):
    """Split a name like 'foo/CH U' into name and geo components.

    Sets original name to ``simapro name``."""
    for ds in db:
        match = detoxify_re.match(ds['name'])
        if match:
            gd = match.groupdict()
            ds['simapro name'] = ds['name']
            ds['location'] = gd['geo']
            ds['name'] = ds['reference product'] = gd['name']
        for exc in ds.get('exchanges', []):
            match = detoxify_re.match(exc['name'])
            if match:
                gd = match.groupdict()
                exc['simapro name'] = exc['name']
                exc['location'] = gd['geo']
                exc['name'] = gd['name']
    return db

def normalize_simapro_biosphere_categories(db):
    """Normalize biosphere categories to ecoinvent standard."""
    for ds in db:
        for exc in (exc for exc in ds.get('exchanges', []) if exc['type'] == 'biosphere'):
            cat = SIMAPRO_BIOSPHERE.get(exc['categories'][0], exc['categories'][0])
            if len(exc['categories']) > 1:
                subcat = SIMAPRO_BIO_SUBCATEGORIES.get(exc['categories'][1], exc['categories'][1])
                exc['categories'] = (cat, subcat)
            else:
                exc['categories'] = (cat,)
    return db

def normalize_simapro_biosphere_names(db):
    """Normalize biosphere flow names to ecoinvent standard"""
    mapping = {tuple(x[:2]): x[2] for x in load_json_data_file('simapro-biosphere')}
    for ds in db:
        for exc in (exc for exc in ds.get('exchanges', []) if exc['type'] == 'biosphere'):
            try:
                exc['name'] = mapping[exc['categories'][0], exc['name']]
            except KeyError:
                pass
    return db

def normalize_simapro_formulae(formula, settings):
    """Convert SimaPro formulae to Python"""

    def replace_comma(match):
        return match.group(0).replace(',', '.')
    formula = formula.replace('^', '**')
    if settings and settings.get('Decimal separator') == ',':
        formula = re.sub('\\d,\\d', replace_comma, formula)
    return formula

def change_electricity_unit_mj_to_kwh(db):
    """Change datasets with the string ``electricity`` in their name from units of MJ to kilowatt hour."""
    for ds in db:
        for exc in ds.get('exchanges', []):
            if (exc.get('name', '').lower().startswith('electricity') or exc.get('name', '').lower().startswith('market for electricity')) and exc.get('unit') == 'megajoule':
                exc['unit'] = 'kilowatt hour'
                rescale_exchange(exc, 1 / 3.6)
    return db

def fix_localized_water_flows(db):
    """Change ``Water, BR`` to ``Water``.

    Biosphere flows can't have locations - locations are defined by the activity dataset."""
    locations = set(get_valid_geonames()).union(set(GEO_UPDATE.keys())).union(set(GEO_UPDATE.values()))
    flows = ['Water', 'Water, cooling, unspecified natural origin', 'Water, river', 'Water, turbine use, unspecified natural origin', 'Water, unspecified natural origin', 'Water, well, in ground']
    mapping = {'{}, {}'.format(flow, location): (flow, location) for flow in flows for location in locations}
    for ds in db:
        for exc in ds.get('exchanges', []):
            if exc.get('input') or not exc['type'] == 'biosphere':
                continue
            try:
                flow, location = mapping[exc['name']]
                exc['name'] = flow
                exc['simapro location'] = GEO_UPDATE.get(location, location)
            except KeyError:
                pass
    return db

def set_lognormal_loc_value_uncertainty_safe(db):
    """Make sure ``loc`` value is correct for lognormal uncertainty distributions"""
    for ds in db:
        for exc in ds.get('exchanges', []):
            if exc.get('uncertainty type') == LognormalUncertainty.id:
                exc['loc'] = np.log(abs(exc['amount']))
    return db