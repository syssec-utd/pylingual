def get_slider_items(context, amount=None):
    """Returns the published slider items."""
    req = context.get('request')
    qs = SliderItem.objects.published(req).order_by('position')
    if amount:
        qs = qs[:amount]
    return qs