def ensure_fresh_rates(func):
    """Decorator for Backend that ensures rates are fresh within last 5 mins"""

    def wrapper(self, *args, **kwargs):
        if self.last_updated + timedelta(minutes=5) < zulu.now():
            self.refresh()
        return func(self, *args, **kwargs)
    return wrapper