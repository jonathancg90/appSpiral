import json

from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

from apps.sp.tests.Helpers.InsertDataHelper import InsertDataHelper
from apps.sp.views.panel.Model import ModelDataJsonView
from apps.sp.models.Model import Model


class ModelCreateTest(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.insert_data_helper = InsertDataHelper()
        self.insert_test_data()

    def insert_test_data(self):
        self.insert_data_helper.run()

    def test_get_model(self):
        view = ModelDataJsonView.as_view()
        model = Model.objects.latest('created')
        request = self.request_factory.get(
            reverse('panel_information_model', kwargs={'pk': model.pk})
        )
        response = view(request, pk=model.pk)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)

        self.assertTrue('profile' in data)
        self.assertTrue('features' in data)
        self.assertTrue('commercial' in data)
        self.assertTrue('images' in data)

    def test_get_model_fail(self):
        view = ModelDataJsonView.as_view()
        request = self.request_factory.get(
            reverse('panel_information_model', kwargs={'pk': 876})
        )
        response = view(request, pk=876)
        self.assertEqual(response.status_code, 200)
