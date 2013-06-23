import datetime
from django.test import TestCase
from django.utils.timezone import utc
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from apps.sp.tests.Helpers.InsertDataHelper import InsertDataHelper
from apps.sp.models.Brand import Brand
from apps.sp.models.Entry import Entry
from apps.sp.models.Commercial import Commercial
from apps.sp.models.Project import Project
from apps.sp.views.Commercial import CommercialListView, CommercialCreateView ,\
    CommercialUpdateView, CommercialDeleteView


class CommercialViewTest(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.insert_data_helper = InsertDataHelper()
        self.date = datetime.datetime.now().utcnow().replace(tzinfo=utc)

    def insert_test_data(self):
        self.insert_data_helper.insert_data_helper()

    def test_basic_data(self):
        """
        Tests data test insert correct
        """
        self.insert_test_data()
        self.assertTrue(Brand.objects.all().count() > 0)
        self.assertTrue(Entry.objects.all().count() > 0)
        self.assertTrue(Project.objects.all().count() > 0)
        self.assertTrue(Commercial.objects.all().count() > 0)

    def test_list_view_commercial(self):
        self.insert_test_data()
        view = CommercialListView.as_view()
        request = self.request_factory.get(
            reverse('commercial_list')
        )
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['object_list'].count(), 4)
        commercial = Commercial()
        commercial.brand = Brand.objects.latest('id')
        commercial.realized = self.date
        commercial.save()
        response = view(request)
        self.assertEqual(response.context_data['object_list'].count(), 5)

    def test_list_view_commercial_filter(self):
        self.insert_test_data()
        request = self.request_factory.get(reverse('commercial_list'),
                                   data={'name__icontains': 'Navidad'})
        view = CommercialListView.as_view()
        response = view(request)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context_data['object_list']), 1)






