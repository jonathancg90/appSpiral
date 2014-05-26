from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from apps.sp.tests.Helpers.InsertDataHelper import InsertDataHelper
from apps.sp.models.Brand import Brand
from apps.sp.models.Entry import Entry
from apps.sp.views.panel.Brand import BrandListView, BrandCreateView,\
    BrandUpdateView, BrandDeleteView


class BrandViewTest(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.insert_data_helper = InsertDataHelper()

    def insert_test_data(self):
        self.insert_data_helper.run()

    def test_basic_data(self):
        """
        Tests data test insert correct
        """
        self.insert_test_data()
        self.assertTrue(Brand.objects.all().count() > 0)
        self.assertTrue(Entry.objects.all().count() > 0)

    def test_list_view_brand(self):
        """
        Tests data: List
        """
        self.insert_test_data()
        view = BrandListView.as_view()
        request = self.request_factory.get(
            reverse('brand_list')
        )
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['object_list'].count(), 9)
        brand = Brand()
        brand.entry = Entry.objects.latest('id')
        brand.name = 'Brand Test'
        brand.save()
        response = view(request)
        self.assertEqual(response.context_data['object_list'].count(), 10)

    def test_list_view_brand_filter(self):
        """
        Tests data: Filter
        """
        self.insert_test_data()
        request = self.request_factory.get(reverse('brand_list'),
                                   data={'name__icontains': 'Sprite'})
        view = BrandListView.as_view()
        response = view(request)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context_data['object_list']), 1)

    def test_create_view_brand(self):
        """
        Tests data: Create
        """
        self.insert_test_data()
        self.assertEqual(Brand.objects.all().count(), 9)
        data = {
            'name': 'Brand test',
            'entry': Entry.objects.filter(name='Bancos')[0].id
        }
        view = BrandCreateView.as_view()
        request = self.request_factory.post(
            reverse('brand_create'), data
        )
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Brand.objects.all().count(), 10)

    def test_update_view_brand(self):
        """
        Tests data: Update
        """
        self.insert_test_data()
        self.assertEqual(Brand.objects.all().count(), 9)
        brand = Brand.objects.get(pk=1)

        request = self.request_factory.get(reverse('brand_edit',
                                         kwargs={'pk': brand.id}))

        view = BrandUpdateView.as_view()
        response = view(request, pk=brand.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Brand.objects.all().count(), 9)
        self.assertEqual(brand.name, 'Coca Cola')
        #Post
        data = {
            'pk':  brand.id,
            'name': "actualizado",
            'entry': Entry.objects.get(id=1).id
        }

        url_kwargs = {'pk': brand.id}
        url = reverse('brand_edit', kwargs=url_kwargs)
        request = self.request_factory.post(url, data=data)
        view = BrandUpdateView.as_view()
        response = view(request, **data)

        brand = Brand.objects.get(pk=1)
        self.assertEqual(brand.name, 'actualizado')
        self.assertEqual(response.status_code, 302)

    def test_delete_view_brand(self):
        """
        Tests data: Delete
        """
        self.insert_test_data()
        self.assertEqual(Brand.objects.all().count(), 9)
        brand = Brand.objects.get(pk=1)

        kwargs = {'pk': brand.id}
        url = reverse('brand_delete', kwargs=kwargs)
        request = self.request_factory.post(url, kwargs)
        response = BrandDeleteView.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Brand.objects.all().count(), 8)