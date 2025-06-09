def create_user(self, params):
    """Register a new user account."""
    receivers = create_user.send(sender=__name__, request=this.request, params=params)
    if len(receivers) == 0:
        raise NotImplementedError('Handler for `create_user` not registered.')
    user = receivers[0][1]
    user = auth.authenticate(username=user.get_username(), password=params['password'])
    self.do_login(user)
    return get_user_token(user=user, purpose=HashPurpose.RESUME_LOGIN, minutes_valid=HASH_MINUTES_VALID[HashPurpose.RESUME_LOGIN])