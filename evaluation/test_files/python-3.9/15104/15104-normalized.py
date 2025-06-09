def _invoice_matches_cart(self):
    """ Returns true if there is no cart, or if the revision of this
        invoice matches the current revision of the cart. """
    self._refresh()
    cart = self.invoice.cart
    if not cart:
        return True
    return cart.revision == self.invoice.cart_revision