def parse_observation_response(json):
    """Decode AQICN observation response JSON into python object."""
    logging.debug(json)
    iaqi = json['iaqi']
    result = {'idx': json['idx'], 'city': json.get('city', ''), 'aqi': json['aqi'], 'dominentpol': json.get('dominentpol', ''), 'time': json['time']['s'], 'iaqi': [{'p': item, 'v': iaqi[item]['v']} for item in iaqi]}
    return result