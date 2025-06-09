def get_arguments(self):
    """
        Extracts the specific arguments of this CLI
        """
    ApiCli.get_arguments(self)
    if self.args.metricName is not None:
        self.metricName = self.args.metricName
    if self.args.measurement is not None:
        self.measurement = self.args.measurement
    if self.args.source is not None:
        self.source = self.args.source
    else:
        self.source = socket.gethostname()
    if self.args.timestamp is not None:
        self.timestamp = int(self.args.timestamp)
    m = {'metric': self.metricName, 'measure': self.measurement}
    if self.source is not None:
        m['source'] = self.source
    if self.timestamp is not None:
        m['timestamp'] = int(self.timestamp)
    self._process_properties()
    if self._properties is not None:
        m['metadata'] = self._properties
    self.data = json.dumps(m, sort_keys=True)
    self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}