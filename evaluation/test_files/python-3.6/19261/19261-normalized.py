def _getdata(self, url, data=''):
    """
        Wrapper method
        """
    request = Request(url)
    if data != '':
        request = Request(url, urlencode(data))
    try:
        response = urlopen(request)
    except HTTPError as e:
        print("The Server couldn't fulfill the request.")
        print('Error code: ', e.code)
    except URLError as e:
        print('We failed to reach a server.')
        print('Reason: ', e.code)
    else:
        return response.read()