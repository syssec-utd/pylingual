def _build_request_data(request):
    """
    Returns a dictionary containing data from the request.
    Can handle webob or werkzeug-based request objects.
    """
    if WebobBaseRequest and isinstance(request, WebobBaseRequest):
        return _build_webob_request_data(request)
    if DjangoHttpRequest and isinstance(request, DjangoHttpRequest):
        return _build_django_request_data(request)
    if RestFrameworkRequest and isinstance(request, RestFrameworkRequest):
        return _build_django_request_data(request)
    if WerkzeugRequest and isinstance(request, WerkzeugRequest):
        return _build_werkzeug_request_data(request)
    if TornadoRequest and isinstance(request, TornadoRequest):
        return _build_tornado_request_data(request)
    if BottleRequest and isinstance(request, BottleRequest):
        return _build_bottle_request_data(request)
    if SanicRequest and isinstance(request, SanicRequest):
        return _build_sanic_request_data(request)
    if FalconRequest and isinstance(request, FalconRequest):
        return _build_falcon_request_data(request)
    if isinstance(request, dict) and 'wsgi.version' in request:
        return _build_wsgi_request_data(request)
    return None