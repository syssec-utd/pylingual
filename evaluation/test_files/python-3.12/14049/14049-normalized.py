def _set_affiliation(self, v, load=False):
    """
    Setter method for affiliation, mapped from YANG variable /universe/individual/affiliation (identityref)
    If this variable is read-only (config: false) in the
    source YANG file, then _set_affiliation is considered as a private
    method. Backends looking to populate this variable should
    do so via calling thisObj._set_affiliation() directly.
    """
    if hasattr(v, '_utype'):
        v = v._utype(v)
    try:
        t = YANGDynClass(v, base=RestrictedClassType(base_type=unicode, restriction_type='dict_key', restriction_arg={u'napalm-star-wars:EMPIRE': {'@namespace': u'https://napalm-yang.readthedocs.io/napalm-star-wars', '@module': u'napalm-star-wars'}, u'EMPIRE': {'@namespace': u'https://napalm-yang.readthedocs.io/napalm-star-wars', '@module': u'napalm-star-wars'}, u'napalm-star-wars:REBEL_ALLIANCE': {'@namespace': u'https://napalm-yang.readthedocs.io/napalm-star-wars', '@module': u'napalm-star-wars'}, u'REBEL_ALLIANCE': {'@namespace': u'https://napalm-yang.readthedocs.io/napalm-star-wars', '@module': u'napalm-star-wars'}}), is_leaf=True, yang_name='affiliation', parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='https://napalm-yang.readthedocs.io/napalm-star-wars', defining_module='napalm-star-wars', yang_type='identityref', is_config=True)
    except (TypeError, ValueError):
        raise ValueError({'error-string': 'affiliation must be of a type compatible with identityref', 'defined-type': 'napalm-star-wars:identityref', 'generated-type': 'YANGDynClass(base=RestrictedClassType(base_type=unicode, restriction_type="dict_key", restriction_arg={u\'napalm-star-wars:EMPIRE\': {\'@namespace\': u\'https://napalm-yang.readthedocs.io/napalm-star-wars\', \'@module\': u\'napalm-star-wars\'}, u\'EMPIRE\': {\'@namespace\': u\'https://napalm-yang.readthedocs.io/napalm-star-wars\', \'@module\': u\'napalm-star-wars\'}, u\'napalm-star-wars:REBEL_ALLIANCE\': {\'@namespace\': u\'https://napalm-yang.readthedocs.io/napalm-star-wars\', \'@module\': u\'napalm-star-wars\'}, u\'REBEL_ALLIANCE\': {\'@namespace\': u\'https://napalm-yang.readthedocs.io/napalm-star-wars\', \'@module\': u\'napalm-star-wars\'}},), is_leaf=True, yang_name="affiliation", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace=\'https://napalm-yang.readthedocs.io/napalm-star-wars\', defining_module=\'napalm-star-wars\', yang_type=\'identityref\', is_config=True)'})
    self.__affiliation = t
    if hasattr(self, '_set'):
        self._set()