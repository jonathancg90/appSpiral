from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from apps.sp.tests.Helpers.InsertDataHelper import InsertDataHelper
from apps.sp.models.Studio import Studio
from apps.sp.views.panel.Studio import StudioListView, StudioCreateView, \
    StudioUpdateView, StudioDeleteView


class StudioViewTest(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.insert_data_helper = InsertDataHelper()
        self.insert_test_data()

    def insert_test_data(self):
        self.insert_data_helper.run()
        self.user = User.objects.get(is_superuser=True)

    def test_list_view_studio(self):
        """
        Tests data: List
        """
        view = StudioListView.as_view()
        request = self.request_factory.get(
            reverse('studio_list')
        )
        request.user = self.user
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['object_list'].count(), 0)

        studio = Studio()
        studio.name = 'Client Test'
        studio.save()
        response = view(request)
        self.assertEqual(response.context_data['object_list'].count(), 1)

    def test_create_view_studio(self):
        """
        Tests data: Create
        """
        self.assertEqual(Studio.objects.all().count(), 0)

        data = {
            'name': 'Studio test',
        }
        view = StudioCreateView.as_view()
        request = self.request_factory.post(
            reverse('studio_create'), data
        )
        request.user = self.user
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Studio.objects.all().count(), 1)

    def test_update_view_brand(self):
        """
        Tests data: Update
        """
        self.assertEqual(Studio.objects.all().count(), 0)
        studio = Studio()
        studio.name = 'studio test'
        studio.save()

        request = self.request_factory.get(reverse('studio_edit',
                                                   kwargs={'pk': studio.id})
        )
        request.user = self.user
        view = StudioUpdateView.as_view()
        response = view(request, pk=studio.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Studio.objects.all().count(), 1)
        self.assertEqual(studio.name, 'studio test')
        #Post
        data = {
            'pk':  studio.id,
            'name': "actualizado",
        }

        url_kwargs = {'pk': studio.id}
        url = reverse('client_edit', kwargs=url_kwargs)
        request = self.request_factory.post(url, data=data)
        request.user = self.user
        view = StudioUpdateView.as_view()
        response = view(request, **data)

        client = Studio.objects.get(pk=1)
        self.assertEqual(client.name, 'actualizado')
        self.assertEqual(response.status_code, 302)

    def test_delete_view_brand(self):
        """
        Tests data: Delete
        """
        studio = Studio()
        studio.name = 'studio test'
        studio.save()
        studio = Studio.objects.get(pk=1)
        self.assertEqual(Studio.objects.all().count(), 1)

        kwargs = {'pk': studio.id}
        url = reverse('studio_delete', kwargs=kwargs)
        request = self.request_factory.post(url, kwargs)
        request.user = self.user
        response = StudioDeleteView.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Studio.objects.all().count(), 0)