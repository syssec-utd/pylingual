def verify_token():
    """Verify token and save in session if it's valid."""
    try:
        from .models import SecretLink
        token = request.args['token']
        if token and SecretLink.validate_token(token, {}):
            session['accessrequests-secret-token'] = token
    except KeyError:
        pass