def render_prev_next_links(self, scheme=None):
    """Render the rel=prev and rel=next links to a Markup object for injection into a template"""
    output = ''
    if self.has_prev:
        output += '<link rel="prev" href="{}" />\n'.format(self.get_full_page_url(self.prev, scheme=scheme))
    if self.has_next:
        output += '<link rel="next" href="{}" />\n'.format(self.get_full_page_url(self.next, scheme=scheme))
    return Markup(output)