def create_user(username):
    """Create a new user."""
    password = prompt_pass('Enter password')
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()