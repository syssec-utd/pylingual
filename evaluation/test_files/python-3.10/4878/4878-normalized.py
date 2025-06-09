def fetch(self, from_date=DEFAULT_DATETIME):
    """Fetch the mbox files from the remote archiver.

        Stores the archives in the path given during the initialization
        of this object. Those archives which a not valid extension will
        be ignored.

        Pipermail archives usually have on their file names the date of
        the archives stored following the schema year-month. When `from_date`
        property is called, it will return the mboxes which their year
        and month are equal or after that date.

        :param from_date: fetch archives that store messages
            equal or after the given date; only year and month values
            are compared

        :returns: a list of tuples, storing the links and paths of the
            fetched archives
        """
    logger.info("Downloading mboxes from '%s' to since %s", self.url, str(from_date))
    logger.debug("Storing mboxes in '%s'", self.dirpath)
    from_date = datetime_to_utc(from_date)
    r = requests.get(self.url, verify=self.verify)
    r.raise_for_status()
    links = self._parse_archive_links(r.text)
    fetched = []
    if not os.path.exists(self.dirpath):
        os.makedirs(self.dirpath)
    for l in links:
        filename = os.path.basename(l)
        mbox_dt = self._parse_date_from_filepath(filename)
        if from_date.year == mbox_dt.year and from_date.month == mbox_dt.month or from_date < mbox_dt:
            filepath = os.path.join(self.dirpath, filename)
            success = self._download_archive(l, filepath)
            if success:
                fetched.append((l, filepath))
    logger.info('%s/%s MBoxes downloaded', len(fetched), len(links))
    return fetched