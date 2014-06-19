import uuid
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory
from django.contrib.auth.models import User

from apps.sp.tests.Helpers.InsertDataHelper import InsertDataHelper
from apps.sp.views.panel.admin.User import AdminUserListView


class UsersTest(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()
        self.client = Client()

    def create_user(self):
        user = User()
        user.username = 'testUser'
        user.set_password(uuid.uuid4().hex)
        user.email = 'testuser@gmail.com'
        user.save()

    def test_no_repeat_username(self):
        pass

    def test_no_repeat_email(self):
        pass

    def test_list_users(self):
        """
        Tests data: List
        """
        view = AdminUserListView.as_view()
        request = self.request_factory.get(
            reverse('brand_list')
        )
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['object_list'].count(), 0)
        self.create_user()
        response = view(request)
        self.assertEqual(response.context_data['object_list'].count(), 1)

    def test_create_user(self):
        pass

    def test_update_state_user(self):
        pass

    def test_update_user(self):
        pass

    def test_assign_group_user(self):
        pass

    def test_permission_dashboard(self):
        pass