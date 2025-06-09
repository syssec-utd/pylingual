def parse_indented_config(config, current_indent=0, previous_indent=0, nested=False):
    """
    This methid basically reads a configuration that conforms to a very poor industry standard
    and returns a nested structure that behaves like a dict. For example:
        {'enable password whatever': {},
         'interface GigabitEthernet1': {
             'description "bleh"': {},
             'fake nested': {
                 'nested nested configuration': {}},
             'switchport mode trunk': {}},
         'interface GigabitEthernet2': {
             'no ip address': {}},
         'interface GigabitEthernet3': {
             'negotiation auto': {},
             'no ip address': {},
             'shutdown': {}},
         'interface Loopback0': {
             'description "blah"': {}}}
    """
    parsed = OrderedDict()
    while True:
        if not config:
            break
        line = config.pop(0)
        if line.lstrip().startswith('!'):
            continue
        last = line.lstrip()
        leading_spaces = len(line) - len(last)
        if leading_spaces > current_indent:
            current = parse_indented_config(config, leading_spaces, current_indent, True)
            _attach_data_to_path(parsed, last, current, nested)
        elif leading_spaces < current_indent:
            config.insert(0, line)
            break
        elif not nested:
            current = parse_indented_config(config, leading_spaces, current_indent, True)
            _attach_data_to_path(parsed, last, current, nested)
        else:
            config.insert(0, line)
            break
    return parsed