def encode(something):
    """Encode something with SECRET_KEY."""
    secret_key = current_app.config.get('SECRET_KEY')
    s = URLSafeSerializer(secret_key)
    return s.dumps(something)