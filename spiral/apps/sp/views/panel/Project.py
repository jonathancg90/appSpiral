# -*- coding: utf-8 -*-
import json
import calendar

from django.conf import settings
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView
from datetime import datetime

from apps.common.view import LoginRequiredMixin, PermissionRequiredMixin
from apps.common.view import JSONResponseMixin
from apps.common.view import SearchFormMixin
from apps.sp.models.Commercial import Commercial, CommercialDateDetail
from apps.sp.models.Currency import Currency
from apps.sp.models.Client import Client, TypeClient
from apps.sp.models.Payment import Payment
from apps.sp.views.panel.Casting import CastingSaveProcess
from apps.sp.views.panel.Extra import ExtraSaveProcess
from apps.sp.views.panel.Representation import RepresentationSaveProcess
from apps.sp.views.panel.PhotoCasting import PhotoCastingSaveProcess
from apps.sp.models.Project import Project, ProjectDetailStaff, ProjectClientDetail, \
    ProjectDetailDeliveries
from apps.sp.forms.Project import ProjectFiltersForm
from django.views.generic import View
from apps.sp.models.Casting import Casting
from apps.sp.models.Extras import Extras
from apps.sp.models.PhotoCasting import PhotoCasting
from apps.sp.models.Representation import Representation


class ProjectListView(LoginRequiredMixin, PermissionRequiredMixin,
                      SearchFormMixin, ListView):
    template_name = 'panel/project/list.html'
    model = Project
    search_form_class = ProjectFiltersForm
    paginate_by = settings.PANEL_PAGE_SIZE
    filtering = {
        'start_date_date': ['gte'],
        'finish_date_date': ['lte'],
        'line_productions': SearchFormMixin.ALL
    }

    def _build_filters(self, filters=None):
        bf = super(ProjectListView, self).build_filters(filters=filters)
        column_name = 'start_productions__exact'
        input_formats = '%d/%m/%Y'
        ini = 'initial_date'
        end = 'end_date'
        ini_sufix = self.LOOKUP_SEP + 'gte'
        end_sufix = self.LOOKUP_SEP + 'lte'
        if bf.get(column_name) is not None:
            column = bf.pop(column_name)
            if bf.get(ini + ini_sufix) is not None:
                bf[column + ini_sufix] = datetime.strptime(
                    bf.pop(ini + ini_sufix), input_formats)
            if bf.get(end + end_sufix) is not None:
                bf[column + end_sufix] = datetime.strptime(
                    bf.pop(end + end_sufix), input_formats)
        return bf


class ProjectCreateView(LoginRequiredMixin, PermissionRequiredMixin,
                  TemplateView):
    model = Project
    template_name = 'panel/project/crud.html'

    def get_project(self):
        try:
            project_id = self.kwargs.get('pk')
            project = Project.objects.get(pk=project_id)
            return project
        except:
            return None

    def get_context_data(self, **kwargs):
        context = super(ProjectCreateView, self).get_context_data(**kwargs)
        project = self.get_project()
        if project is not None:
            context['code'] = project.get_code()
            context['id'] = project.id
        return context


class ProjectRolesJsonView(LoginRequiredMixin, PermissionRequiredMixin,
                      JSONResponseMixin, View):
    model = ProjectDetailStaff

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(ProjectRolesJsonView, self).dispatch(request, *args, **kwargs)

    def get_staff_roles(self):
        data = []
        roles = ProjectDetailStaff.CHOICE_ROLES
        for role in roles:
            data.append({
                'id':role[0],
                'name': role[1]
            })
        return data

    def get(self, request, *args, **kwargs):
        context = {}
        context['roles'] = self.get_staff_roles()
        return self.render_to_response(context)


class ProjectSaveJsonView(LoginRequiredMixin, PermissionRequiredMixin,
                           JSONResponseMixin, CastingSaveProcess,
                           ExtraSaveProcess, RepresentationSaveProcess,
                           PhotoCastingSaveProcess, View):

    model = ProjectDetailStaff
    MESSAGE_ERROR_SAVE = 'Ha ocurrido un error al tratar de registrar el proyecto'
    MESSAGE_ERROR_COMMERCIAL = 'El comercial ingresado ya se encuentra registrado en otro proyecto'
    MESSAGE_SUCCESS = 'Projecto registrado correctamente'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(ProjectSaveJsonView, self).dispatch(request, *args, **kwargs)

    @transaction.commit_manually
    def save_process(self):
        try:
            validate, msg = self.process_validate()
            if validate:
                project = self.save_project()
                self.save_line(project)
                self.save_commercial_dates(project)
                self.save_resources(project)
                self.save_payment(project)
                transaction.commit()
                return project, self.MESSAGE_SUCCESS
            else:
                transaction.rollback()
                return None, msg
        except Exception, e:
            transaction.rollback()
            return None, self.MESSAGE_ERROR_SAVE

    def process_validate(self):
        commercial = Commercial.objects.get(pk=self.data_project.get('commercial'))
        if Project.objects.filter(
                commercial=commercial,
                line_productions=self.data_project.get('line_productions')
        ).exists():
            return False, self.MESSAGE_ERROR_COMMERCIAL

        return True, None

    def save_commercial_dates(self, project):
        commercial = project.commercial
        new = CommercialDateDetail.objects.filter(commercial=commercial).exists()
        if new:
            CommercialDateDetail.objects.filter(commercial=commercial).delete()

        for _commercial in self.data_commercial.get('dates'):
            commercial_detail = CommercialDateDetail()
            commercial_detail.commercial = commercial
            commercial_detail.date = self.format_date(_commercial.get('date'))
            commercial_detail.save()

    def save_resources(self, project):
        for resources in self.data_resources:
            project_detail_staff = ProjectDetailStaff()
            project_detail_staff.project = project
            project_detail_staff.role = resources.get('role').get('id')
            project_detail_staff.employee = resources.get('employee').get('id_emp')
            project_detail_staff.budget = resources.get('budget')
            project_detail_staff.percentage = resources.get('percentage')
            project_detail_staff.save()

    def save_payment(self, project):
        client_id = self.data_payment.get('client')

        payment = Payment()
        payment.client = Client.objects.get(pk=client_id) if client_id is not None else None
        payment.conditions = json.dumps(self.data_payment.get('conditions'))
        payment.project = project
        payment.save()

    def save_line(self, project):
        project_line = None
        if project.line_productions == Project.LINE_CASTING:
            project_line = self.save_casting(project)
            self.save_detail_model_casting(project_line)
        if project.line_productions == Project.LINE_EXTRA:
            project_line = self.save_extra(project)
            self.save_detail_model_extra(project_line)
        if project.line_productions == Project.LINE_PHOTO:
            project_line = self.save_photo(project)
            self.save_detail_model_photo(project_line)
        if project.line_productions == Project.LINE_REPRESENTATION:
            project_line = self.save_representation(project)
            self.save_detail_model_representation(project_line)
        return project_line

    def save_project(self):
        project = Project()
        project.code = self.generate_code()
        project.commercial = Commercial.objects.get(pk=self.data_project.get('commercial'))
        project.end_productions = self.format_date(self.data_project.get('end_productions'))
        project.start_productions = self.format_date(self.data_project.get('start_productions'))
        project.budget = self.data_project.get('budget') if self.data_project.get('budget') is not None else 0
        project.currency = Currency.objects.get(pk=self.data_project.get('currency')) if self.data_project.get('currency') is not None else None
        project.budget_cost = self.data_project.get('budget_cost') if self.data_project.get('budget_cost') is not None else 0
        project.observations = self.data_project.get('observations')
        project.line_productions = self.data_project.get('line_productions')
        project.save()
        self.save_clients(project)
        self.save_delivery_dates(project)
        return project

    def format_date(self, date):
        if date is not None:
            date = datetime.strptime(date, "%d/%m/%Y")
            return "%s-%s-%s" % (date.year, date.month, date.day)
        return date

    def generate_code(self):
        date = datetime.strptime(self.data_project.get('start_productions'), "%d/%m/%Y")
        dateMonthStart = "%s-%s-01" % (date.year, date.month)
        dateMonthEnd = "%s-%s-%s" % (date.year, date.month, calendar.monthrange(date.year-1, date.month-1)[1])
        project = Project.objects.filter(
            start_productions__gte=dateMonthStart,
            start_productions__lte=dateMonthEnd
        ).order_by('-code')
        if len(project) > 0:
            code = project[0].code + 1
        else:
            return 1
        return code

    def save_delivery_dates(self, project):
        for delivery in self.data_deliveries:
            project_delivery = ProjectDetailDeliveries()
            project_delivery.project = project
            project_delivery.delivery_date = self.format_date(delivery.get('date'))
            project_delivery.save()

    def save_clients(self, project):
        type_director = TypeClient.objects.get(name='Realizadora')
        type_agency = TypeClient.objects.get(name='Agencia')
        type_productor = TypeClient.objects.get(name='Productora')

        id_director = self.data_client.get('director', None)
        id_agency = self.data_client.get('agency', None)
        id_productor = self.data_client.get('productor', None)

        if id_director is not None:
            client_detail = ProjectClientDetail(
                project=project,
                client=Client.objects.get(pk=id_director),
                type=type_director
            )
            client_detail.save()

        if id_agency is not None:
            client_detail = ProjectClientDetail(
                project=project,
                client=Client.objects.get(pk=id_agency),
                type=type_agency
            )
            client_detail.save()

        if id_productor is not None:
            client_detail = ProjectClientDetail(
                project=project,
                client=Client.objects.get(pk=id_productor),
                type=type_productor
            )
            client_detail.save()

    def set_attributes(self, data):
        self.data_project = data.get('project')
        self.data_line = data.get('line')
        self.data_client = data.get('client')
        self.data_commercial = data.get('commercial')
        self.data_deliveries = data.get('deliveries')
        self.data_models = data.get('models')
        self.data_resources = data.get('resources')
        self.data_payment = data.get('payment')

    def post(self, request, *args, **kwargs):
        context = {}
        data = json.loads(request.body)
        self.set_attributes(data)
        project, msg = self.save_process()
        context['status'] = 'success'
        context['message'] = msg
        if project is None:
            context['status'] = 'warning'
        else:
            project = Project.objects.get(pk=project.id)
            context['result'] = {
                'code': project.get_code(),
                'id': project.id
            }
        return self.render_to_response(context)


class ProjectUpdateJsonView(ProjectSaveJsonView):
    pass


class ProjectDataUpdateJsonView(LoginRequiredMixin, PermissionRequiredMixin,
                                JSONResponseMixin, View):

    model = Project
    PRODUCTOR = 'Productora'
    AGENCY = 'Agencia'
    DIRECTOR = 'Realizadora'

    def get_step(self):
        self.step_permissions = []
        for permission in self.permissions:
            result = self.user.has_perm(permission.get('permission'))
            if result:
                self.step_permissions.append(permission.get('step'))
        self.step_permissions.sort()
        return self.step_permissions

    def get_deliveries(self):
        data=[]
        detail_deliveries = ProjectDetailDeliveries.objects.filter(project=self.project)
        for delivery in detail_deliveries:
            data.append({
                'date': delivery.delivery_date.strftime("%d/%m/%Y"),
            })
        return data

    def get_detail_model(self):
        data = []
        if self.line.get('id') == Project.LINE_EXTRA:
            details = self.line_project.extras_detail_model_set.all()
            for detail in details:
                data.append({
                    'cant': detail.quantity,
                    'profile': detail.profile,
                    'feature': detail.feature,
                    'character': {
                        'id': detail.character,
                        'name': detail.get_character_display()
                    },
                    'currency': {
                        'symbol': detail.currency.symbol,
                        'id': detail.currency.id
                    },
                    'budget_cost': detail.budget_cost,
                    'schedule': detail.schedule
                })

        if self.line.get('id') == Project.LINE_CASTING:
            details = self.line_project.casting_detail_model_set.all()
            for detail in details:
                data.append({
                    'cant': detail.quantity,
                    'profile': detail.profile,
                    'feature': detail.feature,
                    'character': {
                        'id': detail.character,
                        'name': detail.get_character_display()
                    },
                    'type': self.get_types(detail.type_casting.all()),
                    'scene': detail.scene,
                    'budget': detail.budget
                })

        if self.line.get('id') == Project.LINE_PHOTO:
            details = self.line_project.photo_casting_detail_model_set.all()
            for detail in details:
                data.append({
                    'cant': detail.quantity,
                    'profile': detail.profile,
                    'feature': detail.feature,
                    'character': {
                        'id': detail.character,
                        'name': detail.get_character_display()
                    },
                    'currency': {
                        'symbol': detail.currency.symbol,
                        'id': detail.currency.id
                    },
                    'budget_cost': detail.budget_cost
                })

        if self.line.get('id') == Project.LINE_REPRESENTATION:
            details = self.line_project.representation_detail_model_set.all()
            for detail in details:
                data.append({
                    'profile': detail.profile,
                    'model_name': detail.model.name_complete,
                    'model': {
                        'document': detail.model.get_type_document_display() + + detail.model.number_doc,
                        'id': detail.model.id,
                        'name': detail.model.name_complete,
                    },
                    'character': {
                        'id': detail.character,
                        'name': detail.get_character_display()
                    },
                    'observations': detail.observations
                })
        return data

    def get_types(self, types):
        data = []
        for type in types:
            data.append({
                'id': type.id,
                'name': type.name
            })
        return data


    def get_conditions(self):
        try:
            payment = Payment.objects.get(project=self.project)
            return json.loads(payment.conditions)
        except:
            return {}

    def get_detail_staff(self):
        data = []
        try:
            detail_staff = ProjectDetailStaff.objects.filter(project=self.project)
            for staff in detail_staff:
                data.append({
                    'role': {
                        'id':  staff.role,
                        'name':  staff.get_role_display()
                    },
                    'employee': {
                        'id': staff.employee,
                    },
                    'percentage': int(staff.percentage),
                    'budget': float(staff.budget),
                    'total': float((staff.budget * staff.percentage)/100)
                })
        except:
            return data
        return data

    def get_payment(self):
        try:
            payment = Payment.objects.get(project=self.project)
            return {
                'client': {
                    'type': self.get_types(payment.client.type_client.all()),
                    'id': payment.client.id,
                    'name': payment.client.name
                },
                'currency': {
                    'symbol': self.project.currency.symbol,
                    'id': self.project.currency.id
                }
            }
        except:
            return {}

    def get_commercial(self):
        commercial = self.project.commercial
        date_detail = CommercialDateDetail.objects.filter(commercial=commercial)
        dates = []
        for detail in date_detail:
            dates.append({
                'id': detail.id,
                'date': detail.date.strftime("%d/%m/%Y")
            })
        data = {
            'id': commercial.id,
            'name': commercial.name,
            'dates': dates
        }

        return data

    def get_client(self, type):
        try:
            type_client = TypeClient.objects.get(name=type)
            client_detail = ProjectClientDetail.objects.get(type=type_client, project=self.project)
            return {
                'id': client_detail.client.id,
                'name': client_detail.client.name,
                'type': self.get_types(client_detail.client.type_client.all())
            }
        except Exception, e:
            return {}

    def get_data_project(self):

        project = {
            "permission_steps": self.get_step(),
            "step": 1,
            "line":  self.line,
            "deliveries": self.get_deliveries(),
            "detailModel": self.get_detail_model(),
            "conditions":  self.get_conditions(),
            "productor": self.get_client(self.PRODUCTOR),
            "agency": self.get_client(self.AGENCY),
            "director": self.get_client(self.DIRECTOR),
            "detailStaff": self.get_detail_staff(),
            "payment": self.get_payment(),
            "commercial":  self.get_commercial(),
            "startProduction":  self.project.start_productions.strftime("%d/%m/%Y"),
            "finishProduction": self.project.end_productions.strftime("%d/%m/%Y"),
            "observation": self.project.observations
        }

        if self.line.get('id') == Project.LINE_CASTING:
            project.update({
                "typeCasting": self.get_types(self.line_project.type_casting.all()),
                "ppi": self.line_project.ppi.strftime("%d/%m/%Y") if self.line_project.ppi is not None else [],
                "ppg": self.line_project.ppg.strftime("%d/%m/%Y") if self.line_project.ppg is not None else [],
                "internalBudget": float(self.project.budget),
                "budget": float(self.project.budget_cost)
            })
        return project

    def get_permissions(self):
        permissions = [
            {
                'step':1,
                'permission': 'change_project'
            },
            {
                'step':3,
                'permission': 'change_payment'
            },
            {
                'step':4,
                'permission': 'change_projectdetailstaff'
            }
        ]
        if self.line.get('id') == Project.LINE_EXTRA:
            permissions.append({
                'step': 2,
                'permission': 'change_extrasdetailmodel'
            })
            self.line_project = Extras.objects.get(project=self.project)
        if self.line.get('id') == Project.LINE_CASTING:
            permissions.append({
                'step': 2,
                'permission': 'change_castingdetailmodel'
            })
            self.line_project = Casting.objects.get(project=self.project)
        if self.line.get('id') == Project.LINE_PHOTO:
            permissions.append({
                'step': 2,
                'permission': 'change_photocastingdetailmodel'
            })
            self.line_project = PhotoCasting.objects.get(project=self.project)
        if self.line.get('id') == Project.LINE_REPRESENTATION:
            permissions.append({
                'step': 2,
                'permission': 'change_representationdetailmodel'
            })
            self.line_project = Representation.objects.get(project=self.project)
        return permissions

    def set_attributes(self):
        self.user = self.request.user
        self.project = Project.objects.get(pk=self.kwargs.get('pk'))
        self.line = {
            'id': self.project.line_productions,
            'name': self.project.get_line_productions_display()
        }
        self.permissions = self.get_permissions()

    def get(self, request, *args, **kwargs):
        context = {}
        self.set_attributes()
        context['result'] = self.get_data_project()
        return self.render_to_response(context)


class ProjectLinesJsonView(LoginRequiredMixin, PermissionRequiredMixin,
                           JSONResponseMixin, View):

    model = Project

    def get_lines(self):
        data = []
        lines = Project.CHOICE_LINE
        for line in lines:
            data.append({
                'id': line[0],
                'name': line[1]
            })
        return data

    def get(self, request, *args, **kwargs):
        context = {}
        context['lines'] = self.get_lines()
        return self.render_to_response(context)