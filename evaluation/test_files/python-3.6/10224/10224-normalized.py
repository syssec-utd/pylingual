def gravatar(user_or_email, size=GRAVATAR_DEFAULT_SIZE, alt_text='', css_class='gravatar'):
    """ Builds an gravatar <img> tag from an user or email """
    if hasattr(user_or_email, 'email'):
        email = user_or_email.email
    else:
        email = user_or_email
    try:
        url = escape(get_gravatar_url(email=email, size=size))
    except:
        return ''
    return mark_safe('<img class="{css_class}" src="{src}" width="{width}" height="{height}" alt="{alt}" />'.format(css_class=css_class, src=url, width=size, height=size, alt=alt_text))