def missing_categories(context):
    """ Adds the categories that the user does not currently have. """
    user = user_for_context(context)
    categories_available = set(CategoryController.available_categories(user))
    items = ItemController(user).items_pending_or_purchased()
    categories_held = set()
    for product, quantity in items:
        categories_held.add(product.category)
    return categories_available - categories_held