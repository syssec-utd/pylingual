def save_aggregate_report_to_elasticsearch(aggregate_report, index_suffix=None, monthly_indexes=False):
    """
    Saves a parsed DMARC aggregate report to ElasticSearch

    Args:
        aggregate_report (OrderedDict): A parsed forensic report
        index_suffix (str): The suffix of the name of the index to save to
        monthly_indexes (bool): Use monthly indexes instead of daily indexes

    Raises:
            AlreadySaved
    """
    logger.debug('Saving aggregate report to Elasticsearch')
    aggregate_report = aggregate_report.copy()
    metadata = aggregate_report['report_metadata']
    org_name = metadata['org_name']
    report_id = metadata['report_id']
    domain = aggregate_report['policy_published']['domain']
    begin_date = human_timestamp_to_datetime(metadata['begin_date'])
    end_date = human_timestamp_to_datetime(metadata['end_date'])
    begin_date_human = begin_date.strftime('%Y-%m-%d %H:%M:%S')
    end_date_human = end_date.strftime('%Y-%m-%d %H:%M:%S')
    if monthly_indexes:
        index_date = begin_date.strftime('%Y-%m')
    else:
        index_date = begin_date.strftime('%Y-%m-%d')
    aggregate_report['begin_date'] = begin_date
    aggregate_report['end_date'] = end_date
    date_range = [aggregate_report['begin_date'], aggregate_report['end_date']]
    org_name_query = Q(dict(match=dict(org_name=org_name)))
    report_id_query = Q(dict(match=dict(report_id=report_id)))
    domain_query = Q(dict(match={'published_policy.domain': domain}))
    begin_date_query = Q(dict(match=dict(date_range=begin_date)))
    end_date_query = Q(dict(match=dict(date_range=end_date)))
    search = Search(index='dmarc_aggregate*')
    query = org_name_query & report_id_query & domain_query
    query = query & begin_date_query & end_date_query
    search.query = query
    existing = search.execute()
    if len(existing) > 0:
        raise AlreadySaved('An aggregate report ID {0} from {1} about {2} with a date range of {3} UTC to {4} UTC already exists in Elasticsearch'.format(report_id, org_name, domain, begin_date_human, end_date_human))
    published_policy = _PublishedPolicy(domain=aggregate_report['policy_published']['domain'], adkim=aggregate_report['policy_published']['adkim'], aspf=aggregate_report['policy_published']['aspf'], p=aggregate_report['policy_published']['p'], sp=aggregate_report['policy_published']['sp'], pct=aggregate_report['policy_published']['pct'], fo=aggregate_report['policy_published']['fo'])
    for record in aggregate_report['records']:
        agg_doc = _AggregateReportDoc(xml_schemea=aggregate_report['xml_schema'], org_name=metadata['org_name'], org_email=metadata['org_email'], org_extra_contact_info=metadata['org_extra_contact_info'], report_id=metadata['report_id'], date_range=date_range, errors=metadata['errors'], published_policy=published_policy, source_ip_address=record['source']['ip_address'], source_country=record['source']['country'], source_reverse_dns=record['source']['reverse_dns'], source_base_domain=record['source']['base_domain'], message_count=record['count'], disposition=record['policy_evaluated']['disposition'], dkim_aligned=record['policy_evaluated']['dkim'] == 'pass', spf_aligned=record['policy_evaluated']['spf'] == 'pass', header_from=record['identifiers']['header_from'], envelope_from=record['identifiers']['envelope_from'], envelope_to=record['identifiers']['envelope_to'])
        for override in record['policy_evaluated']['policy_override_reasons']:
            agg_doc.add_policy_override(type_=override['type'], comment=override['comment'])
        for dkim_result in record['auth_results']['dkim']:
            agg_doc.add_dkim_result(domain=dkim_result['domain'], selector=dkim_result['selector'], result=dkim_result['result'])
        for spf_result in record['auth_results']['spf']:
            agg_doc.add_spf_result(domain=spf_result['domain'], scope=spf_result['scope'], result=spf_result['result'])
        index = 'dmarc_aggregate'
        if index_suffix:
            index = '{0}_{1}'.format(index, index_suffix)
        index = '{0}-{1}'.format(index, index_date)
        create_indexes([index])
        agg_doc.meta.index = index
        try:
            agg_doc.save()
        except Exception as e:
            raise ElasticsearchError('Elasticsearch error: {0}'.format(e.__str__()))