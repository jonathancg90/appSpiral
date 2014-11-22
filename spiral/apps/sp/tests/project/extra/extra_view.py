import json

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory
from django.contrib.auth.models import User

from apps.sp.models.Project import Project
from apps.sp.models.Extras import Extras, ExtrasDetailModel
from apps.sp.models.Commercial import Commercial
from apps.sp.models.Currency import Currency
from apps.sp.tests.Helpers.InsertDataHelper import InsertDataHelper
from apps.sp.views.panel.Extra import ExtraCharacterDataList, ExtraSaveProcess


class ExtraViewTest(TestCase):

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
        self.assertTrue(len(Currency.objects.all()) > 0)

    def insert_test_data(self):
        self.insert_data_helper.run()
        self.user = User.objects.get(is_superuser=True)

    def test_character_data_list(self):
        """
        Tests List
        """
        view = ExtraCharacterDataList.as_view()
        request = self.request_factory.get(
            reverse('extra_data_character')
        )
        request.user = self.user
        response = view(request)
        self.assertEqual(response.status_code, 200)
        content = json.loads(response._container[0])
        self.assertEqual(len( content.get('character')), 2)

    def test_save_casting_method(self):
        self.assertEqual(len(Extras.objects.all()), 0)
        extra_save_process = ExtraSaveProcess()
        project = self.insert_project()
        extra_save_process.extras = extra_save_process.get_extras()
        extra_save_process.data_line = {
        }

        extra_save_process.data_models = [
            {
                'profile': 'perfil',
                'budget_cost': '100',
                'schedule': '12:00',
                'character': {'id': 0, 'name': 'Extra especial'},
                'feature': 'carracteristicas',
                'currency': {
                    'symbol': '$',
                    'id': 2
                },
                'cant': 2
            },
            {
                'profile': 'perfil2',
                'budget_cost': '100',
                'schedule': '12:00',
                'character': {'id': 0, 'name': 'Extra especial'},
                'feature': 'test',
                'currency': {'symbol': '$', 'id': 2},
                'cant': 2
            }
        ]

        extra = extra_save_process.save_extra(project)
        extra_save_process.save_detail_model_extra(extra)

        self.assertEqual(len(Extras.objects.all()), 1)
        self.assertEqual(len(ExtrasDetailModel.objects.filter(extras=extra)), 2)