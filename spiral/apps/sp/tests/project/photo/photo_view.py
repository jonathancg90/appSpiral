import json

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory
from django.contrib.auth.models import User

from apps.sp.models.Project import Project
from apps.sp.models.PhotoCasting import PhotoCastingDetailModel, PhotoCasting, UsePhotos, TypePhotoCasting
from apps.sp.models.Commercial import Commercial
from apps.sp.tests.Helpers.InsertDataHelper import InsertDataHelper
from apps.sp.views.panel.PhotoCasting import TypePhotoCastingDataList, UsePhotoDataList, PhotoCastingSaveProcess


class PhotoCastingViewTest(TestCase):

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
        self.assertTrue(len(UsePhotos.objects.all()) > 0)
        self.assertTrue(len(TypePhotoCasting.objects.all()) > 0)

    def insert_test_data(self):
        self.insert_data_helper.run()
        self.user = User.objects.get(is_superuser=True)

    def test_type_casting_list(self):
        """
        Tests List
        """
        view = TypePhotoCastingDataList.as_view()
        request = self.request_factory.get(
            reverse('photo_casting_data_types')
        )
        request.user = self.user
        response = view(request)
        self.assertEqual(response.status_code, 200)
        content = json.loads(response._container[0])
        self.assertEqual(len( content.get('types')), 3)

    def test_use_photo_list(self):
        """
        Tests List
        """
        view = UsePhotoDataList.as_view()
        request = self.request_factory.get(
            reverse('photo_casting_use_photos')
        )
        request.user = self.user
        response = view(request)
        self.assertEqual(response.status_code, 200)
        content = json.loads(response._container[0])
        self.assertEqual(len( content.get('uses')), 10)

    def test_save_photo_casting_method(self):
        self.assertEqual(len(PhotoCasting.objects.all()), 0)
        photo_casting_save_process = PhotoCastingSaveProcess()
        project = self.insert_project()
        photo_casting_save_process.photo_casting = photo_casting_save_process.get_photo_casting()
        photo_casting_save_process.data_line = {
            'type_casting': 2,
            'uses': [
                {'id': 1, 'name': 'Todo Uso'},
                {'id': 2, 'name': 'Paneles'}
            ]
        }

        photo_casting_save_process.data_models = [
            {
                'profile': 'perfil',
                'budget_cost': '100',
                'character': {'id': 1, 'name': 'Principal'},
                'feature': 'carracteristicas',
                'currency': {'symbol': '$', 'id': 2},
                'cant': 2,
                'observations': 'observacio es'
            },
            {
                'profile': 'test',
                'budget_cost': '200',
                'character': {'id': 1, 'name': 'Principal'},
                'feature': 'features',
                'currency': {'symbol': '$', 'id': 2},
                'cant': 1
            }
        ]


        photo = photo_casting_save_process.save_photo(project)
        photo_casting_save_process.save_detail_model_photo(photo)

        self.assertEqual(len(PhotoCasting.objects.all()), 1)
        self.assertEqual(len(PhotoCastingDetailModel.objects.filter(photo_casting=photo)), 2)