def start_instances(instances, region):
    """Start all the instances given by its ids"""
    if not instances:
        return
    conn = ec2_connect(region)
    log('Starting instances {0}.'.format(instances))
    conn.start_instances(instances)
    log('Done')