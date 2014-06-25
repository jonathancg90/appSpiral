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
                "id_adulto": "425",
                "nom_datos": "lucero",
                "app_datos": "ore",
                "apm_datos": "tragodara",
                "naci_datos": "177",
                "sexo": "F",
                "fec_datos": "2014-06-25",
                "tipdoc_datos": "DNI",
                "num_doc_datos": "76692889",
                "pais_datos": "177",
                "dep_datos": "lima",
                "dir_datos": "av.javier prado #7456",
                "fijo_datos": "0",
                "movil_datos": "994407300",
                "mail_datos": "janellis.jlo.lo@hotmail.com",
                "fb_datos": "https://www.facebook.com/luceritho.peluche",
                "yt_datos": "http://www.youtube.com/watch?v=ebXbLfLACGM",
                "ocu_datos": "Administracion",
                "tip_cab": "Ondulado",
                "larg_cab": "Mediano",
                "color_ojos": "Negro",
                "estatura": "1.63",
                "fot1": "424.jpg",
                "fot2": "",
                "cam_blu": "S",
                "pant": "28",
                "shoes": "36",
                "hobbie": "actuar, bailar ,escuchar music",
                "terminos": "aceptar",
                "status": "0",
                "pais": "Perú",
                "naci": "Perú"
            }
        ]

    @patch("apps.sp.tasks.facebook.TabFacebookTask.get_data")
    def test_task_save_model(self, mock_get_data):
        self.assertEqual(Model.objects.all().count(), 4)
        mock_get_data.return_value = self.fake_response()
        self.tab_facebook_task.apply()
        self.assertEqual(Model.objects.all().count(), 5)

    @patch("apps.sp.tasks.facebook.TabFacebookTask.get_data")
    def test_method_get_data(self, mock_get_data):
        mock_get_data.return_value = self.fake_response()
        self.assertEqual(Model.objects.all().count(), 4)
        result = self.tab_facebook_task.run()
        self.assertEqual(Model.objects.all().count(), 5)
        self.assertEquals(result.get('status'), 200)

    def _test_method_test_real(self):
        self.assertEqual(Model.objects.all().count(), 4)
        result = self.tab_facebook_task.run()
        self.assertEqual(Model.objects.all().count(), 5)
        self.assertEquals(result.get('status'), 200)