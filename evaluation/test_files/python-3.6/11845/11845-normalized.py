def process_ttl(data, template):
    """
    Replace {$ttl} in template with a serialized $TTL record
    """
    record = ''
    if data is not None:
        record += '$TTL %s' % data
    return template.replace('{$ttl}', record)