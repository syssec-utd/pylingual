def _list_resource_record_sets_by_zone_id(self, id, rrset_type=None, identifier=None, name=None, page_chunks=100):
    """
        Lists a hosted zone's resource record sets by Zone ID, if you
        already know it.

        .. tip:: For most cases, we recommend going through a
            :py:class:`HostedZone <route53.hosted_zone.HostedZone>`
            instance's
            :py:meth:`HostedZone.record_sets <route53.hosted_zone.HostedZone.record_sets>`
            property, but this saves an HTTP request if you already know the
            zone's ID.

        :param str id: The ID of the zone whose record sets we're listing.
        :keyword str rrset_type: The type of resource record set to begin the
            record listing from.
        :keyword str identifier: Weighted and latency resource record sets
            only: If results were truncated for a given DNS name and type,
            the value of SetIdentifier for the next resource record set
            that has the current DNS name and type.
        :keyword str name: Not really sure what this does.
        :keyword int page_chunks: This API call is paginated behind-the-scenes
            by this many ResourceRecordSet instances. The default should be
            fine for just about everybody, aside from those with tons of RRS.

        :rtype: generator
        :returns: A generator of ResourceRecordSet instances.
        """
    params = {'name': name, 'type': rrset_type, 'identifier': identifier, 'maxitems': page_chunks}
    return self._do_autopaginating_api_call(path='hostedzone/%s/rrset' % id, params=params, method='GET', parser_func=xml_parsers.list_resource_record_sets_by_zone_id_parser, parser_kwargs={'zone_id': id}, next_marker_xpath='./{*}NextRecordName', next_marker_param_name='name', next_type_xpath='./{*}NextRecordType')