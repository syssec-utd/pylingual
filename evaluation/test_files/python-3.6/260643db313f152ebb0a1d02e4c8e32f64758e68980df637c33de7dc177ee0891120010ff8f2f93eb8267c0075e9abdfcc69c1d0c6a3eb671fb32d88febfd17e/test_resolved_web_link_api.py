from rest_framework import status
from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase
from ..events import event_web_link_navigated
from ..models import ResolvedWebLink
from ..permissions import permission_web_link_instance_view
from .mixins import ResolvedWebLinkAPIViewTestMixin, WebLinkTestMixin

class ResolvedWebLinkAPIViewTestCase(DocumentTestMixin, WebLinkTestMixin, ResolvedWebLinkAPIViewTestMixin, BaseAPITestCase):

    def setUp(self):
        super().setUp()
        self._create_test_web_link(add_test_document_type=True)

    def test_resolved_web_link_detail_api_view_no_permission(self):
        self._clear_events()
        response = self._request_resolved_web_link_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_resolved_web_link_detail_api_view_with_document_access(self):
        self.grant_access(obj=self._test_document, permission=permission_web_link_instance_view)
        self._clear_events()
        response = self._request_resolved_web_link_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_resolved_web_link_detail_api_view_with_web_link_access(self):
        self.grant_access(obj=self._test_web_link, permission=permission_web_link_instance_view)
        self._clear_events()
        response = self._request_resolved_web_link_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_resolved_web_link_detail_api_view_with_full_access(self):
        self.grant_access(obj=self._test_web_link, permission=permission_web_link_instance_view)
        self.grant_access(obj=self._test_document, permission=permission_web_link_instance_view)
        self._clear_events()
        response = self._request_resolved_web_link_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self._test_web_link.pk)
        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_resolved_web_link_detail_api_view_with_full_access(self):
        self.grant_access(obj=self._test_web_link, permission=permission_web_link_instance_view)
        self.grant_access(obj=self._test_document, permission=permission_web_link_instance_view)
        self._test_document.delete()
        self._clear_events()
        response = self._request_resolved_web_link_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_resolved_web_link_list_api_view_no_permission(self):
        self._clear_events()
        response = self._request_resolved_web_link_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_resolved_web_link_list_api_view_with_document_access(self):
        self.grant_access(obj=self._test_document, permission=permission_web_link_instance_view)
        self._clear_events()
        response = self._request_resolved_web_link_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_resolved_web_link_list_api_view_with_web_link_access(self):
        self.grant_access(obj=self._test_web_link, permission=permission_web_link_instance_view)
        self._clear_events()
        response = self._request_resolved_web_link_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_resolved_web_link_list_api_view_with_full_access(self):
        self.grant_access(obj=self._test_web_link, permission=permission_web_link_instance_view)
        self.grant_access(obj=self._test_document, permission=permission_web_link_instance_view)
        self._clear_events()
        response = self._request_resolved_web_link_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['id'], self._test_web_link.pk)
        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_resolved_web_link_list_api_view_with_full_access(self):
        self.grant_access(obj=self._test_web_link, permission=permission_web_link_instance_view)
        self.grant_access(obj=self._test_document, permission=permission_web_link_instance_view)
        self._test_document.delete()
        self._clear_events()
        response = self._request_resolved_web_link_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_resolved_web_link_navigate_api_view_no_permission(self):
        self._clear_events()
        response = self._request_resolved_web_link_navigate_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_resolved_web_link_navigate_api_view_with_web_link_access(self):
        self.grant_access(obj=self._test_web_link, permission=permission_web_link_instance_view)
        self._clear_events()
        response = self._request_resolved_web_link_navigate_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_resolved_web_link_navigate_api_view_with_document_access(self):
        self.grant_access(obj=self._test_document, permission=permission_web_link_instance_view)
        self._clear_events()
        response = self._request_resolved_web_link_navigate_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_resolved_web_link_navigate_api_view_with_full_access(self):
        self.grant_access(obj=self._test_document, permission=permission_web_link_instance_view)
        self.grant_access(obj=self._test_web_link, permission=permission_web_link_instance_view)
        self._clear_events()
        response = self._request_resolved_web_link_navigate_api_view()
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, ResolvedWebLink.objects.get(pk=self._test_web_link.pk).get_redirect_url_for(document=self._test_document))
        events = self._get_test_events()
        self.assertEqual(events.count(), 1)
        self.assertEqual(events[0].action_object, self._test_document)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_web_link)
        self.assertEqual(events[0].verb, event_web_link_navigated.id)

    def test_trashed_document_resolved_web_link_navigate_api_view_with_full_access(self):
        self.grant_access(obj=self._test_document, permission=permission_web_link_instance_view)
        self.grant_access(obj=self._test_web_link, permission=permission_web_link_instance_view)
        self._test_document.delete()
        self._clear_events()
        response = self._request_resolved_web_link_navigate_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        events = self._get_test_events()
        self.assertEqual(events.count(), 0)