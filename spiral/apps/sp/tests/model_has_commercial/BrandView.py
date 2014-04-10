import datetime
from django.test import TestCase
from django.utils.timezone import utc
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from apps.sp.tests.Helpers.InsertDataHelper import InsertDataHelper
from apps.sp.models.Brand import Brand
from apps.sp.models.Entry import Entry
from apps.sp.views.panel.Brand import BrandListView, BrandCreateView


class BrandViewTest(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.insert_data_helper = InsertDataHelper()
        self.date = datetime.datetime.now().utcnow().replace(tzinfo=utc)

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
        self.insert_test_data()
        request = self.request_factory.get(reverse('brand_list'),
                                   data={'name__icontains': 'Sprite'})
        view = BrandListView.as_view()
        response = view(request)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context_data['object_list']), 1)

    def test_create_view_brand(self):
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