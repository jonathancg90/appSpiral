
from django.test import TestCase

from apps.sp.tests.Helpers.InsertDataHelper import InsertDataHelper


class SearchLogicTest(TestCase):

    def setUp(self):
        self.insert_data_helper = InsertDataHelper()

    def insert_test_data(self):
        self.insert_data_helper.run()

    def test_data_inserted(self):
        pass
