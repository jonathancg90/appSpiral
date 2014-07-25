import datetime


from django.test import TestCase
from django.utils.timezone import utc
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test.utils import override_settings

from apps.sp.tests.Helpers.InsertDataHelper import InsertDataHelper
from apps.sp.models.Brand import Brand
from apps.sp.models.Entry import Entry
from apps.sp.models.Commercial import Commercial, CommercialDateDetail
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
        self.user = User.objects.get(is_superuser=True)

    def test_basic_data(self):
        """
        Tests data test insert correct
        """
        self.insert_test_data()
        self.assertTrue(Brand.objects.all().count() > 0)
        self.assertTrue(Entry.objects.all().count() > 0)
        self.assertTrue(Project.objects.all().count() > 0)
        self.assertTrue(Commercial.objects.all().count() > 0)

    @override_settings(APPLICATION_CACHE=False)
    def test_list_view_commercial(self):
        """
        Tests List
        """
        self.insert_test_data()
        view = CommercialListView.as_view()
        request = self.request_factory.get(
            reverse('commercial_list')
        )
        request.user = self.user
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data['object_list']), 4)
        commercial = Commercial()
        commercial.brand = Brand.objects.latest('id')
        commercial.save()
        response = view(request)
        self.assertEqual(len(response.context_data['object_list']), 5)

    def test_list_view_commercial_filter(self):
        """
        Tests Filter
        """
        self.insert_test_data()
        request = self.request_factory.get(reverse('commercial_list'),
                                   data={'name__icontains': 'Navidad'}
        )
        request.user = self.user
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
            'name': 'Commercial test',
            'brand': Brand.objects.filter(name='Sprite')[0].id,
            'id_realized': '02/07/2014'
        }
        view = CommercialCreateView.as_view()
        request = self.request_factory.post(
            reverse('commercial_create'), data
        )
        request.user = self.user
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Commercial.objects.all().count(), 5)
        self.assertEqual(CommercialDateDetail.objects.all().count(), 1)

    def test_update_view_commercial(self):
        """
        Tests data: Update
        """
        from datetime import datetime
        self.insert_test_data()
        self.assertEqual(Commercial.objects.all().count(), 4)
        commercial = Commercial.objects.get(pk=1)

        request = self.request_factory.get(reverse('commercial_edit',
                                                   kwargs={'pk': commercial.id})
        )
        request.user = self.user
        view = CommercialUpdateView.as_view()
        response = view(request, pk=commercial.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Commercial.objects.all().count(), 4)
        self.assertEqual(commercial.name, 'Coca Cola Navidad')

        #Post
        data = {
            'pk':  commercial.id,
            'name': "actualizado",
            'brand': Brand.objects.get(id=1).id,
            'realized': '2014-08-08',
        }

        url_kwargs = {'pk': commercial.id}
        url = reverse('commercial_edit', kwargs=url_kwargs)
        request = self.request_factory.post(url, data=data)
        request.user = self.user
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
        request.user = self.user
        response = CommercialDeleteView.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Commercial.objects.all().count(), 3)