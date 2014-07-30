from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from apps.sp.tests.Helpers.InsertDataHelper import InsertDataHelper
from apps.sp.models.Project import Project
from apps.sp.models.Client import Client
from apps.sp.models.Commercial import Commercial
from apps.sp.views.panel.Project import ProjectListView


class ProjectViewTest(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.insert_data_helper = InsertDataHelper()
        self.insert_test_data()

    def insert_test_data(self):
        self.insert_data_helper.run()
        self.user = User.objects.get(is_superuser=True)

    def test_basic_data(self):
        """
        Tests data test insert correct
        """
        self.assertTrue(Commercial.objects.all().count() > 0)
        self.assertTrue(Client.objects.all().count() > 0)

    def insert_project(self):
        project = Project()
        project.line_productions = Project.LINE_CASTING
        project.code = '1'
        project.commercial = Commercial.objects.latest('created')
        project.version = '0'
        project.start_productions = '2014-08-12'
        project.end_productions = '2014-08-20'
        project.save()
        return project


    def test_list_view_project(self):
        """
        Tests data: List
        """
        view = ProjectListView.as_view()
        request = self.request_factory.get(
            reverse('project_list')
        )
        request.user = self.user
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['object_list'].count(), 0)

        self.insert_project()
        response = view(request)
        self.assertEqual(response.context_data['object_list'].count(), 1)

    def test_list_view_project_filter(self):
        """
        Tests data: Filter
        """
        request = self.request_factory.get(reverse('project_list'),
                                           data={'line_productions': Project.LINE_CASTING})
        request.user = self.user
        view = ProjectListView.as_view()
        response = view(request)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context_data['project_list']), 1)
