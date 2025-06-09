def ignore_case_get(jsonItem, key, defValue=''):
    if not isinstance(jsonItem, dict):
        return defValue
    if not key or not jsonItem:
        return defValue
    if key in jsonItem:
        return jsonItem[key]
    for k in jsonItem.keys():
        if k.upper() == key.upper():
            return jsonItem[k]
    return defValue