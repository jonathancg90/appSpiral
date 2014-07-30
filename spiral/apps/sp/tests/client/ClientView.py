from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from apps.sp.tests.Helpers.InsertDataHelper import InsertDataHelper
from apps.sp.models.Client import TypeClient
from apps.sp.models.Client import Client
from apps.sp.views.panel.Client import ClientListView, ClientCreateView, \
    ClientUpdateView, ClientDeleteView


class ClientViewTest(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.insert_data_helper = InsertDataHelper()
        self.insert_test_data()

    def insert_test_data(self):
        self.insert_data_helper.run()
        self.user = User.objects.get(is_superuser=True)

    def test_basic_data(self):
        """
        Tests data test insert correct
        """
        self.assertTrue(TypeClient.objects.all().count() > 0)
        self.assertTrue(Client.objects.all().count() > 0)

    def test_list_view_client(self):
        """
        Tests data: List
        """
        view = ClientListView.as_view()
        request = self.request_factory.get(
            reverse('client_list')
        )
        request.user = self.user
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['object_list'].count(), 3)

        client = Client()
        client.name = 'Client Test'
        client.ruc = '2345654321'
        client.address = 'Direccion'
        client.save()
        response = view(request)
        self.assertEqual(response.context_data['object_list'].count(), 4)

    def test_list_view_brand_filter(self):
        """
        Tests data: Filter
        """
        request = self.request_factory.get(reverse('brand_list'),
                                           data={'name__icontains': 'Produc'})
        request.user = self.user
        view = ClientListView.as_view()
        response = view(request)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context_data['object_list']), 1)

    def test_create_view_brand(self):
        """
        Tests data: Create
        """
        self.assertEqual(Client.objects.all().count(), 3)

        data = {
            'name': 'Brand test',
            'ruc':  '2323232323',
            'address': 'mi direccion',
            'type_client': [TypeClient.objects.get(name='Productora').id]
        }
        view = ClientCreateView.as_view()
        request = self.request_factory.post(
            reverse('client_create'), data
        )
        request.user = self.user
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Client.objects.all().count(), 4)

    def test_update_view_brand(self):
        """
        Tests data: Update
        """
        self.assertEqual(Client.objects.all().count(), 3)
        client = Client.objects.get(name='Productora')

        request = self.request_factory.get(reverse('client_edit',
                                                   kwargs={'pk': client.id})
        )
        request.user = self.user
        view = ClientUpdateView.as_view()
        response = view(request, pk=client.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Client.objects.all().count(), 3)
        self.assertEqual(client.name, 'Productora')
        #Post
        data = {
            'pk':  client.id,
            'name': "actualizado",
            'ruc':  '2323232323',
            'address': 'mi direccion',
            'type_client': [TypeClient.objects.get(name='Productora').id]
        }

        url_kwargs = {'pk': client.id}
        url = reverse('client_edit', kwargs=url_kwargs)
        request = self.request_factory.post(url, data=data)
        request.user = self.user
        view = ClientUpdateView.as_view()
        response = view(request, **data)

        client = Client.objects.get(pk=1)
        self.assertEqual(client.name, 'actualizado')
        self.assertEqual(response.status_code, 302)

    def test_delete_view_brand(self):
        """
        Tests data: Delete
        """
        self.insert_test_data()
        self.assertEqual(Client.objects.all().count(), 3)
        brand = Client.objects.get(pk=1)

        kwargs = {'pk': brand.id}
        url = reverse('brand_delete', kwargs=kwargs)
        request = self.request_factory.post(url, kwargs)
        request.user = self.user
        response = ClientDeleteView.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Client.objects.all().count(), 2)