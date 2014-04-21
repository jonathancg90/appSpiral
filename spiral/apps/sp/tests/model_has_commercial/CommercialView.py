import datetime

from django.test import TestCase
from django.utils.timezone import utc
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from dateutil.relativedelta import relativedelta

from apps.sp.tests.Helpers.InsertDataHelper import InsertDataHelper
from apps.sp.models.Brand import Brand
from apps.sp.models.Entry import Entry
from apps.sp.models.Commercial import Commercial
from apps.sp.models.Project import Project
from apps.sp.views.panel.Commercial import CommercialListView, CommercialCreateView, \
    CommercialUpdateView, CommercialDeleteView


class CommercialViewTest(TestCase):

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
        self.assertTrue(Project.objects.all().count() > 0)
        self.assertTrue(Commercial.objects.all().count() > 0)

    def test_list_view_commercial(self):
        """
        Tests List
        """
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
        """
        Tests Filter
        """
        self.insert_test_data()
        request = self.request_factory.get(reverse('commercial_list'),
                                   data={'name__icontains': 'Navidad'})
        view = CommercialListView.as_view()
        response = view(request)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context_data['object_list']), 1)

    def test_create_view_commercial(self):
        """
        Tests Create
        """
        self.insert_test_data()
        self.assertEqual(Commercial.objects.all().count(), 4)
        data = {
            'name': 'Brand test',
            'brand': Brand.objects.filter(name='Sprite')[0].id,
            'realized':'2013-08-06',
            'project': '13-08M120'
        }
        view = CommercialCreateView.as_view()
        request = self.request_factory.post(
            reverse('commercial_create'), data
        )
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Commercial.objects.all().count(), 5)

    def test_update_view_commercial(self):
        """
        Tests data: Update
        """
        from datetime import datetime
        self.insert_test_data()
        self.assertEqual(Commercial.objects.all().count(), 4)
        commercial = Commercial.objects.get(pk=1)

        request = self.request_factory.get(reverse('commercial_edit',
                                                   kwargs={'pk': commercial.id}))

        view = CommercialUpdateView.as_view()
        response = view(request, pk=commercial.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Commercial.objects.all().count(), 4)
        self.assertEqual(commercial.name, 'Coca Cola Navidad')

        date = datetime.today().utcnow().replace(tzinfo=utc)
        date = date + relativedelta(days=1)
        #Post
        data = {
            'pk':  commercial.id,
            'name': "actualizado",
            'brand': Brand.objects.get(id=1).id,
            'realized': date.strftime("%Y/%m/%d"),
            'project': ''
        }

        url_kwargs = {'pk': commercial.id}
        url = reverse('commercial_edit', kwargs=url_kwargs)
        request = self.request_factory.post(url, data=data)
        view = CommercialUpdateView.as_view()
        response = view(request, **data)

        commercial = Commercial.objects.get(pk=1)
        self.assertEqual(commercial.name, 'actualizado')
        self.assertEqual(response.status_code, 302)

    def test_delete_view_brand(self):
        """
        Tests data: Delete
        """
        self.insert_test_data()
        self.assertEqual(Commercial.objects.all().count(), 4)
        commercial = Commercial.objects.get(pk=1)

        kwargs = {'pk': commercial.id}
        url = reverse('commercial_delete', kwargs=kwargs)
        request = self.request_factory.post(url, kwargs)
        response = CommercialDeleteView.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Commercial.objects.all().count(), 3)