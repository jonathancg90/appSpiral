from django.test import TestCase
from mock import patch
from apps.sp.tasks.facebook import TabFacebookTask
from apps.sp.tests.Helpers.InsertDataHelper import InsertDataHelper

from apps.sp.models.Model import Model


class FacebookTaskTest(TestCase):

    def setUp(self):
        self.tab_facebook_task = TabFacebookTask()
        insert_data_helper = InsertDataHelper()
        insert_data_helper.run()

    @patch("apps.sp.tasks.facebook.TabFacebookTask.get_data")
    def test_task_save_model(self, mock_get_data):
        mock_get_data.return_value = [
            {
                "name":"jonathan",
                "last_name":"Carrasco",
                "type_doc":"DNI",
                "num_doc":"46443224",
                "address":"av. catalino miranda 356 Barranco",
                "email":"jonathancg90@gmail.com",
                "birth":"1990-08-12",
                "nationality":"Peruana",
                "image":"http://spiral.com.pe/facebook/slide/imgs/1.jpg"
            }
        ]
        self.tab_facebook_task.apply()
        self.assertEqual(Model.objects.all().count(), 1)

    @patch("apps.sp.tasks.facebook.TabFacebookTask.get_data")
    def test_method_save_data(self, mock_get_data):
        mock_get_data.return_value = [
            {
                "name":"jonathan",
                "last_name":"Carrasco",
                "type_doc":"DNI",
                "num_doc":"46443224",
                "address":"av. catalino miranda 356 Barranco",
                "email":"jonathancg90@gmail.com",
                "birth":"1990-08-12",
                "nationality":"Peruana",
                "image":"http://spiral.com.pe/facebook/slide/imgs/1.jpg"
            }
        ]
        self.tab_facebook_task.run()
        self.assertEqual(Model.objects.all().count(), 1)