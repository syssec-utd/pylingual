def get_station_observation(station_code, token):
    """Request station data for a specific station identified by code.

    A language parameter can also be specified to translate location
    information (default: "en")
    """
    req = requests.get(API_ENDPOINT_OBS % station_code, params={'token': token})
    if req.status_code == 200 and req.json()['status'] == 'ok':
        return parse_observation_response(req.json()['data'])
    else:
        return {}