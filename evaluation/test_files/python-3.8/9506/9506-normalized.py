def imap(requests, stream=True, pool=None, size=2, exception_handler=None):
    """Concurrently converts a generator object of Requests to
    a generator of Responses.

    :param requests: a generator of Request objects.
    :param stream: If False, the content will not be downloaded immediately.
    :param size: Specifies the number of requests to make at a time. default is 2
    :param exception_handler: Callback function, called when exception occured. Params: Request, Exception
    """

    def send(r):
        return r.send(stream=stream)
    pool = pool if pool else Pool(size)
    for request in pool.imap(send, requests):
        if request.response is not None:
            yield request.response
        elif exception_handler:
            exception_handler(request, request.exception)
    if not pool:
        pool.close()