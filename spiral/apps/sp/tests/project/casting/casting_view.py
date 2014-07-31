import json

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory
from django.contrib.auth.models import User

from apps.sp.models.Project import Project
from apps.sp.models.Casting import Casting, CastingDetailModel, TypeCasting
from apps.sp.models.Commercial import Commercial
from apps.sp.tests.Helpers.InsertDataHelper import InsertDataHelper
from apps.sp.views.panel.Casting import CastingCharacterDataList, CastingSaveProcess


class CastingViewTest(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.insert_data_helper = InsertDataHelper()
        self.insert_test_data()

    def insert_project(self):
        project = Project()
        project.line_productions = Project.LINE_PHOTO
        project.code = '1'
        project.commercial = Commercial.objects.latest('created')
        project.version = '0'
        project.start_productions = '2014-08-1'
        project.end_productions = '2014-08-2'
        project.save()
        return project

    def test_data_required(self):
        self.assertTrue(len(TypeCasting.objects.all()) > 0)

    def insert_test_data(self):
        self.insert_data_helper.run()
        self.user = User.objects.get(is_superuser=True)

    def test_character_data_list(self):
        """
        Tests List
        """
        view = CastingCharacterDataList.as_view()
        request = self.request_factory.get(
            reverse('casting_data_character')
        )
        request.user = self.user
        response = view(request)
        self.assertEqual(response.status_code, 200)
        content = json.loads(response._container[0])
        self.assertEqual(len( content.get('character')), 2)

    def test_save_casting_method(self):
        self.assertEqual(len(Casting.objects.all()), 0)
        casting_save_process = CastingSaveProcess()
        project = self.insert_project()
        casting_save_process.casting = casting_save_process.get_casting()
        casting_save_process.data_line = {
            'ppi': '2014-07-01',
            'ppg': '2014-07-01',
            'type_casting': [
                {'id': 2, 'name': 'Archivo'},
                {'id': 3, 'name': 'Scouting'},
                {'id': 4, 'name': 'Callback'}
            ]
        }

        casting_save_process.data_models = [
            {
                'profile': 'perfil1',
                'scene': '1',
                'character':
                    {
                        'id': 0,
                        'name': 'Secundario'
                    },
                'feature': 'carracteristica 1',
                'budget': '100',
                'cant': 2,
                'type': [
                    {'id': 3, 'name': 'Scouting'},
                    {'id': 4, 'name': 'Callback'}
                ]
            },
            {
                'profile': 'perfil2',
                'scene': '',
                'character': {'id': 1, 'name': 'Principal'},
                'feature': 'test',
                'budget': '100',
                'cant': 2,
                'type': [
                    {'id': 3, 'name': 'Scouting'}
                ]
            }
        ]


        casting = casting_save_process.save_casting(project)
        casting_save_process.save_detail_model_casting(casting)

        self.assertEqual(len(Casting.objects.all()), 1)
        self.assertEqual(len(CastingDetailModel.objects.filter(casting=casting)), 2)