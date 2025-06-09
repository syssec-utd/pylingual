def from_url(url):
    """
        Given a URL, return a package
        :param url:
        :return:
        """
    package_data = HTTPClient().http_request(url=url, decode=None)
    return Package(raw_data=package_data)