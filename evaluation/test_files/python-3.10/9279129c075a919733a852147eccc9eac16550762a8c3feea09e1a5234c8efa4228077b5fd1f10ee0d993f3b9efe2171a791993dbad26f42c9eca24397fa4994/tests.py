import json
from abc import ABC, abstractmethod
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils.http import urlencode
from temba.api.models import APIToken
from temba.tests import TembaTest
from temba.orgs.models import Org

class TembaRequestMixin(ABC):

    def reverse(self, viewname, kwargs=None, query_params=None):
        url = reverse(viewname, kwargs=kwargs)
        if query_params:
            return '%s?%s' % (url, urlencode(query_params))
        else:
            return url

    def request_get(self, **query_params):
        url = self.reverse(self.get_url_namespace(), query_params=query_params)
        token = APIToken.get_or_create(self.org, self.admin, Group.objects.get(name='Administrators'))
        return self.client.get(f'{url}', HTTP_AUTHORIZATION=f'Token {token.key}')

    def request_detail(self, **kwargs):
        url = self.reverse(self.get_url_namespace(), query_params=kwargs)
        token = APIToken.get_or_create(self.org, self.admin, Group.objects.get(name='Administrators'))
        return self.client.get(f'{url}', HTTP_AUTHORIZATION=f'Token {token.key}')

    def request_patch(self, data, **kwargs):
        url = self.reverse(self.get_url_namespace(), query_params=kwargs)
        token = APIToken.get_or_create(self.org, self.admin, Group.objects.get(name='Administrators'))
        return self.client.patch(f'{url}', HTTP_AUTHORIZATION=f'Token {token.key}', data=json.dumps(data), content_type='application/json')

    def request_post(self, data):
        url = reverse(self.get_url_namespace())
        token = APIToken.get_or_create(self.org, self.admin, Group.objects.get(name='Administrators'))
        return self.client.post(url, HTTP_AUTHORIZATION=f'Token {token.key}', data=json.dumps(data), content_type='application/json')

    def request_delete(self, data, **kwargs):
        url = self.reverse(self.get_url_namespace(), query_params=kwargs)
        token = APIToken.get_or_create(self.org, self.admin, Group.objects.get(name='Administrators'))
        return self.client.delete(f'{url}', HTTP_AUTHORIZATION=f'Token {token.key}', data=json.dumps(data), content_type='application/json')

    @abstractmethod
    def get_url_namespace(self):
        ...

class UserPermissionUpdateDestroyTestCase(TembaTest, TembaRequestMixin):

    def setUp(self):
        self.admin = User.objects.create_user(username='testuser', password='123', email='test@weni.ai', is_superuser=True)
        super().setUp()

    def test_user_permission_destroy(self):
        org = Org.objects.first()
        user = User.objects.first()
        destroy_wrong_permission = self.request_delete(data=dict(org_uuid=str(org.uuid), user_email=user.email, permission='adm'))
        self.assertEqual(destroy_wrong_permission.status_code, 400)
        self.assertEqual(destroy_wrong_permission.json()[0], 'adm is not a valid permission!')
        self.request_patch(data=dict(org_uuid=str(org.uuid), user_email=user.email, permission='viewer'))
        user_permissions = self._get_user_permissions(org=org, user=user)
        self.request_delete(data=dict(org_uuid=str(org.uuid), user_email=user.email, permission='viewer'))
        user_permissions_removed = self._get_user_permissions(org=org, user=user)
        self.assertFalse(user_permissions_removed.get('viewer', False))
        self.assertNotEquals(user_permissions, user_permissions_removed)

    def test_user_permission_update(self):
        org = Org.objects.first()
        user = User.objects.first()
        update_wrong_permission_response = self.request_patch(data=dict(org_uuid=str(org.uuid), user_email=user.email, permission='adm'))
        self.assertEqual(update_wrong_permission_response.status_code, 400)
        self.assertEqual(update_wrong_permission_response.json()[0], 'adm is not a valid permission!')
        update_response = self.request_patch(data=dict(org_uuid=str(org.uuid), user_email=user.email, permission='administrator')).json()
        user_permissions = self._get_user_permissions(org, user)
        self.assertTrue(user_permissions.get('administrator'))
        self.assertTrue(self._permission_is_unique_true(update_response, 'administrator'))
        update_response = self.request_patch(data=dict(org_uuid=str(org.uuid), user_email=user.email, permission='viewer')).json()
        user_permissions = self._get_user_permissions(org, user)
        self.assertTrue(user_permissions.get('viewer'))
        self.assertTrue(self._permission_is_unique_true(update_response, 'viewer'))
        update_response = self.request_patch(data=dict(org_uuid=str(org.uuid), user_email=user.email, permission='editor')).json()
        user_permissions = self._get_user_permissions(org, user)
        self.assertTrue(user_permissions.get('editor'))
        self.assertTrue(self._permission_is_unique_true(update_response, 'editor'))
        update_response = self.request_patch(data=dict(org_uuid=str(org.uuid), user_email=user.email, permission='surveyor')).json()
        user_permissions = self._get_user_permissions(org, user)
        self.assertTrue(user_permissions.get('surveyor'))
        self.assertTrue(self._permission_is_unique_true(update_response, 'surveyor'))

    def _get_permissions(self, org: Org) -> dict:
        return {'administrator': org.administrators, 'viewer': org.viewers, 'editor': org.editors, 'surveyor': org.surveyors}

    def _get_user_permissions(self, org: Org, user: User) -> dict:
        permissions = {}
        org_permissions = self._get_permissions(org)
        for (perm_name, org_field) in org_permissions.items():
            if org_field.filter(pk=user.id).exists():
                permissions[perm_name] = True
        return permissions

    def _permission_is_unique_true(self, response, permission: str) -> bool:
        permissions = {'administrator': response.get('administrator'), 'viewer': response.get('viewer'), 'editor': response.get('editor'), 'surveyor': response.get('surveyor')}
        false_valeues = [key for (key, value) in permissions.items() if not value]
        return len(false_valeues) == 3 and permission not in false_valeues

    def get_url_namespace(self):
        return 'user_permission'

class UserPermissionRetrieveTestCase(TembaTest, TembaRequestMixin):

    def setUp(self):
        self.admin = User.objects.create_user(username='testuser', password='123', email='test@weni.ai', is_superuser=True)
        super().setUp()

    def test_user_permission_retrieve(self):
        org = Org.objects.first()
        user = User.objects.first()
        response_wrong_org = self.request_detail(org_uuid='f7e70145-6d17-4384-a1f2-d6981397866a', user_email='wrong@weni.ai')
        self.assertEqual(response_wrong_org.status_code, 404)
        self.assertEqual(response_wrong_org.json().get('detail'), 'Not found.')
        org.administrators.add(user)
        response_wrong_user = self.request_detail(org_uuid=org.uuid, user_email=0)
        self.assertEqual(response_wrong_user.status_code, 404)
        self.assertEqual(response_wrong_user.json().get('detail'), 'Not found.')
        response = self.request_detail(org_uuid=org.uuid, user_email=user.email).json()
        self.assertTrue(response.get('administrator'))
        self.assertTrue(self.permission_is_unique_true(response, 'administrator'))
        org.administrators.remove(user)
        org.viewers.add(user)
        response = self.request_detail(org_uuid=org.uuid, user_email=user.email).json()
        self.assertTrue(response.get('viewer'))
        self.assertTrue(self.permission_is_unique_true(response, 'viewer'))
        org.viewers.remove(user)
        org.editors.add(user)
        response = self.request_detail(org_uuid=org.uuid, user_email=user.email).json()
        self.assertTrue(response.get('editor'))
        self.assertTrue(self.permission_is_unique_true(response, 'editor'))
        org.editors.remove(user)
        org.surveyors.add(user)
        response = self.request_detail(org_uuid=org.uuid, user_email=user.email).json()
        self.assertTrue(response.get('surveyor'))
        self.assertTrue(self.permission_is_unique_true(response, 'surveyor'))

    def permission_is_unique_true(self, response, permission: str) -> bool:
        permissions = {'administrator': response.get('administrator'), 'viewer': response.get('viewer'), 'editor': response.get('editor'), 'surveyor': response.get('surveyor')}
        false_valeues = [key for (key, value) in permissions.items() if not value]
        return len(false_valeues) == 3 and permission not in false_valeues

    def get_url_namespace(self):
        return 'user_permission'

class UserUpdateTestCase(TembaTest, TembaRequestMixin):

    def setUp(self):
        self.admin = User.objects.create_user(username='testuser', password='123', email='test@weni.ai', is_superuser=True)
        super().setUp()

    def test_user_language_update(self):
        languages = [language[0] for language in settings.LANGUAGES]
        bad_language_response = self.request_patch(data={'language': 'wrong'}, email=self.admin.email)
        self.assertEqual(bad_language_response.status_code, 400)
        for language in languages:
            self.request_patch(data={'language': language}, email=self.admin.email)
            user_language = User.objects.get(id=self.admin.id).get_settings().language
            self.assertEqual(user_language, language)

    def test_update_user_lang_with_non_existent_user(self):
        bad_user_response = self.request_patch(data={'language': 'wrong'}, email='ssd')
        self.assertEqual(bad_user_response.status_code, 404)
        self.assertEqual(bad_user_response.json().get('detail'), 'Not found.')

    def get_url_namespace(self):
        return 'flow_users-detail'

class UserRetrieveByEmailTestCase(TembaTest, TembaRequestMixin):

    def setUp(self):
        self.admin = User.objects.create_user(username='testuser', password='123', email='test@weni.ai', is_superuser=True)
        super().setUp()

    def test_retrive_user_by_email(self):
        response = self.request_get(email=self.admin.email).json()
        response_user = User.objects.get(id=response.get('id'))
        self.assertEqual(response_user, self.admin)

    def get_url_namespace(self):
        return 'flow_users-detail'