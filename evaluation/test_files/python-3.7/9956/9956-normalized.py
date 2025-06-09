def validate(self, *args, **kwargs):
    """
        Validates the form by calling `validate` on each field, passing any
        extra `Form.validate_<fieldname>` validators to the field validator.

        also calls `validate_ldap`
        """
    valid = FlaskForm.validate(self, *args, **kwargs)
    if not valid:
        logging.debug("Form validation failed before we had a chance to check ldap. Reasons: '{0}'".format(self.errors))
        return valid
    return self.validate_ldap()