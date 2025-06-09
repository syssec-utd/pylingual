def add_entry():
    """Adds single guestbook record."""
    name, msg = (flask.request.form['name'], flask.request.form['message'])
    flask.g.db.execute('INSERT INTO entry (name, message) VALUES (?, ?)', (name, msg))
    flask.g.db.commit()
    return flask.redirect('/')