def geckoboard_number_widget(request):
    """
    Returns a number widget for the specified metric's cumulative total.
    """
    params = get_gecko_params(request, days_back=7)
    metric = Metric.objects.get(uid=params['uid'])
    try:
        latest_stat = metric.statistics.filter(frequency=params['frequency']).order_by('-date_time')[0]
    except IndexError:
        return (0, 0)
    try:
        prev_stat = metric.statistics.filter(frequency=params['frequency'], date_time__lte=latest_stat.date_time - timedelta(days=params['days_back'])).order_by('-date_time')[0]
    except IndexError:
        return (latest_stat.cumulative_count, 0) if params['cumulative'] else (latest_stat.count, 0)
    return (latest_stat.cumulative_count, prev_stat.cumulative_count) if params['cumulative'] else (latest_stat.count, prev_stat.count)