def get_gecko_params(request, uid=None, days_back=0, cumulative=True, frequency=settings.STATISTIC_FREQUENCY_DAILY, min_val=0, max_val=100, chart_type='standard', percentage='show', sort=False):
    """
    Returns the default GET parameters for a particular Geckoboard
    view request.
    """
    return {'days_back': int(request.GET.get('daysback', days_back)), 'uid': request.GET.get('uid', uid), 'uids': get_GET_array(request, 'uids[]'), 'cumulative': get_GET_bool(request, 'cumulative', cumulative), 'frequency': request.GET.get('frequency', frequency), 'min': request.GET.get('min', min_val), 'max': request.GET.get('max', max_val), 'type': request.GET.get('type', chart_type), 'percentage': request.GET.get('percentage', percentage), 'sort': get_GET_bool(request, 'sort', sort)}