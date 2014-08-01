import json

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory
from django.contrib.auth.models import User

from apps.sp.models.Project import Project
from apps.sp.models.Representation import Representation, RepresentationDetailModel, TypeEvent
from apps.sp.models.Model import Model
from apps.sp.models.Commercial import Commercial
from apps.sp.tests.Helpers.InsertDataHelper import InsertDataHelper
from apps.sp.views.panel.Representation import RepresentationEventsDataList, RepresentationCharacterDataList,\
    RepresentationSaveProcess


class RepresentationViewTest(TestCase):

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
        self.assertTrue(len(Model.objects.all()) > 0)

    def insert_test_data(self):
        self.insert_data_helper.run()
        self.user = User.objects.get(is_superuser=True)

    def test_event_list(self):
        """
        Tests List
        """
        view = RepresentationEventsDataList.as_view()
        request = self.request_factory.get(
            reverse('representation_data_event')
        )
        request.user = self.user
        response = view(request)
        self.assertEqual(response.status_code, 200)
        content = json.loads(response._container[0])
        self.assertEqual(len( content.get('events')), 4)

    def test_character_list(self):
        """
        Tests List
        """
        view = RepresentationCharacterDataList.as_view()
        request = self.request_factory.get(
            reverse('representation_data_character')
        )
        request.user = self.user
        response = view(request)
        self.assertEqual(response.status_code, 200)
        content = json.loads(response._container[0])
        self.assertEqual(len( content.get('character')), 5)

    def test_save_representation_method(self):
        self.assertEqual(len(Representation.objects.all()), 0)
        representation_save_process = RepresentationSaveProcess()
        project = self.insert_project()
        representation_save_process.representation = representation_save_process.get_representation()
        type_event = TypeEvent.objects.get(pk=2)

        representation_save_process.data_line = {
            'ppi': '2014-08-06',
            'ppg': '2014-08-21',
            'type_event': type_event.id
        }

        model_1 = Model.objects.get(pk=1)
        model_2 = Model.objects.get(pk=2)

        representation_save_process.data_models = [
            {
                'profile': 'perfil',
                'budget_cost': '1000',
                'character': {'id': 1, 'name': 'Extra'},
                'currency': {'symbol': '$', 'id': 2},
                'model': {'id': model_1.id},
                'model_name': 'jonathan carrasco'
            },
            {
                'profile': 'perfil2',
                'budget_cost': '200',
                'character': {'id': 1, 'name': 'Extra'},
                'currency': {'symbol': '$', 'id': 2},
                'model': {'id': model_2.id},
                'model_name': 'jonathan carrasco'
            }
        ]


        representation = representation_save_process.save_representation(project)
        representation_save_process.save_detail_model_representation(representation)

        self.assertEqual(len(Representation.objects.all()), 1)
        self.assertEqual(len(RepresentationDetailModel.objects.filter(representation=representation)), 2)