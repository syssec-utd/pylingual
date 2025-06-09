from django.conf import settings
from django.urls import reverse
from django.test import override_settings
from garpix_user.models import UserSession
from garpix_user.tests.utils.settings import GARPIX_USER_SETTINGS
from garpix_user.tests.utils.test_case_mixin import ApiTestMixin
from rest_framework.test import APIClient
from django.utils.translation import ugettext_lazy as _
BASE_GARPIX_USER_SETTINGS = getattr(settings, 'GARPIX_USER', dict())

class UserSessionApiTest(ApiTestMixin):

    def setUp(self):
        self.set_init_data()
        self.client = APIClient()

    def test_create_user_session(self):
        """
        Check creation of user session
        """
        response = self.client.post(reverse('garpix_user:garpix_user_api:api_user_session-create-user-session'), HTTP_ACCEPT='application/json', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('session_user', response.json())
        token = response.json()['session_user']['token_number']
        self.assertNotEqual(UserSession.objects.filter(token_number=token).first(), None)

    def test_set_user_to_user_session(self):
        """
        Check creation of user session for authorized user
        """
        self.user_login()
        response = self.client.post(reverse('garpix_user:garpix_user_api:api_user_session-create-user-session'), HTTP_ACCEPT='application/json', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('session_user', response.json())
        token = response.json()['session_user']['token_number']
        user_session = UserSession.objects.filter(token_number=token).first()
        self.assertEqual(user_session.user, self.user)

    @override_settings(GARPIX_USER=GARPIX_USER_SETTINGS)
    def test_restore_password(self):
        """
        Check restore password functionality
        """
        if BASE_GARPIX_USER_SETTINGS.get('USE_RESTORE_PASSWORD', False):
            self.User.USERNAME_FIELDS = ('phone', 'email')
            self.check_password_restore(self.user_data, 'email')
            self.check_password_restore_less_than_one_minute(self.user_data, 'email')
            self.user = self.User.objects.create_user(**self.new_user_data)
            self.check_password_restore(self.new_user_data, 'phone')
            self.check_password_restore_less_than_one_minute(self.user_data, 'phone')

    def check_password_restore(self, user_data, field):
        response = self.client.post(reverse('garpix_user:garpix_user_api:api_restore_password-send-code'), {'username': user_data.get(field)}, HTTP_ACCEPT='application/json', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token_number', response.json())
        token = response.json()['token_number']
        user_session = UserSession.objects.get(token_number=token)
        response = self.client.post(reverse('garpix_user:garpix_user_api:api_restore_password-check-code'), {'restore_password_confirm_code': user_session.restore_password_confirm_code}, HTTP_ACCEPT='application/json', format='json', **{f'HTTP_{UserSession.HEAD_NAME}': token})
        self.assertEqual(response.status_code, 204)
        response = self.client.post(reverse('garpix_user:garpix_user_api:api_restore_password-set-password'), {'new_password': 'pAsSwOrD12345'}, HTTP_ACCEPT='application/json', format='json', **{f'HTTP_{UserSession.HEAD_NAME}': token})
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {'result': _('Password was updated!')})
        response = self.client.post(reverse('garpix_user:garpix_user_api:api_login'), {'username': user_data.get(field), 'password': 'pAsSwOrD12345'}, HTTP_ACCEPT='application/json')
        self.check_login_result(response)

    def check_password_restore_less_than_one_minute(self, user_data, field):
        response = self.client.post(reverse('garpix_user:garpix_user_api:api_restore_password-send-code'), {'username': user_data.get(field)}, HTTP_ACCEPT='application/json', format='json')
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json(), {'non_field_error': [_('Less than 1 minutes has passed since the last request')]})