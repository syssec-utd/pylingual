"""
Various text-manipulating and formatting utilities.
"""
import re
import sys
import time
import itertools
import locale
import codecs
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
try:
    ENCODING = locale.getdefaultlocale()[1]
except ValueError:
    ENCODING = None
if ENCODING == None:
    ENCODING = 'UTF-8'

def bytes_to_text(s):
    """
    Converts a byte string (as read from, e.g., standard input)
    to a text string.

    In Python 3, this is from type ``bytes`` to ``str``.
    In Python 2, this is, confusingly, from type ``str`` to ``unicode``.

    """
    s = codecs.decode(s, ENCODING)
    if sys.hexversion < 50331648:
        s = codecs.encode(s, 'utf-8')
    return s

def parse_curie_standard_qualified_name(prefixed_name, sep=':'):
    if sep not in prefixed_name:
        raise ValueError("'{}' is not a valid CURIE-standard qualified name".format(prefixed_name))
    return prefixed_name.split(':', 1)
if sys.version_info.major == 2:

    def is_str_type(x):
        return isinstance(x, basestring)
else:

    def is_str_type(x):
        return isinstance(x, str)

def camel_case(s):
    components = s.split('_')
    return components[0] + ''.join((x.title() for x in components[1:]))

def snake_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', '\\1_\\2', name)
    return re.sub('([a-z0-9])([A-Z])', '\\1_\\2', s1).lower()

def unique_taxon_label_map(taxa, taxon_label_map=None, max_label_len=0, logger=None):
    """
    Given a list of taxa, returns a dictionary with the Taxon objects as
    keys and string labels as values, where the labels are guaranteed to
    be unique. If ``taxon_label_map`` is pre-populated (as <Taxon> : 'label'),
    then those labels will be used as the basis for the label composition,
    otherwise the original taxon object label will be used. ``max_label_len``
    can be used to restrict the maximum length of the labels.
    """
    if taxon_label_map is None:
        taxon_label_map = {}
        for t in taxa:
            taxon_label_map[t] = t.label
    labels = []
    for t in taxon_label_map:
        label = taxon_label_map[t]
        idx = 1
        if label in labels:
            candidate_label = label
            while candidate_label in labels:
                idx += 1
                if max_label_len > 0:
                    k = max_label_len - len(str(idx))
                    if k < 1:
                        raise ValueError('Unable to make labels unique with maximum label length of %d' % max_label_len)
                    candidate_label = label[:k] + str(idx)
                else:
                    candidate_label = label + str(idx)
            label = candidate_label
        labels.append(label)
        taxon_label_map[t] = label
    return taxon_label_map

def format_dict_table(*args, **kwargs):
    """
    Returns a (single) string representation of a tuple of dictionaries in a
    table format. This method can read the column names directly off the
    dictionary keys, but if a tuple of these keys is provided in the
    'column_names' variable, then the order of column_names will follow the
    order of the fields/keys in that variable.
    """
    display = format_dict_table_rows(*args, **kwargs)
    if display:
        return '\n'.join(display)
    else:
        return ''

def format_dict_table_rows(rows, column_names=None, max_column_width=None, border_style=2):
    """
    Returns a string representation of a tuple of dictionaries in a
    table format. This method can read the column names directly off the
    dictionary keys, but if a tuple of these keys is provided in the
    'column_names' variable, then the order of column_names will follow
    the order of the fields/keys in that variable.
    """
    if column_names or len(rows) > 0:
        lengths = {}
        rules = {}
        if column_names:
            column_list = column_names
        else:
            try:
                column_list = rows[0].keys()
            except:
                column_list = None
        if column_list:
            border_style = int(border_style)
            if border_style == 0:
                vertical_rule = '  '
                horizontal_rule = ''
                rule_junction = ''
            elif border_style == 1:
                vertical_rule = ' '
                horizontal_rule = '-'
                rule_junction = '-'
            else:
                vertical_rule = ' | '
                horizontal_rule = '-'
                rule_junction = '-+-'
            if border_style >= 3:
                left_table_edge_rule = '| '
                right_table_edge_rule = ' |'
                left_table_edge_rule_junction = '+-'
                right_table_edge_rule_junction = '-+'
            else:
                left_table_edge_rule = ''
                right_table_edge_rule = ''
                left_table_edge_rule_junction = ''
                right_table_edge_rule_junction = ''
            if max_column_width:
                column_list = [c[:max_column_width] for c in column_list]
                trunc_rows = []
                for row in rows:
                    new_row = {}
                    for k in row.keys():
                        new_row[k[:max_column_width]] = str(row[k])[:max_column_width]
                    trunc_rows.append(new_row)
                rows = trunc_rows
            for col in column_list:
                rls = [len(str(row[col])) for row in rows]
                lengths[col] = max(rls + [len(col)])
                rules[col] = horizontal_rule * lengths[col]
            template_elements = ['%%(%s)-%ss' % (col, lengths[col]) for col in column_list]
            row_template = vertical_rule.join(template_elements)
            border_template = rule_junction.join(template_elements)
            full_line = left_table_edge_rule_junction + border_template % rules + right_table_edge_rule_junction
            display = []
            if border_style > 0:
                display.append(full_line)
            display.append(left_table_edge_rule + row_template % dict(zip(column_list, column_list)) + right_table_edge_rule)
            if border_style > 0:
                display.append(full_line)
            for row in rows:
                display.append(left_table_edge_rule + row_template % row + right_table_edge_rule)
            if border_style > 0:
                display.append(full_line)
            return display
        else:
            return ''
    else:
        return ''