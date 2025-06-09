def guess_type_name(value):
    """
    Guess the type name of a serialized value.
    """
    value = str(value)
    if value.upper() in ['TRUE', 'FALSE']:
        return 'BOOLEAN'
    elif re.match('(-)?(\\d+)(\\.\\d+)', value):
        return 'REAL'
    elif re.match('(-)?(\\d+)', value):
        return 'INTEGER'
    elif re.match("\\'((\\'\\')|[^\\'])*\\'", value):
        return 'STRING'
    elif re.match('\\"([^\\\\\\n]|(\\\\.))*?\\"', value):
        return 'UNIQUE_ID'