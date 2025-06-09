def fill(self, doc_contents):
    """ Fill the content of the document with the information in doc_contents.
        This is different from the TextDocument fill function, because this will
        check for symbools in the values of `doc_content` and replace them
        to good XML codes before filling the template.

        Parameters
        ----------
        doc_contents: dict
            Set of values to set the template document.

        Returns
        -------
        filled_doc: str
            The content of the document with the template information filled.
        """
    for (key, content) in doc_contents.items():
        doc_contents[key] = replace_chars_for_svg_code(content)
    return super(SVGDocument, self).fill(doc_contents=doc_contents)