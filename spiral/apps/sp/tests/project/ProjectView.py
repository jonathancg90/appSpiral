from django.test import TestCase
import json
from json import dumps
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from apps.sp.tests.Helpers.InsertDataHelper import InsertDataHelper
from apps.sp.models.Project import Project
from apps.sp.models.Casting import Casting
from apps.sp.models.Client import Client
from apps.sp.models.Commercial import Commercial
from apps.sp.views.panel.Project import ProjectListView, ProjectSaveJsonView, ProjectUpdateJsonView


class ProjectViewTest(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.insert_data_helper = InsertDataHelper()
        self.insert_test_data()

    def insert_test_data(self):
        self.insert_data_helper.run()
        self.user = User.objects.get(is_superuser=True)

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

    def test_basic_data(self):
        """
        Tests data test insert correct
        """
        self.assertTrue(Commercial.objects.all().count() > 0)
        self.assertTrue(Client.objects.all().count() > 0)

    def _test_list_view_project(self):
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
        self.assertEqual(response.context_data['object_list'].count(), 4)

        self.insert_project()
        response = view(request)
        self.assertEqual(response.context_data['object_list'].count(), 5)

    def _test_list_view_project_filter_casting(self):
        """
        Tests data: Filter
        """
        request = self.request_factory.get(reverse('project_list'),
                                           data={'line_productions': Project.LINE_CASTING})
        request.user = self.user
        view = ProjectListView.as_view()
        response = view(request)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context_data['project_list']), 4)

    def _test_list_view_project_filter_photo(self):
        """
        Tests data: Filter
        """
        self.insert_project()
        request = self.request_factory.get(reverse('project_list'),
                                           data={'line_productions': Project.LINE_PHOTO})
        request.user = self.user
        view = ProjectListView.as_view()
        response = view(request)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context_data['project_list']), 1)

    def _test_list_view_project_filter_range_dates(self):
        """
        Tests data: Filter
        """
        self.insert_project()
        request = self.request_factory.get(reverse('project_list'),
                                           data={'start_date__gte': '01/07/2014',
                                                 'finish_date__lte': '02/07/2014'})
        request.user = self.user
        view = ProjectListView.as_view()
        response = view(request)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context_data['project_list']), 1)

    def _test_minimal_create_project(self):
        self.assertEqual(Project.objects.all().count(), 4)
        url = reverse('project_save')

        commercial = Commercial.objects.get(pk=1)

        data = {
            'duty': {},
            'models': [],
            'commercial': {
                'dates': [
                    {
                        'date': '15/08/2014',
                        'id': 107
                    },
                    {
                        'date': '06/08/2014',
                        'id': 108
                    }
                ],
                'id': commercial.id,
                'name': 'new commercial'
            },
            'deliveries': [],
            'project':
                {
                    'start_productions': '07/08/2014',
                    'line_productions': 1,
                    'commercial': commercial.id,
                    'end_productions': '04/08/2014'
                },
            'client': {},
            'line': {},
            'payment': {
                'conditions': []
            },
            'resources': []
        }


        view = ProjectSaveJsonView.as_view()
        request = self.request_factory.post(
            url, data=dumps(data), content_type='application/json'
        )
        request.user = self.user
        response = view(request)
        content = json.loads(response._container[0])
        self.assertEqual(content.get('status'), 'success')
        self.assertEqual(Project.objects.all().count(), 5)

    def _test_full_create_project(self):
        self.assertEqual(Project.objects.all().count(), 4)
        url = reverse('project_save')

        commercial = Commercial.objects.get(pk=1)
        client_director = Client.objects.get(pk=3)
        client_agency = Client.objects.get(pk=2)
        client_productor = Client.objects.get(pk=1)

        data = {
            'duty': {
                'duration_month': 3,
                'broadcasts': [
                    {
                        'id': 2,
                        'name': 'Web'
                    },
                    {
                        'id': 4,
                        'name': 'Cable'
                    }
                ],
                'type_contract': {
                    'id': 1,
                    'name':'Uso de imagen'
                }, 'countries': [
                    {
                        'nationality': 'Peruana',
                        'cities': [],
                        'id': 1,
                        'name': u'Per\xfa'
                    },
                    {
                        'nationality': 'Ucraniano',
                        'cities': [],
                        'id': 6,
                        'name': 'Ucrania'
                    },
                    {
                        'nationality': 'Argentino',
                        'cities': [],
                        'id': 7,
                        'name':'Argentina'
                    }
                ]
            },
            'models': [
                {
                    'profile': 'perfil',
                    'scene': '1',
                    'character': {'id': 1, 'name': 'Principal'},
                    'feature': 'carracteristicas',
                    'budget': '100',
                    'cant': 2,
                    'type': [
                        {'id': 1, 'name': 'Especifico'},
                        {'id': 2, 'name': 'Archivo'}
                    ]
                },
                {
                    'profile': 'perfil test',
                    'scene': '1',
                    'character': {'id': 0, 'name': 'Secundario'},
                    'feature': 'features',
                    'budget': '200',
                    'cant': 3,
                    'type': [
                        {'id': 2, 'name': 'Archivo'}
                    ]
                }
            ],
            'commercial': {
                'dates': [
                    {'date': '15/08/2014'},
                    {'date': '06/08/2014'}
                ], 'name': 'new commercial',
                'id': commercial.id
            },
            'deliveries': [
                {'date': '01/08/2014'},
                {'date': '02/08/2014'},
                {'date': '12/08/2014'}
            ],
            'project':
                {
                    'end_productions': '07/08/2014',
                    'budget_cost': '800',
                    'line_productions': 1,
                    'commercial': commercial.id,
                    'budget': '1000',
                    'currency': 2,
                    'observations':'Mis observaciones',
                    'start_productions': '01/08/2014'
                },
            'client': {
                'director': client_director.id,
                'agency': client_agency.id,
                'productor': client_productor.id
            },
            'line': {},
            'payment':
                {
                    'client': client_director.id,
                    'conditions': ['condicion1', 'condicion2']
                },
            'resources': []
        }


        view = ProjectSaveJsonView.as_view()
        request = self.request_factory.post(
            url, data=dumps(data), content_type='application/json'
        )
        request.user = self.user
        response = view(request)
        content = json.loads(response._container[0])
        self.assertEqual(content.get('status'), 'success')
        self.assertEqual(Project.objects.all().count(), 5)

    def _test_save_duty_none(self):
        self.assertEqual(Project.objects.all().count(), 4)
        url = reverse('project_save')

        commercial = Commercial.objects.get(pk=1)
        client_director = Client.objects.get(pk=3)
        client_agency = Client.objects.get(pk=2)
        client_productor = Client.objects.get(pk=1)

        data = {
            'duty': {},
            'models': [
                {
                    'profile': 'perfil',
                    'scene': '1',
                    'character': {'id': 1, 'name': 'Principal'},
                    'feature': 'carracteristicas',
                    'budget': '100',
                    'cant': 2,
                    'type': [
                        {'id': 1, 'name': 'Especifico'},
                        {'id': 2, 'name': 'Archivo'}
                    ]
                },
                {
                    'profile': 'perfil test',
                    'scene': '1',
                    'character': {'id': 0, 'name': 'Secundario'},
                    'feature': 'features',
                    'budget': '200',
                    'cant': 3,
                    'type': [
                        {'id': 2, 'name': 'Archivo'}
                    ]
                }
            ],
            'commercial': {
                'dates': [
                    {'date': '15/08/2014'},
                    {'date': '06/08/2014'}
                ], 'name': 'new commercial',
                'id': commercial.id
            },
            'deliveries': [
                {'date': '01/08/2014'},
                {'date': '02/08/2014'},
                {'date': '12/08/2014'}
            ],
            'project':
                {
                    'end_productions': '07/08/2014',
                    'budget_cost': '800',
                    'line_productions': 1,
                    'commercial': commercial.id,
                    'budget': '1000',
                    'currency': 2,
                    'observations':'Mis observaciones',
                    'start_productions': '01/08/2014'
                },
            'client': {
                'director': client_director.id,
                'agency': client_agency.id,
                'productor': client_productor.id
            },
            'line': {},
            'payment':
                {
                    'client': client_director.id,
                    'conditions': ['condicion1', 'condicion2']
                },
            'resources': []
        }


        view = ProjectSaveJsonView.as_view()
        request = self.request_factory.post(
            url, data=dumps(data), content_type='application/json'
        )
        request.user = self.user
        response = view(request)
        content = json.loads(response._container[0])
        self.assertEqual(content.get('status'), 'success')
        self.assertEqual(Project.objects.all().count(), 5)

    def test_update_project(self):
        self.assertEqual(Project.objects.all().count(), 4)
        url = reverse('project_update')
        project = self.insert_project()
        casting = Casting()
        casting.project = project
        casting.save()
        self.assertEqual(Project.objects.all().count(), 5)

        commercial = Commercial.objects.get(pk=1)
        client_director = Client.objects.get(pk=3)
        client_agency = Client.objects.get(pk=2)
        client_productor = Client.objects.get(pk=1)

        data = {
            'duty': {},
            'models': [
                {
                    'profile': 'perfil',
                    'scene': '1',
                    'character': {'id': 1, 'name': 'Principal'},
                    'feature': 'carracteristicas',
                    'budget': '100',
                    'cant': 2,
                    'type': [
                        {'id': 1, 'name': 'Especifico'},
                        {'id': 2, 'name': 'Archivo'}
                    ]
                },
                {
                    'profile': 'perfil test',
                    'scene': '1',
                    'character': {'id': 0, 'name': 'Secundario'},
                    'feature': 'features',
                    'budget': '200',
                    'cant': 3,
                    'type': [
                        {'id': 2, 'name': 'Archivo'}
                    ]
                }
            ],
            'commercial': {
                'dates': [
                    {'date': '15/08/2014'},
                    {'date': '06/08/2014'}
                ], 'name': 'new commercial',
                'id': commercial.id
            },
            'deliveries': [
                {'date': '01/08/2014'},
                {'date': '02/08/2014'},
                {'date': '12/08/2014'}
            ],
            'project':
                {
                    'end_productions': '07/08/2014',
                    'budget_cost': '800',
                    'line_productions': 1,
                    'commercial': commercial.id,
                    'budget': '1000',
                    'currency': 2,
                    'observations':'Mis observaciones',
                    'start_productions': '01/08/2014'
                },
            'client': {
                'director': client_director.id,
                'agency': client_agency.id,
                'productor': client_productor.id
            },
            'line': {},
            'project_id': project.id,
            'payment':
                {
                    'client': client_director.id,
                    'conditions': ['condicion1', 'condicion2']
                },
            'resources': []
        }


        view = ProjectUpdateJsonView.as_view()
        request = self.request_factory.post(
            url, data=dumps(data), content_type='application/json'
        )
        request.user = self.user
        response = view(request)
        content = json.loads(response._container[0])
        self.assertEqual(content.get('status'), 'success')
        self.assertEqual(Project.objects.all().count(), 5)