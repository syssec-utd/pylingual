def _modifies_cart(func):
    """ Decorator that makes the wrapped function raise ValidationError
    if we're doing something that could modify the cart.

    It also wraps the execution of this function in a database transaction,
    and marks the boundaries of a cart operations batch.
    """

    @functools.wraps(func)
    def inner(self, *a, **k):
        self._fail_if_cart_is_not_active()
        with transaction.atomic():
            with BatchController.batch(self.cart.user):
                memoised = self.for_user(self.cart.user)
                memoised._modified_by_batch = True
                return func(self, *a, **k)
    return inner