# -*- coding: utf-8 -*-

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

    def fake_response(self):
        return [
            {
                "id_adulto": "232",
                "nom_datos": "Edwin",
                "app_datos": "Acuña",
                "apm_datos": "Motta",
                "naci_datos": "Peruana",
                "sexo": "M",
                "fec_datos": "1987-07-08",
                "tipdoc_datos": "DNI",
                "num_doc_datos": "44426463",
                "pais_datos": "177",
                "dep_datos": "San Juan de Miraflores",
                "dir_datos": "Manuel Jaramillo 629",
                "fijo_datos": "0",
                "movil_datos": "986161752",
                "mail_datos": "DJAxl_rose@hotmail.com",
                "fb_datos": "https://www.facebook.com/edwinpunkeke",
                "yt_datos": "https://www.youtube.com/user/edwinpunkeke",
                "ocu_datos": "Ciencias de la Comunicacion",
                "tip_cab": "Rizado o crespo",
                "larg_cab": "Corto",
                "color_ojos": "Marron",
                "estatura": "1.74",
                "fot1": "232.jpg",
                "fot2": "232-232.jpg",
                "cam_blu": "L",
                "pant": "32",
                "shoes": "43",
                "hobbie": "Fotografía, Rock n Roll https",
                "terminos": "aceptar",
                "status": "0",
                "pais": "PerÃº"
            }
        ]

    @patch("apps.sp.tasks.facebook.TabFacebookTask.get_data")
    def _test_task_save_model(self, mock_get_data):
        self.assertEqual(Model.objects.all().count(), 4)
        mock_get_data.return_value = self.fake_response()
        self.tab_facebook_task.apply()
        self.assertEqual(Model.objects.all().count(), 5)

    @patch("apps.sp.tasks.facebook.TabFacebookTask.get_data")
    def _test_method_get_data(self, mock_get_data):
        mock_get_data.return_value = self.fake_response()
        self.assertEqual(Model.objects.all().count(), 4)
        result = self.tab_facebook_task.run()
        self.assertEqual(Model.objects.all().count(), 5)
        self.assertEquals(result.get('status'), 200)

    def test_method_test_real(self):
        self.assertEqual(Model.objects.all().count(), 4)
        result = self.tab_facebook_task.run()
        self.assertEqual(Model.objects.all().count(), 5)
        self.assertEquals(result.get('status'), 200)