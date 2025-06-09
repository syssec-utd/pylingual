def template(self, string):
    """
        Interpret a template string.  This returns a callable taking one
        argument--this context--and returning a string rendered from
        the template.

        :param string: The template string.

        :returns: A callable of one argument that will return the
                  desired string.
        """
    if not isinstance(string, six.string_types):
        return lambda ctxt: string
    tmpl = self._jinja.from_string(string)
    return lambda ctxt: tmpl.render(ctxt.variables)