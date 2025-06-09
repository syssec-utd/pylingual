def is_matching_mime_type(self, mime_type):
    """This implements the MIME-type matching logic for deciding whether
        to run `make_clean_html`

        """
    if len(self.include_mime_types) == 0:
        return True
    if mime_type is None:
        return False
    mime_type = mime_type.lower()
    return any((mime_type.startswith(mt) for mt in self.include_mime_types))