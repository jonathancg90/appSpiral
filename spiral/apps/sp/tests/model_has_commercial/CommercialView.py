from django.test import TestCase
from apps.sp.tests.Helpers.InsertDataHelper import InsertDataHelper
from apps.sp.models.Brand import Brand


class SimpleTest(TestCase):

    def setUp(self):
        self.insert_data_helper = InsertDataHelper()

    def insert_test_data(self):
        self.insert_data_helper.insert_data_helper()

    def test_basic_data(self):
        """
        Tests data test insert correct
        """
        self.insert_test_data()
        self.assertTrue(Brand.objects.all().count() > 0)

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)



