from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

from apps.sp.tests.Helpers.InsertDataHelper import InsertDataHelper
from apps.sp.models.Entry import Entry
from apps.sp.views.panel.Entry import EntryListView, EntryCreateView


class EntryViewTest(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.insert_data_helper = InsertDataHelper()

    def test_list_view_entry(self):
        self.insert_data_helper.insert_data_helper()
        view = EntryListView.as_view()
        request = self.request_factory.get(
            reverse('entry_list')
        )
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['object_list'].count(), 5)
        entry = Entry()
        entry.name = 'Entry test'
        entry.save()
        response = view(request)
        self.assertEqual(response.context_data['object_list'].count(), 6)

    def test_list_view_entry_filter(self):
        self.insert_data_helper.insert_data_helper()
        request = self.request_factory.get(reverse('entry_list'),
                                   data={'name__icontains': 'Telefonia'})
        view = EntryListView.as_view()
        response = view(request)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context_data['object_list']), 1)

    def test_create_view_entry(self):
        self.assertEqual(Entry.objects.all().count(), 0)
        data = {
            'name': 'Entry test'
        }
        view = EntryCreateView.as_view()
        request = self.request_factory.post(
            reverse('entry_create'),data
        )
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Entry.objects.all().count(), 1)