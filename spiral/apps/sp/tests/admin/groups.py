from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory
from django.contrib.auth.models import User, Group

from apps.sp.tests.Helpers.InsertDataHelper import InsertDataHelper
from apps.sp.views.panel.admin.Group import AdminGroupListView


class GroupsTest(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.client = Client()
        self.insert_data = InsertDataHelper()
        self.insert_default_data()

    def insert_default_data(self):
        self.insert_data.run()
        self.user = User.objects.get(is_superuser=True)

    def test_list_groups(self):
        view = AdminGroupListView.as_view()
        request = self.request_factory.get(
            reverse('admin_user_list')
        )
        request.user = self.user
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['object_list'].count(), 1)
        self.create_user()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['object_list'].count(), 2)