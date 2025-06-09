def create_job_collection_to_xml(plan):
    """
        <Resource xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://schemas.microsoft.com/windowsazure">
        <IntrinsicSettings>
            <Plan>Standard</Plan>
            <Quota>
                <MaxJobCount>10</MaxJobCount>
                <MaxRecurrence>
                    <Frequency>Second</Frequency>
                    <Interval>1</Interval>
                </MaxRecurrence>
            </Quota>
        </IntrinsicSettings>
        </Resource>
        """
    if plan not in ['Free', 'Standard']:
        raise ValueError("Plan: Invalid option must be 'Standard' or 'Free'")
    body = '<Resource xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://schemas.microsoft.com/windowsazure"><IntrinsicSettings>'
    body += ''.join(['<plan>', plan, '</plan>'])
    body += '</IntrinsicSettings></Resource>'
    return body