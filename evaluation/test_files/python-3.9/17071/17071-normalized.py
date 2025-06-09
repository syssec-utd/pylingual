def do_login(self, user):
    """Login a user."""
    this.user_id = user.pk
    this.user_ddp_id = get_meteor_id(user)
    this.user_sub_id = meteor_random_id()
    API.do_sub(this.user_sub_id, 'LoggedInUser', silent=True)
    self.update_subs(user.pk)
    user_logged_in.send(sender=user.__class__, request=this.request, user=user)