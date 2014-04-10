from django.test import TestCase
from apps.sp.tasks.facebook import TabFacebookTask
from apps.sp.tests.Helpers.InsertDataHelper import InsertDataHelper

from apps.sp.models.Model import Model


class FacebookTaskTest(TestCase):

    def setUp(self):
        self.tab_facebook_task = TabFacebookTask()
        insert_data_helper = InsertDataHelper()
        insert_data_helper.run()

    def _test_task_save_model(self):
        self.tab_facebook_task.apply()
        self.tab_facebook_task.apply()
        self.assertEqual(Model.objects.all().count(), 2)

    def test_method_save_data(self):
        self.tab_facebook_task.run()
        self.assertEqual(Model.objects.all().count(), 1)