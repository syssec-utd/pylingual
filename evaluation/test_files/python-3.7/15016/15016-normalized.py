def iter_osm_stream(start_sqn=None, base_url='https://planet.openstreetmap.org/replication/minute', expected_interval=60, parse_timestamps=True, state_dir=None):
    """Start processing an OSM diff stream and yield one changeset at a time to
    the caller."""
    if state_dir:
        if not os.path.exists(state_dir):
            raise Exception('Specified state_dir "%s" doesn\'t exist.' % state_dir)
        if os.path.exists('%s/state.txt' % state_dir):
            with open('%s/state.txt' % state_dir) as f:
                state = readState(f)
                start_sqn = state['sequenceNumber']
    if not start_sqn:
        u = urllib2.urlopen('%s/state.txt' % base_url)
        state = readState(u)
    else:
        sqnStr = str(start_sqn).zfill(9)
        u = urllib2.urlopen('%s/%s/%s/%s.state.txt' % (base_url, sqnStr[0:3], sqnStr[3:6], sqnStr[6:9]))
        state = readState(u)
    interval_fudge = 0.0
    while True:
        sqnStr = state['sequenceNumber'].zfill(9)
        url = '%s/%s/%s/%s.osc.gz' % (base_url, sqnStr[0:3], sqnStr[3:6], sqnStr[6:9])
        content = urllib2.urlopen(url)
        content = StringIO.StringIO(content.read())
        gzipper = gzip.GzipFile(fileobj=content)
        for a in iter_osm_change_file(gzipper, parse_timestamps):
            yield a
        stateTs = datetime.datetime.strptime(state['timestamp'], '%Y-%m-%dT%H:%M:%SZ')
        yield (None, model.Finished(state['sequenceNumber'], stateTs))
        nextTs = stateTs + datetime.timedelta(seconds=expected_interval + interval_fudge)
        if datetime.datetime.utcnow() < nextTs:
            timeToSleep = (nextTs - datetime.datetime.utcnow()).total_seconds()
        else:
            timeToSleep = 0.0
        time.sleep(timeToSleep)
        sqnStr = str(int(state['sequenceNumber']) + 1).zfill(9)
        url = '%s/%s/%s/%s.state.txt' % (base_url, sqnStr[0:3], sqnStr[3:6], sqnStr[6:9])
        delay = 1.0
        while True:
            try:
                u = urllib2.urlopen(url)
                interval_fudge -= interval_fudge / 2.0
                break
            except urllib2.HTTPError as e:
                if e.code == 404:
                    time.sleep(delay)
                    delay = min(delay * 2, 13)
                    interval_fudge += delay
        if state_dir:
            with open('%s/state.txt' % state_dir, 'w') as f:
                f.write(u.read())
            with open('%s/state.txt' % state_dir, 'r') as f:
                state = readState(f)
        else:
            state = readState(u)