def _kwargs_to_qs(**kwargs):
    """Converts kwargs given to GPF to a querystring.

    :returns: the querystring.
    """
    inpOptDef = inputs_options_defaults()
    opts = {name: dct['value'] for name, dct in inpOptDef.items()}
    for k, v in kwargs.items():
        if k.lower() in ('pid', 'playerid'):
            del kwargs[k]
            kwargs['player_id'] = v
        if k == 'player_id':
            if v.startswith('/players/'):
                kwargs[k] = utils.rel_url_to_id(v)
        if isinstance(v, bool):
            kwargs[k] = 'Y' if v else 'N'
        if k.lower() in ('tm', 'team'):
            del kwargs[k]
            kwargs['team_id'] = v
        if k.lower() in ('yr_min', 'yr_max'):
            del kwargs[k]
            if k.lower() == 'yr_min':
                kwargs['year_min'] = int(v)
            else:
                kwargs['year_max'] = int(v)
        if k.lower() in ('wk_min', 'wk_max'):
            del kwargs[k]
            if k.lower() == 'wk_min':
                kwargs['week_num_min'] = int(v)
            else:
                kwargs['week_num_max'] = int(v)
        if k.lower() in ('yr', 'year', 'yrs', 'years'):
            del kwargs[k]
            if isinstance(v, collections.Iterable):
                lst = list(v)
                kwargs['year_min'] = min(lst)
                kwargs['year_max'] = max(lst)
            elif isinstance(v, basestring):
                v = list(map(int, v.split(',')))
                kwargs['year_min'] = min(v)
                kwargs['year_max'] = max(v)
            else:
                kwargs['year_min'] = v
                kwargs['year_max'] = v
        if k.lower() in ('wk', 'week', 'wks', 'weeks'):
            del kwargs[k]
            if isinstance(v, collections.Iterable):
                lst = list(v)
                kwargs['week_num_min'] = min(lst)
                kwargs['week_num_max'] = max(lst)
            elif isinstance(v, basestring):
                v = list(map(int, v.split(',')))
                kwargs['week_num_min'] = min(v)
                kwargs['week_num_max'] = max(v)
            else:
                kwargs['week_num_min'] = v
                kwargs['week_num_max'] = v
        if k == 'playoff_round':
            kwargs['game_type'] = 'P'
        if isinstance(v, basestring):
            v = v.split(',')
        if not isinstance(v, collections.Iterable):
            v = [v]
    for k in kwargs:
        if k in opts:
            opts[k] = []
    for k, v in kwargs.items():
        if k in opts:
            if isinstance(v, basestring):
                v = v.split(',')
            elif not isinstance(v, collections.Iterable):
                v = [v]
            for val in v:
                opts[k].append(val)
    opts['request'] = [1]
    qs = '&'.join(('{}={}'.format(name, val) for name, vals in sorted(opts.items()) for val in vals))
    return qs