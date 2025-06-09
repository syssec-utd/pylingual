def _items(self, cart_status, category=None):
    """ Aggregates the items that this user has purchased.

        Arguments:
            cart_status (int or Iterable(int)): etc
            category (Optional[models.inventory.Category]): the category
                of items to restrict to.

        Returns:
            [ProductAndQuantity, ...]: A list of product-quantity pairs,
                aggregating like products from across multiple invoices.

        """
    if not isinstance(cart_status, Iterable):
        cart_status = [cart_status]
    status_query = (Q(productitem__cart__status=status) for status in cart_status)
    in_cart = Q(productitem__cart__user=self.user)
    in_cart = in_cart & reduce(operator.__or__, status_query)
    quantities_in_cart = When(in_cart, then='productitem__quantity')
    quantities_or_zero = Case(quantities_in_cart, default=Value(0))
    products = inventory.Product.objects
    if category:
        products = products.filter(category=category)
    products = products.select_related('category')
    products = products.annotate(quantity=Sum(quantities_or_zero))
    products = products.filter(quantity__gt=0)
    out = []
    for prod in products:
        out.append(ProductAndQuantity(prod, prod.quantity))
    return out