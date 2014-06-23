import uuid
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory
from django.contrib.auth.models import User, Group

from django.contrib.messages.storage.fallback import FallbackStorage
from apps.sp.tests.Helpers.InsertDataHelper import InsertDataHelper
from apps.sp.views.panel.admin.User import AdminUserListView, \
    AdminUserCreateView, AdminUserChangeStatusRedirectView, \
    AdminUserUpdateView, AdminUserDetailView
from apps.sp.views.panel.Dashboard import SettingsTemplateView


class UsersTest(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()
        self.client = Client()
        self.insert_data = InsertDataHelper()
        self.insert_default_data()

    def insert_default_data(self):
        self.insert_data.run()
        self.user = User.objects.get(is_superuser=True)

    def create_user(self):
        self.user = User()
        self.user.username = 'testUser'
        self.user.set_password(uuid.uuid4().hex)
        self.user.email = 'testuser@gmail.com'
        self.user.save()

    def test_list_users(self):
        """
        Tests data: List
        """
        view = AdminUserListView.as_view()
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

    def test_create_user(self):
        """
         Tests data: Create
         """
        self.assertEqual(User.objects.all().count(), 1)
        data = {
            'username': 'newUser',
            'first_name': '',
            'last_name': '',
            're_password': '321',
            'password': '321',
            'email': 'test@gmail.com',
            'groups': []
        }

        view = AdminUserCreateView.as_view()
        request = self.request_factory.post(
            reverse('admin_user_create'), data
        )
        request.user = self.user
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.all().count(), 2)

    def test_create_user_password_invalid(self):
        """
        Tests data: Create
        """
        self.assertEqual(User.objects.all().count(), 1)
        data = {
            'username': 'newUser',
            'first_name': '',
            'last_name': '',
            're_password': '321',
            'password': '312321321',
            'email': 'test@gmail.com',
            'groups': []
        }

        view = AdminUserCreateView.as_view()
        request = self.request_factory.post(
            reverse('admin_user_create'), data
        )
        request.user = self.user
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 1)

    def test_update_state_user(self):
        self.assertEqual(self.user.is_active, True)
        url_kwargs = {'pk': self.user.id}
        url = reverse('admin_user_change_status', kwargs=url_kwargs)
        request = self.request_factory.get(url)
        request.user = self.user
        view = AdminUserChangeStatusRedirectView.as_view()
        response = view(request, pk=self.user.id)
        user = User.objects.get(is_superuser=True)
        self.assertEqual(user.is_active, False)
        self.assertEqual(response.status_code, 302)

    def test_update_user(self):
        """
        Tests data: Update
        """
        self.assertEqual(User.objects.all().count(), 1)
        user = User.objects.get(is_superuser=True)

        request = self.request_factory.get(reverse('admin_user_update',
                                                   kwargs={'pk': user.id}))
        request.user = self.user
        view = AdminUserUpdateView.as_view()
        response = view(request, pk=user.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(user.first_name, '')
        #Post
        data = {
            'pk':  user.id,
            'username': 'admin',
            'first_name': 'administrador',
            'last_name': '',
            're_password': '321',
            'password': '321',
            'email': 'admin@gmail.com',
            'groups': []
        }

        url_kwargs = {'pk': user.id}
        url = reverse('admin_user_update', kwargs=url_kwargs)
        request = self.request_factory.post(url, data=data)
        request.user = self.user
        view = AdminUserUpdateView.as_view()
        response = view(request, **data)

        user = User.objects.get(is_superuser=True)
        self.assertEqual(user.first_name, 'administrador')
        self.assertEqual(response.status_code, 302)

    def test_assign_group_user(self):
        """
        Tests data: Update
        """
        user_group = self.user.groups.all()
        self.assertEqual(user_group.count(), 0)
        request = self.request_factory.get(reverse('admin_user_group_detail',
                                                   kwargs={'pk': self.user.id}))
        request.user = self.user
        view = AdminUserDetailView.as_view()
        response = view(request, pk=self.user.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user_group.count(), 0)
        #Post
        data = {
            'pk': self.user.id,
            'group': Group.objects.get(pk=1).id
        }

        url_kwargs = {'pk': self.user.id}
        url = reverse('admin_user_group_detail', kwargs=url_kwargs)
        request = self.request_factory.post(url, data=data)
        request.user = self.user
        view = AdminUserDetailView.as_view()
        response = view(request, **data)

        user = User.objects.get(is_superuser=True)
        user_group = user.groups.all()
        self.assertEqual(user_group.count(), 1)
        self.assertEqual(response.status_code, 302)

    def test_permission_dashboard(self):
        #SuperAdmin
        view = SettingsTemplateView.as_view()
        request = self.request_factory.get(
            reverse('admin_settings')
        )
        request.user = self.user
        response = view(request)
        self.assertEqual(response.status_code, 200)
        #Other User
        self.create_user()
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = view(request)
        self.assertEqual(response.status_code, 302)