def fetch(self, from_date=DEFAULT_DATETIME):
    """Fetch the mbox files from the remote archiver.

        This method stores the archives in the path given during the
        initialization of this object.

        HyperKitty archives are accessed month by month and stored following
        the schema year-month. Archives are fetched from the given month
        till the current month.

        :param from_date: fetch archives that store messages
            equal or after the given date; only year and month values
            are compared

        :returns: a list of tuples, storing the links and paths of the
            fetched archives
        """
    logger.info("Downloading mboxes from '%s' to since %s", self.client.base_url, str(from_date))
    logger.debug("Storing mboxes in '%s'", self.dirpath)
    self.client.fetch(self.client.base_url)
    from_date = datetime_to_utc(from_date)
    to_end = datetime_utcnow()
    to_end += dateutil.relativedelta.relativedelta(months=1)
    months = months_range(from_date, to_end)
    fetched = []
    if not os.path.exists(self.dirpath):
        os.makedirs(self.dirpath)
    tmbox = 0
    for dts in months:
        tmbox += 1
        (start, end) = (dts[0], dts[1])
        filename = start.strftime('%Y-%m.mbox.gz')
        filepath = os.path.join(self.dirpath, filename)
        url = urijoin(self.client.base_url, 'export', filename)
        params = {'start': start.strftime('%Y-%m-%d'), 'end': end.strftime('%Y-%m-%d')}
        success = self._download_archive(url, params, filepath)
        if success:
            fetched.append((url, filepath))
    logger.info('%s/%s MBoxes downloaded', len(fetched), tmbox)
    return fetched