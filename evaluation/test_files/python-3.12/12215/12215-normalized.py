def render_standalone_response(self, request, fragment, **kwargs):
    """
        Renders a standalone page as a response for the specified fragment.
        """
    if fragment is None:
        return HttpResponse(status=204)
    html = self.render_to_standalone_html(request, fragment, **kwargs)
    return HttpResponse(html)