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
                "id_adulto": "231",
                "nom_datos": "valeria",
                "app_datos": "ahon",
                "apm_datos": "bustillos",
                "naci_datos": "177",
                "sexo": "F",
                "fec_datos": "1994-01-12",
                "tipdoc_datos": "DNI",
                "num_doc_datos": "71434079",
                "pais_datos": "177",
                "dep_datos": "lima",
                "dir_datos": "pasaje octavio bernal 120 / g",
                "fijo_datos": "6029681",
                "movil_datos": "993575082",
                "mail_datos": "valeruz_12@hotmail.com",
                "fb_datos": "https://www.facebook.com/valeruzhi",
                "yt_datos": "http://m.youtube.com/channel_switcher",
                "ocu_datos": "Estudiante",
                "tip_cab": "Ondulado",
                "larg_cab": "Mediano",
                "color_ojos": "Negro",
                "estatura": "1,60",
                "fot1": "231.jpg",
                "fot2": "231-231.jpg",
                "cam_blu": "M",
                "pant": "30",
                "shoes": "38",
                "hobbie": "Me gusta la actuación, escuch",
                "terminos": "aceptar",
                "status": "0",
                "pais": "Perú",
                "naci": "Perú"
            }
        ]

<<<<<<< HEAD
    # @patch("apps.sp.tasks.facebook.TabFacebookTask.get_data")
    # def test_task_save_model(self, mock_get_data):
    #     self.assertEqual(Model.objects.all().count(), 4)
    #     mock_get_data.return_value = self.fake_response()
    #     self.tab_facebook_task.apply()
    #     self.assertEqual(Model.objects.all().count(), 5)
    #
    # @patch("apps.sp.tasks.facebook.TabFacebookTask.get_data")
    # def test_method_get_data(self, mock_get_data):
    #     mock_get_data.return_value = self.fake_response()
    #     self.assertEqual(Model.objects.all().count(), 4)
    #     result = self.tab_facebook_task.run()
    #     self.assertEqual(Model.objects.all().count(), 5)
    #     self.assertEquals(result.get('status'), 200)
=======
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
>>>>>>> f3f688468a37b6a901f63a2ac97f52df7d04f4d6

<<<<<<< HEAD
<<<<<<< HEAD
    def test_method_test_real(self):
        self.assertEqual(Model.objects.all().count(), 4)
        result = self.tab_facebook_task.run()
<<<<<<< HEAD
        self.assertEqual(Model.objects.all().count(), 59)
=======
        self.assertEqual(Model.objects.all().count(), 5)
>>>>>>> f3f688468a37b6a901f63a2ac97f52df7d04f4d6
        self.assertEquals(result.get('status'), 200)
=======
    # def _test_method_test_real(self):
    #     self.assertEqual(Model.objects.all().count(), 4)
    #     result = self.tab_facebook_task.run()
    #     self.assertEqual(Model.objects.all().count(), 5)
    #     self.assertEquals(result.get('status'), 200)
>>>>>>> 5efb30166a87765b30ff5a79eb8125ceb315009e
=======
    def _test_method_test_real(self):
        self.assertEqual(Model.objects.all().count(), 4)
        result = self.tab_facebook_task.run()
        self.assertEqual(Model.objects.all().count(), 5)
        self.assertEquals(result.get('status'), 200)
>>>>>>> 0073a1a753ca1f4ec5756734d890539f18a18bc0
