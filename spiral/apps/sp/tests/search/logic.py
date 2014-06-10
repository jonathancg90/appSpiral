
from django.test import TestCase

from apps.sp.tests.Helpers.InsertDataHelper import InsertDataHelper
from apps.sp.models.Model import Model, ModelFeatureDetail
from apps.sp.models.Model import ModelFeatureDetail
from apps.sp.logic.search import Search


class SearchLogicTest(TestCase):

    def setUp(self):
        self.search = Search()
        self.insert_data_helper = InsertDataHelper()
        self.insert_test_data()

    def insert_test_data(self):
        self.insert_data_helper.run()

    def test_data_inserted(self):
        _count_model = Model.objects.all().count()
        _count_model_feature = ModelFeatureDetail.objects.all().count()
        self.assertTrue(_count_model > 0)
        self.assertTrue(_count_model_feature > 0)

    def test_basic_search(self):
        data = {'text': 'Jonathan'}
        self.search.set_type(Search.TYPE_BASIC)

        #Name
        self.search.set_params(data)
        result = self.search.run()
        self.assertEquals(len(result), 2)

        #Not found
        self.search = Search()
        data = {'text': 'cualquiera'}
        self.search.set_params(data)
        result = self.search.run()
        self.assertEquals(len(result), 0)

        #Lastname
        self.search = Search()
        data = {'text': 'de la cruz'}
        self.search.set_params(data)
        result = self.search.run()
        self.assertEquals(len(result), 1)

        #Number
        self.search = Search()
        data = {'text': '96372543756'}
        self.search.set_params(data)
        result = self.search.run()
        self.assertEquals(len(result), 1)

        #Name and LastName
        self.search = Search()
        data = {'text': 'Jonathan perez'}
        self.search.set_params(data)
        result = self.search.run()
        self.assertEquals(len(result), 2)

        #ExactName and LastName
        self.search = Search()
        data = {'text': 'Jonathan perez'}
        self.search.set_mode(Search.MODE_SENSITIVE)
        self.search.set_params(data)
        result = self.search.run()
        self.assertEquals(len(result), 1)

        #ExactName and LastName
        self.search = Search()
        data = {'text': '96372543756 perez'}
        self.search.set_mode(Search.MODE_SENSITIVE)
        self.search.set_params(data)
        result = self.search.run()
        self.assertEquals(len(result), 0)

    def test_advance_search_features(self):
        model = Model.objects.latest('created')
        model_features = model.model_feature_detail_set.all()
        data = {
            'advance': [],
            'features': [
                {
                    'id': model_features[0].feature_value.id,
                    'text': 'Tipo-de-cabello-Lacio',
                    'feature': True
                }
            ]
        }
        self.search.set_type(Search.TYPE_ADVANCE)
        #Features
        self.search.set_params(data)
        result = self.search.run()
        self.assertEquals(len(result), 2)

    def test_advance_search_age(self):
        data = {
            'advance': [
                {
                    'camp': 'sp_model.birth',
                    'id': ['15', '25'],
                    'feature': False
                }
            ],
            'features': []
        }
        self.search.set_type(Search.TYPE_ADVANCE)
        #Age
        self.search.set_params(data)
        result = self.search.run()
        self.assertEquals(len(result), 2)

    def test_advance_search_feature_params(self):
        model = Model.objects.latest('created')
        model_features = model.model_feature_detail_set.all()
        data = {
            'advance': [
                {
                    'camp': 'sp_model.birth',
                    'id': ['15', '25'],
                    'feature': False
                }
            ],
            'features': [
                {
                    'id': model_features[0].feature_value.id,
                    'text': 'Tipo-de-cabello-Lacio',
                    'feature': True
                }
            ]
        }
        self.search.set_type(Search.TYPE_ADVANCE)
        #Features and Age
        self.search.set_params(data)
        result = self.search.run()
        self.assertEquals(len(result), 1)

    def test_advance_search_web_casting(self):
        model = Model.objects.latest('created')
        model_features = model.model_feature_detail_set.all()
        data = {
            'advance': [
                {
                    'camp': 'sp_model.last_visit',
                    'id': False,
                    'feature': False
                }
            ],
            'features': []
        }
        self.search.set_type(Search.TYPE_ADVANCE)
        #Features and Age
        self.search.set_params(data)
        result = self.search.run()
        self.assertEquals(len(result), 3)
