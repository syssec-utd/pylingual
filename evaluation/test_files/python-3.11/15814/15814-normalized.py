def _for_element__get(self):
    """
        Get/set the element this label points to.  Return None if it
        can't be found.
        """
    id = self.get('for')
    if not id:
        return None
    return self.body.get_element_by_id(id)