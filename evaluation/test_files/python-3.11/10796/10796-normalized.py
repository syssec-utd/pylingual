def push_url(interface):
    """
    Decorates a function returning the url of translation API.
    Creates and maintains HTTP connection state

    Returns a dict response object from the server containing the translated
    text and metadata of the request body

    :param interface: Callable Request Interface
    :type interface: Function
    """

    @functools.wraps(interface)
    def connection(*args, **kwargs):
        """
        Extends and wraps a HTTP interface.

        :return: Response Content
        :rtype: Dictionary
        """
        session = Session()
        session.mount('http://', HTTPAdapter(max_retries=2))
        session.mount('https://', HTTPAdapter(max_retries=2))
        request = Request(**interface(*args, **kwargs))
        prepare = session.prepare_request(request)
        response = session.send(prepare, verify=True)
        if response.status_code != requests.codes.ok:
            response.raise_for_status()
        cleanup = re.subn(',(?=,)', '', response.content.decode('utf-8'))[0]
        return json.loads(cleanup.replace('\\xA0', ' ').replace('[,', '[1,'), encoding='UTF-8')
    return connection