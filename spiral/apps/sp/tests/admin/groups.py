from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory
from django.contrib.auth.models import User, Group, Permission

from apps.sp.tests.Helpers.InsertDataHelper import InsertDataHelper
from apps.sp.views.panel.admin.Group import AdminGroupListView, \
    AdminGroupCreateView, AdminGroupEditView, AdminGroupDeleteView


class GroupsTest(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.client = Client()
        self.insert_data = InsertDataHelper()
        self.insert_default_data()

    def insert_default_data(self):
        self.insert_data.run()
        self.user = User.objects.get(is_superuser=True)

    def create_group(self):
        group = Group()
        group.name = 'testGroup'
        group.save()

    def test_list_groups(self):
        view = AdminGroupListView.as_view()
        request = self.request_factory.get(
            reverse('admin_group_list')
        )
        request.user = self.user
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['object_list'].count(), 2)
        self.create_group()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['object_list'].count(), 3)

    def test_create_group(self):
        """
         Tests data: Create
         """
        self.assertEqual(Group.objects.all().count(), 2)
        data = {
            'name': 'groupTestCreate',
            'permission1': Permission.objects.get(pk=1).id,
            'permission2': Permission.objects.get(pk=2).id,
            'permission3': Permission.objects.get(pk=3).id
        }

        view = AdminGroupCreateView.as_view()
        request = self.request_factory.post(
            reverse('admin_group_create'), data
        )
        request.user = self.user
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Group.objects.all().count(), 3)
        group = Group.objects.get(name='groupTestCreate')
        self.assertEqual(group.permissions.all().count(), 3)

    def test_update_Group(self):
        group = Group.objects.get(pk=1)
        self.assertEqual(group.permissions.all().count(), 0)
        data = {
            'pk': group.id,
            'name': 'groupTestUpdate',
            'permission1': Permission.objects.get(pk=1).id,
            'permission2': Permission.objects.get(pk=2).id,
            'permission3': Permission.objects.get(pk=3).id
        }

        url_kwargs = {'pk': group.id}

        view = AdminGroupEditView.as_view()
        request = self.request_factory.post(
            reverse('admin_group_edit', kwargs=url_kwargs), data
        )
        request.user = self.user
        response = view(request, **data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Group.objects.all().count(), 2)
        group = Group.objects.get(name='groupTestUpdate')
        self.assertEqual(group.permissions.all().count(), 3)

    def test_delete_group(self):
        self.assertEqual(Group.objects.all().count(), 2)
        group = Group.objects.get(pk=1)
        data = {
            'deleteGroup': group.id,
        }

        view = AdminGroupDeleteView.as_view()
        request = self.request_factory.post(
            reverse('admin_group_delete'), data
        )
        request.user = self.user
        response = view(request, **data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Group.objects.all().count(), 1)

