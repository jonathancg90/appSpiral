
from django.test import TestCase

from apps.sp.tests.Helpers.InsertDataHelper import InsertDataHelper
from apps.sp.models.Model import Model, ModelFeatureDetail
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
        data = {
            'text': 'Jonathan'
        }
        self.search.set_type(Search.TYPE_BASIC)
        self.search.set_params(data)
        result = self.search.run()
        self.assertEquals(len(result), 1)
