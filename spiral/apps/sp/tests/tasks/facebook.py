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
                "id_adulto": "5",
                "nom_datos": "Andrea Isabelle",
                "app_datos": "Cano",
                "apm_datos": "Valdez",
                "naci_datos": "Peruana",
                "sexo": "F",
                "fec_datos": "2001-02-06",
                "tipdoc_datos": "DNI",
                "num_doc_datos": "74293741",
                "pais_datos": "177",
                "dep_datos": "Lima",
                "dir_datos": "camino del inca 616",
                "fijo_datos": "2636888",
                "movil_datos": "956771855",
                "mail_datos": "natalie_v_r@hotmail.com",
                "fb_datos": "Andrea Cano",
                "yt_datos": "---",
                "ocu_datos": "Estudiante",
                "tip_cab": "Ondulado",
                "larg_cab": "Mediano",
                "color_ojos": "Avellana",
                "estatura": "",
                "fot1": "5.jpg",
                "fot2": "",
                "cam_blu": "",
                "pant": "0",
                "shoes": "",
                "hobbie": "",
                "terminos": "",
                "status": "0",
                "pais": "Perú"
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
