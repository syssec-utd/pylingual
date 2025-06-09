def get_arguments(self):
    """
        Extracts the specific arguments of this CLI
        """
    ApiCli.get_arguments(self)
    if self.args.metric_name is not None:
        self._metric_name = self.args.metric_name
    if self.args.sample is not None:
        self.sample = self.args.sample
    if self.args.source is not None:
        self.source = self.args.source
    else:
        self.source = None
    if self.args.aggregate is not None:
        self.aggregate = self.args.aggregate
    else:
        self.aggregate = 'avg'
    if self.args.format is not None:
        self.format = self.args.format
    else:
        self.format = 'json'
    if self.args.date_format is not None:
        self.date_format = self.args.date_format
    start_time = int(self.parse_time_date(self.args.start).strftime('%s'))
    if self.args.end is None:
        stop_time = int(self.now.strftime('%s'))
    else:
        stop_time = int(self.parse_time_date(self.args.end).strftime('%s'))
    start_time *= 1000
    stop_time *= 1000
    self.path = 'v1/measurements/{0}'.format(self._metric_name)
    url_parameters = {'start': str(start_time), 'end': str(stop_time), 'sample': str(self.sample), 'agg': self.aggregate}
    if self.source is not None:
        url_parameters['source'] = self.source
    self.url_parameters = url_parameters