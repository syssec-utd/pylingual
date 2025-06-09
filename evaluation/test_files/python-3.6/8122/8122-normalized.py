def get_queryset(self):
    """Optionally restricts the returned articles by filtering against a `topic`
        query parameter in the URL."""
    queryset = self.get_publishable_queryset()
    queryset = queryset.select_related('featured_image', 'featured_video', 'topic', 'section', 'subsection').prefetch_related('tags', 'featured_image__image__authors', 'authors')
    queryset = queryset.order_by('-updated_at')
    q = self.request.query_params.get('q', None)
    section = self.request.query_params.get('section', None)
    tags = self.request.query_params.getlist('tags', None)
    author = self.request.query_params.get('author', None)
    if q is not None:
        queryset = queryset.filter(headline__icontains=q)
    if section is not None:
        queryset = queryset.filter(section_id=section)
    if tags is not None:
        for tag in tags:
            queryset = queryset.filter(tags__id=tag)
    if author is not None:
        queryset = queryset.filter(authors__person_id=author)
    return queryset