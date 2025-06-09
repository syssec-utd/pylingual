def register(device, data, facet):
    """
    Register a U2F device

    data = {
        "version": "U2F_V2",
        "challenge": string, //b64 encoded challenge
        "appId": string, //app_id
    }

    """
    if isinstance(data, string_types):
        data = json.loads(data)
    if data['version'] != VERSION:
        raise ValueError('Unsupported U2F version: %s' % data['version'])
    app_id = data.get('appId', facet)
    verify_facet(app_id, facet)
    app_param = sha256(app_id.encode('utf8')).digest()
    client_data = {'typ': 'navigator.id.finishEnrollment', 'challenge': data['challenge'], 'origin': facet}
    client_data = json.dumps(client_data)
    client_param = sha256(client_data.encode('utf8')).digest()
    request = client_param + app_param
    p1 = 3
    p2 = 0
    response = device.send_apdu(INS_ENROLL, p1, p2, request)
    return {'registrationData': websafe_encode(response), 'clientData': websafe_encode(client_data)}