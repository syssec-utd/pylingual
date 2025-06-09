def _prepare_locale_dirs(languages, locale_root):
    """
    Prepare locale dirs for writing po files.
    Create new directories if they doesn't exist.
    """
    trans_languages = []
    for (i, t) in enumerate(languages):
        lang = t.split(':')[0]
        trans_languages.append(lang)
        lang_path = os.path.join(locale_root, lang)
        if not os.path.exists(lang_path):
            os.makedirs(lang_path)
    return trans_languages