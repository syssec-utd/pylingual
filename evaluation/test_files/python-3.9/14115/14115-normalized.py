def upload_from_url_sync(cls, url, timeout=30, interval=0.3, until_ready=False, store=None, filename=None):
    """Uploads file from given url and returns ``File`` instance.

        Args:
            - url (str): URL of file to upload to
            - store (Optional[bool]): Should the file be automatically stored
                upon upload. Defaults to None.
                - False - do not store file
                - True - store file (can result in error if autostore
                               is disabled for project)
                - None - use project settings
            - filename (Optional[str]): Name of the uploaded file. If this not
                specified the filename will be obtained from response headers
                or source URL. Defaults to None.
            - timeout (Optional[int]): seconds to wait for successful upload.
                Defaults to 30.
            - interval (Optional[float]): interval between upload status checks.
                Defaults to 0.3.
            - until_ready (Optional[bool]): should we wait until file is
                available via CDN. Defaults to False.

        Returns:
            ``File`` instance

        Raises:
            ``TimeoutError`` if file wasn't uploaded in time

        """
    ffu = cls.upload_from_url(url, store, filename)
    return ffu.wait(timeout=timeout, interval=interval, until_ready=until_ready)