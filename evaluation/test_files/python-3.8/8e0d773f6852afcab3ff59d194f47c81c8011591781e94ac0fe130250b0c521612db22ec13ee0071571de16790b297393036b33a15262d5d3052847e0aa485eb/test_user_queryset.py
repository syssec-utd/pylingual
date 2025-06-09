from django.test import TestCase
from pfx.pfxcore.test import TestAssertMixin
from tests.models import Author, User

class TestUserQuerySet(TestAssertMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='user', email='user@example.com', password='test', first_name='User', last_name='Test')
        cls.admin = User.objects.create_user(username='admin', email='admin@example.com', password='test', first_name='Admin', last_name='Test', is_superuser=True)
        cls.author1 = Author.objects.create(first_name='John Ronald Reuel', last_name='Tolkien', slug='jrr-tolkien')
        cls.author2 = Author.objects.create(first_name='Philip Kindred', last_name='Dick', science_fiction=True, slug='philip-k-dick')

    def test_user_queryset(self):
        authors = Author._default_manager.all()
        self.assertEqual(len(authors), 2)
        authors = Author.user_objects.user(self.user)
        self.assertEqual(len(authors), 1)
        authors = Author.user_objects.user(self.admin)
        self.assertEqual(len(authors), 2)

    def test_bad_user_queryset(self):
        with self.assertRaises(NotImplementedError):
            Author.bad_user_objects.user(self.user)