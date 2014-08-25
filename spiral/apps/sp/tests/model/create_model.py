import json

from json import dumps
from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from apps.sp.views.panel.Model import ModelCreateView, ModelUpdateView,\
    ModelFeatureCreateView, ModelFeatureUpdateView, ModelFeatureDeleteView
from apps.sp.tests.Helpers.InsertDataHelper import InsertDataHelper
from apps.sp.views.panel.Model import ModelDataJsonView, \
    ModelControlTemplateView
from apps.sp.models.Model import Model
from django.test.client import Client

from apps.sp.models.Model import ModelFeatureDetail
from apps.sp.models.Feature import FeatureValue


class ModelCreateTest(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.client = Client()
        self.insert_data_helper = InsertDataHelper()
        self.insert_test_data()

    def insert_test_data(self):
        self.insert_data_helper.run()
        self.user = User.objects.get(is_superuser=True)

    def test_template_model_create(self):
        self.assertEqual(Model.objects.all().count(), 4)
        view = ModelControlTemplateView.as_view()
        model = Model.objects.latest('created')
        request = self.request_factory.get(
            reverse('panel_model_control_list') + '?pk=' + str(model.model_code)
        )
        request.user = self.user
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data), 7)
        self.assertTrue('doc_types' in response.context_data)
        self.assertTrue('genders' in response.context_data)
        self.assertTrue('menu' in response.context_data)
        self.assertTrue('features' in response.context_data)
        self.assertTrue('id' in response.context_data)
        self.assertTrue('pk' in response.context_data)

    def test_get_model(self):
        view = ModelDataJsonView.as_view()
        model = Model.objects.latest('created')
        request = self.request_factory.get(
            reverse('panel_information_model', kwargs={'pk': model.model_code})
        )
        request.user = self.user
        response = view(request, pk=model.model_code)
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
        request.user = self.user
        response = view(request, pk=876)
        content = json.loads(response._container[0])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content.get('status'), "warning")

    def test_save_model(self):
        self.assertEqual(Model.objects.all().count(), 4)
        data = {
            "name_complete": "jonathancarrasco garcia",
            "type_doc": {"id": 1,"name": "DNI"},
            "num_doc": "46223224",
            "address": "Jr catalino Miranda 356",
            "email": "jonathancg90@gmail.com",
            "birth": "1978-08-12",
            "nationality": 1,
            "city": 66,
            "phone_fixed": "256-1212",
            "phone_mobil": "963726756",
            "gender": 1
        }

        view = ModelCreateView.as_view()
        request = self.request_factory.post(
            reverse('panel_model_save_profile'), data=dumps(data), content_type='application/json'
        )
        request.user = self.user
        response = view(request)
        self.assertEqual(response.status_code, 200)
        content = json.loads(response._container[0])
        self.assertEqual(content.get('status'), "success")
        self.assertEqual(Model.objects.all().count(), 5)

    def test_update_model(self):
        self.assertEqual(Model.objects.all().count(), 4)
        model = Model.objects.latest('created')
        url = reverse('panel_model_update_profile',  kwargs={'pk': model.id})
        data = {
            "name_complete": "jonathancarrasco garcia",
            "type_doc": {"id": 1,"name": "DNI"},
            "num_doc": "46223224",
            "address": "Jr catalino Miranda 356",
            "email": "jonathancg90@gmail.com",
            "birth": "1978-08-12",
            "nationality": 1,
            "city": 66,
            "phone_fixed": "256-1212",
            "phone_mobil": "963726756",
            "gender": 1
        }
        view = ModelUpdateView.as_view()
        request = self.request_factory.post(
            url, data=dumps(data), content_type='application/json'
        )
        request.user = self.user
        response = view(request, pk=model.id)
        content = json.loads(response._container[0])
        self.assertEqual(content.get('status'), "success")
        self.assertEqual(Model.objects.all().count(), 4)

    def test_save_features(self):
        model = Model.objects.latest('created')
        self.assertEqual(model.model_feature_detail_set.all().count(), 1)
        url = reverse('panel_model_save_feature',  kwargs={'pk': model.id})
        data = {
            "feature_value": {
                "value_id": 138,
                "value_name": "Facebook"
            }
        }
        view = ModelFeatureCreateView.as_view()
        request = self.request_factory.post(
            url, data=dumps(data), content_type='application/json'
        )
        request.user = self.user
        response = view(request, pk=model.id)
        content = json.loads(response._container[0])
        self.assertEqual(content.get('status'), 'success')
        self.assertEqual(model.model_feature_detail_set.all().count(), 2)

    def test_update_features(self):
        model = Model.objects.latest('created')
        self.assertEqual(model.model_feature_detail_set.all().count(), 1)
        model_feature_detail = ModelFeatureDetail()
        model_feature_detail.model = model
        model_feature_detail.feature_value = FeatureValue.objects.get(pk=139)
        model_feature_detail.description = 'Facebook'
        model_feature_detail.save()

        url = reverse('panel_model_update_feature',  kwargs={'pk': model.id})
        data = {
                "feature": {
                    "value_id": 139,
                    "value_name": "Twitter"
                },
            "description": "olalal",
            "model_feature_id": model_feature_detail.id
        }
        view = ModelFeatureUpdateView.as_view()
        request = self.request_factory.post(
            url, data=dumps(data), content_type='application/json'
        )
        request.user = self.user
        response = view(request, pk=model.id)
        content = json.loads(response._container[0])
        self.assertEqual(content.get('status'), 'success')
        self.assertEqual(model.model_feature_detail_set.all().count(), 2)

    def test_delete_features(self):
        model = Model.objects.latest('created')
        model_feature_detail = ModelFeatureDetail()
        model_feature_detail.model = model
        model_feature_detail.feature_value = FeatureValue.objects.get(pk=139)
        model_feature_detail.description = 'Facebook'
        model_feature_detail.save()
        self.assertEqual(model.model_feature_detail_set.all().count(), 2)

        url = reverse('panel_model_delete_feature')
        data = str(model_feature_detail.id)
        view = ModelFeatureDeleteView.as_view()
        request = self.request_factory.post(
            url, data=dumps(data), content_type='application/json'
        )
        request.user = self.user
        response = view(request)
        content = json.loads(response._container[0])
        self.assertEqual(content.get('status'), 'success')
        self.assertEqual(model.model_feature_detail_set.all().count(), 1)
