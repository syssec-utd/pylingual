def parse_hosted_zone(e_zone, connection):
    """
    This a common parser that allows the passing of any valid HostedZone
    tag. It will spit out the appropriate HostedZone object for the tag.

    :param lxml.etree._Element e_zone: The root node of the etree parsed
        response from the API.
    :param Route53Connection connection: The connection instance used to
        query the API.
    :rtype: HostedZone
    :returns: An instantiated HostedZone object.
    """
    kwargs = {}
    for e_field in e_zone:
        tag_name = e_field.tag.split('}')[1]
        field_text = e_field.text
        if tag_name == 'Config':
            e_comment = e_field.find('./{*}Comment')
            kwargs['comment'] = e_comment.text if e_comment is not None else None
            continue
        elif tag_name == 'Id':
            field_text = field_text.strip('/hostedzone/')
        kw_name = HOSTED_ZONE_TAG_TO_KWARG_MAP[tag_name]
        kwargs[kw_name] = field_text
    return HostedZone(connection, **kwargs)