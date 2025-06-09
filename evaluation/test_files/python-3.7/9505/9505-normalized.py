def map(requests, stream=True, pool=None, size=1, exception_handler=None):
    """Concurrently converts a list of Requests to Responses.

    :param requests: a collection of Request objects.
    :param stream: If False, the content will not be downloaded immediately.
    :param size: Specifies the number of workers to run at a time. If 1, no parallel processing.
    :param exception_handler: Callback function, called when exception occured. Params: Request, Exception
    """
    pool = pool if pool else Pool(size)
    requests = list(requests)
    requests = pool.map(send, requests)
    ret = []
    for request in requests:
        if request.response is not None:
            ret.append(request.response)
        elif exception_handler and hasattr(request, 'exception'):
            ret.append(exception_handler(request, request.exception))
        else:
            ret.append(None)
    if not pool:
        pool.close()
    return ret