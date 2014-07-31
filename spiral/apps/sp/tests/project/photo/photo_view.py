import json

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory
from django.contrib.auth.models import User

from apps.sp.models.Project import Project
from apps.sp.models.PhotoCasting import PhotoCastingDetailModel, PhotoCasting, UsePhotos, TypePhotoCasting
from apps.sp.models.Commercial import Commercial
from apps.sp.models.Currency import Currency
from apps.sp.tests.Helpers.InsertDataHelper import InsertDataHelper
from apps.sp.views.panel.PhotoCasting import TypePhotoCastingDataList, UsePhotoDataList, PhotoCastingSaveProcess


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
        self.assertEqual(len( content.get('types')), 2)

    def _test_save_casting_method(self):
        self.assertEqual(len(PhotoCasting.objects.all()), 0)
        extra_save_process = ExtraSaveProcess()
        project = self.insert_project()
        extra_save_process.extras = extra_save_process.get_extras()
        extra_save_process.data_line = {
        }

        extra_save_process.data_models = [
        ]

        extra = extra_save_process.save_extra(project)
        extra_save_process.save_detail_model_extra(extra)

        self.assertEqual(len(PhotoCasting.objects.all()), 1)
        self.assertEqual(len(PhotoCastingDetailModel.objects.filter(extras=extra)), 2)