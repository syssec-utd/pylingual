def render(self, data):
    """ Renders the reports based on data.content_type's value.

        Arguments:
            data (ReportViewRequestData): The report data. data.content_type
                is used to determine how the reports are rendered.

        Returns:
            HTTPResponse: The rendered version of the report.

        """
    renderers = {'text/csv': self._render_as_csv, 'text/html': self._render_as_html, None: self._render_as_html}
    render = renderers[data.content_type]
    return render(data)