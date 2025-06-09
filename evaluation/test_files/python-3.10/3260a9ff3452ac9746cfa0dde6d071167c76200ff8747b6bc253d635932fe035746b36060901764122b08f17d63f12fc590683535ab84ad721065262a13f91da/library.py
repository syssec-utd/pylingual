"""
library.py
====================================
This is the library module of Copper. It contains functions used to parse the JSON library files.
"""
import json, inspect
from copper.units import *
from copper.curves import *
import copper.chiller
location = os.path.dirname(os.path.realpath(__file__))
chiller_lib = os.path.join(location, 'lib', 'chiller_curves.json')

class Library:

    def __init__(self, path=chiller_lib, rating_std='', export=False):
        self.path = path
        self.rating_std = rating_std
        self.data = json.loads(open(self.path, 'r').read())
        for (item, vals) in self.data.items():
            if not vals['full_eff'] is None and vals['condenser_type'] != 'hr_scroll':
                props = inspect.getfullargspec(eval('copper.' + vals['eqp_type'].capitalize()).__init__)[0]
                if 'self' in props:
                    props.remove('self')
                obj_args = {}
                for p in props:
                    if not 'part_eff' in p and (not 'set_of_curves' in p) and (not 'alt' in p):
                        obj_args[p] = vals[p]
                obj_args['part_eff_unit'] = vals['full_eff_unit']
                obj_args['part_eff'] = vals['full_eff']
                obj = eval('copper.' + vals['eqp_type'].capitalize())(**obj_args)
                obj_args['set_of_curves'] = self.get_set_of_curves_by_name(item).curves
                if export:
                    self.get_set_of_curves_by_name(item).export('./curves', fmt='idf')
                if self.rating_std != '':
                    obj_args['part_eff_ref_std'] = self.rating_std
                obj = eval('copper.' + vals['eqp_type'].capitalize())(**obj_args)
                part_eff = obj.calc_rated_eff(eff_type='part', unit=vals['full_eff_unit'])
                if part_eff > -999:
                    vals['part_eff'] = part_eff
                    vals['part_eff_unit'] = vals['full_eff_unit']
                else:
                    if 'part_eff' in vals.keys():
                        del vals['part_eff']
                    if 'part_eff_unit' in vals.keys():
                        del vals['part_eff_unit']

    def load_obj(self, data):
        """Load data for an equipment from the libary.

        :param dict data: Equipment data in a dict format
        :return: Instance of the equipment in Copper (e.g. copper.chiller.Chiller)

        """
        props = inspect.getfullargspec(eval('copper.' + data['eqp_type'].capitalize()).__init__)[0]
        props.remove('self')
        obj_args = {}
        for p in props:
            if not 'part_eff' in p and (not 'set_of_curves' in p) and (not 'alt' in p):
                obj_args[p] = data[p]
        obj_args['part_eff_unit'] = data['full_eff_unit']
        obj_args['part_eff'] = data['full_eff']
        obj = eval('copper.' + data['eqp_type'].capitalize())(**obj_args)
        return obj

    def content(self):
        """Content of a library in a dict format.

        :return: Dictionary of the data contained in a library
        :rtype: dict
        """
        return self.data

    def get_unique_eqp_fields(self):
        """Get all unique values for each field of a particular equipment.

        :return: Dictionary showing all unique values for each equipment field.
        :rtype: dict

        """
        uni_field_val = {}
        for (_, eqp_f) in self.data.items():
            for (field, val) in eqp_f.items():
                if field != 'set_of_curves':
                    if field not in uni_field_val.keys():
                        uni_field_val[field] = [val]
                    else:
                        uni_field_val[field].append(val)
        for (field, val) in uni_field_val.items():
            uni_field_val[field] = set(val)
        return uni_field_val

    def find_set_of_curvess_from_lib(self, filters=[], part_eff_flag=False):
        """Retrieve sets of curves from a library matching specific filters.

        :param list filters: List of filters, represented by tuples (field, val)
        :return: List of sets of curves object matching the filters
        :rtype: list

        """
        eqp_match = self.find_equipment(filters)
        set_of_curvess = []
        for (name, props) in eqp_match.items():
            c_set = SetofCurves()
            eqp_props = inspect.getfullargspec(eval('copper.' + props['eqp_type'].capitalize()).__init__)[0]
            eqp_props.remove('self')
            obj_args = {}
            for p in eqp_props:
                if not 'set_of_curves' in p:
                    if part_eff_flag and 'part_eff' in p:
                        if p == 'part_eff_ref_std':
                            obj_args['part_eff_ref_std'] = 'ahri_550/590'
                        elif p in props.keys():
                            obj_args[p] = props[p]
                    elif 'part_eff' in p or 'alt' in p:
                        pass
                    else:
                        obj_args[p] = props[p]
            obj = eval('copper.' + props['eqp_type'].capitalize())(**obj_args)
            c_set.eqp = obj
            for c_att in list(c_set.__dict__):
                if c_att in list(self.data[name].keys()):
                    c_set.__dict__[c_att] = self.data[name][c_att]
            c_lst = []
            for c in self.data[name]['set_of_curves']:
                c_lst.append(self.get_curve(c, self.data[name], eqp=self.load_obj(self.data[name])))
            c_set.curves = c_lst
            set_of_curvess.append(c_set)
        return set_of_curvess

    def find_equipment(self, filters=[]):
        """Find equipment matching specified filter in the curve library.

        Special filter characters:

        - ~! means "all except..."
        - ! means "do not include..."
        - ~ means "include..."

        :param list filters: List of filters, represented by tuples (field, val)
        :return: Dictionary of field for each equipment matching specified filter
        :rtype: dict

        """
        eqp_match_dict = {}
        for eqp in self.data:
            assertions = []
            for (prop, val) in filters:
                if '~!' in val:
                    assertions.append(val.replace('~!', '').lower().strip() not in self.data[eqp][prop].lower().strip())
                elif '!' in val:
                    assertions.append(self.data[eqp][prop] != val)
                elif '~' in val:
                    assertions.append(val.replace('~', '').lower().strip() in self.data[eqp][prop].lower().strip())
                else:
                    assertions.append(self.data[eqp][prop] == val)
            if all(assertions):
                eqp_match_dict[eqp] = self.data[eqp]
        return eqp_match_dict

    def get_set_of_curves_by_name(self, name):
        """Retrieve set of curves from the library by name.

        :param str name: Curve name
        :return: Set of curves object
        :rtype: SetofCurves

        """
        c_set = SetofCurves()
        c_set.name = name
        c_lst = []
        try:
            for c in self.data[name]['set_of_curves']:
                c_lst.append(self.get_curve(c, self.data[name], eqp=self.load_obj(self.data[name])))
            c_set.curves = c_lst
            return c_set
        except:
            raise ValueError('Cannot find curve in library.')

    def get_curve(self, c, c_name, eqp):
        """Retrieve individual attribute of a curve object.

        :param Curve c: Curve object
        :param str c_name: Name of the curve object
        :param str eqp_type: Type of equipment associated with the curve
        :return: Curve object
        :rtype: Curve

        """
        c_prop = c_name['set_of_curves'][c]
        c_obj = Curve(eqp, c_prop['type'])
        c_obj.out_var = c
        for c_att in list(Curve(eqp, c_prop['type']).__dict__):
            if c_att in list(c_prop.keys()):
                c_obj.__dict__[c_att] = c_prop[c_att]
        return c_obj

    def find_base_curves(self, filters, eqp):
        """Find an existing equipment curve that best matches the equipment.

        :param list filters: List of filters, represented by tuples (field, val)
        :param eqp: Instance of the equipment in Copper (e.g. copper.chiller.Chiller)
        :return: Set of curves object
        :rtype: SetofCurves

        """
        eqp_match = self.find_equipment(filters=filters)
        if len(eqp_match) > 0:
            if len(eqp_match) > 1:
                return self.get_set_of_curves_by_name(self.get_best_match(eqp, eqp_match))
            else:
                return self.get_set_of_curves_by_name(eqp_match)
        else:
            raise ValueError('Could not find a set of curves that matches the specified properties.')

    def get_best_match(self, eqp, matches):
        """Find the set of curves matching the equipment characteristics the best.

        :param eqp: Instance of the equipment in Copper (e.g. copper.chiller.Chiller)
        :param dict matches: All potential matches
        :return: Name of the set of curves that best matches the equipment characteristics
        :rtype: str

        """
        diff = float('inf')
        for (name, val) in matches.items():
            if eqp.type == 'chiller':
                cap = val['ref_cap']
                cap_unit = val['ref_cap_unit']
                eff = val['full_eff']
                eff_unit = matches[name]['full_eff_unit']
                if cap is not None:
                    if cap_unit != eqp.ref_cap_unit:
                        c_unit = Units(cap, cap_unit)
                        cap = c_unit.conversion(eqp.ref_cap_unit)
                        cap_unit = eqp.ref_cap_unit
                    if eff_unit != eqp.full_eff_unit:
                        c_unit = Units(eff, eff_unit)
                        eff = c_unit.conversion(eqp.full_eff_unit)
                        eff_unit = eqp.full_eff_unit
                    c_diff = abs((eqp.ref_cap - cap) / eqp.ref_cap) + abs((eqp.full_eff - eff) / eqp.full_eff)
                    if c_diff < diff:
                        diff = c_diff
                        best_match = name
        return best_match