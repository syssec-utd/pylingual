def first_name(languages=None, genders=None):
    """
        return a random first name
    :return:

    >>> from mock import patch
    >>> with patch('%s._get_firstnamess' % __name__, lambda *args: ['aaa']):
    ...     first_name()
    'Aaa'
    """
    choices = []
    languages = languages or ['en']
    genders = genders or [GENDER_MALE, GENDER_FEMALE]
    for lang in languages:
        for gender in genders:
            samples = _get_firstnames(lang, gender)
            choices.extend(samples)
    return random.choice(choices).title()