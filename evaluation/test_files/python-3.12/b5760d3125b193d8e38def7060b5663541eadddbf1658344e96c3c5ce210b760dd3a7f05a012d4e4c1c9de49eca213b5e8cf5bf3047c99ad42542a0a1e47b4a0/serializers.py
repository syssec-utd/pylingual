from rest_framework.serializers import Field
from wagtail.models import Page

class BreadcrumpSerializer(Field):

    def get_parent_or_none(self, page) -> Page or None:
        parent = page.get_parent()
        if parent is None:
            return None
        if parent.url is None:
            return None
        if parent.url == '/':
            return None
        return parent

    def to_representation(self, page: Page):
        parent = page
        while parent is not None:
            yield {'id': parent.id, 'url': parent.url, 'slug': parent.slug, 'title': parent.title}
            parent = self.get_parent_or_none(parent)