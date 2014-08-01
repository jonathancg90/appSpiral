# -*- coding: utf-8 -*-
import json
import calendar

from django.conf import settings
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView
from datetime import datetime
from django.views.generic import View

from apps.common.view import LoginRequiredMixin, PermissionRequiredMixin
from apps.common.view import JSONResponseMixin
from apps.common.view import SearchFormMixin
from apps.sp.models.Country import Country
from apps.sp.models.Commercial import Commercial, CommercialDateDetail
from apps.sp.models.Currency import Currency
from apps.sp.models.Client import Client, TypeClient
from apps.sp.models.Payment import Payment
from apps.sp.models.Broadcast import Broadcast
from apps.sp.views.panel.Casting import CastingSaveProcess
from apps.sp.views.panel.Extra import ExtraSaveProcess
from apps.sp.views.panel.Representation import RepresentationSaveProcess
from apps.sp.views.panel.PhotoCasting import PhotoCastingSaveProcess
from apps.sp.models.Project import Project, ProjectDetailStaff, ProjectClientDetail, \
    ProjectDetailDeliveries
from apps.sp.forms.Project import ProjectFiltersForm
from apps.sp.models.Project import DutyDetail
from apps.sp.models.Casting import Casting, CastingDetailModel
from apps.sp.models.Extras import Extras, ExtrasDetailModel
from apps.sp.models.PhotoCasting import PhotoCasting, PhotoCastingDetailModel
from apps.sp.models.Representation import Representation, RepresentationDetailModel


class ProjectListView(LoginRequiredMixin, PermissionRequiredMixin,
                      SearchFormMixin, ListView):
    template_name = 'panel/project/list.html'
    model = Project
    search_form_class = ProjectFiltersForm
    paginate_by = settings.PANEL_PAGE_SIZE
    filtering = {
        'start_date': ['gte'],
        'finish_date': ['lte'],
        'line_productions': SearchFormMixin.ALL
    }

    def build_filters(self, filters=None):
        bf = super(ProjectListView, self).build_filters(filters=filters)
        column_name = 'start_productions'
        input_formats = '%d/%m/%Y'
        ini = 'start_date'
        end = 'finish_date'
        ini_sufix = self.LOOKUP_SEP + 'gte'
        end_sufix = self.LOOKUP_SEP + 'lte'

        if bf.get(ini + ini_sufix) is not None:
            bf[column_name + ini_sufix] = datetime.strptime(
                bf.pop(ini + ini_sufix), input_formats)
        if bf.get(end + end_sufix) is not None:
            bf[column_name + end_sufix] = datetime.strptime(
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
    MESSAGE_ERROR_PROJECT = 'Ha ocurrido un error al validar el comercial seleccionado'
    MESSAGE_ERROR_COMMERCIAL = 'El comercial ingresado ya se encuentra registrado en otro proyecto'
    MESSAGE_ERROR_CLIENT = 'Se produjo un error al grabar los clientes'
    MESSAGE_ERROR_DELIVERY = 'Se produjo un error al grabar las fechas de entrega'
    MESSAGE_ERROR_DUTY = 'Se produjo un error al grabar los derechos'
    MESSAGE_SUCCESS = 'Projecto registrado correctamente'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(ProjectSaveJsonView, self).dispatch(request, *args, **kwargs)

    @transaction.commit_manually
    def save_process(self):
        try:
            validate, msg = self.process_validate()
            if validate:
                project, msg = self.save_project()
                if project is not None:
                    self.save_line(project)
                    self.save_commercial_dates(project)
                    self.save_resources(project)
                    self.save_payment(project)
                    transaction.commit()
                    return project, self.MESSAGE_SUCCESS
                else:
                    return None, self.MESSAGE_ERROR_SAVE
            else:
                transaction.rollback()
                return None, msg
        except Exception, e:
            transaction.rollback()
            return None, self.MESSAGE_ERROR_SAVE

    def process_validate(self):
        try:
            commercial = Commercial.objects.get(pk=self.data_project.get('commercial'))
        except:
            return False, self.MESSAGE_ERROR_PROJECT
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
            if _commercial.get('date') != '' and _commercial.get('date')  != None:
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

    def get_payment(self, **kwargs):
        return Payment()

    def save_payment(self, project):
        client_id = self.data_payment.get('client')
        payment = self.get_payment()
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

    def get_project(self, **kwargs):
        return Project()

    def save_project(self):
        project = self.project
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
        save_client = self.save_clients(project)
        if not save_client:
            return None, self.MESSAGE_ERROR_CLIENT
        save_deliveries = self.save_delivery_dates(project)
        if not save_deliveries:
            return None, self.MESSAGE_ERROR_DELIVERY
        save_duty = self.save_duty(project)
        if not save_duty:
            return None, self.MESSAGE_ERROR_DUTY
        return project, None

    def save_duty(self, project):
        duty_detail = DutyDetail()
        duty_detail.project = project
        try:
            if self.data_duty.get('type_contract', None) is not None:
                duty_detail.type_contract_id = self.data_duty.get('type_contract').get('id')

            if self.data_duty.get('duration_month', None) is not None:
                duty_detail.duration_month = self.data_duty.get('duration_month')
            duty_detail.save()

            for broadcast in self.data_duty.get('broadcasts', []):
                duty_detail.broadcast.add(Broadcast.objects.get(pk=broadcast.get('id')))

            for country in self.data_duty.get('countries', []):
                duty_detail.country.add(Country.objects.get(pk=country.get('id')))
            return True
        except:
            return False

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
            if delivery.get('date') is not None:
                try:
                    project_delivery = ProjectDetailDeliveries()
                    project_delivery.project = project
                    project_delivery.delivery_date = self.format_date(delivery.get('date'))
                    project_delivery.save()
                except:
                    return False
        return True

    def validate_type_client(self,client, type_validate):
        types = client.type_client.all()
        for type in types:
            if type == type_validate:
                return True
        return False

    def save_clients(self, project):
        type_director = TypeClient.objects.get(name='Realizadora')
        type_agency = TypeClient.objects.get(name='Agencia')
        type_productor = TypeClient.objects.get(name='Productora')

        id_director = self.data_client.get('director', None)
        id_agency = self.data_client.get('agency', None)
        id_productor = self.data_client.get('productor', None)

        if id_director is not None:
            client_director = Client.objects.get(pk=id_director)
            if self.validate_type_client(client_director, type_director):
                client_detail = ProjectClientDetail(
                    project=project,
                    client=client_director,
                    type=type_director
                )
                client_detail.save()
            else:
                return False

        if id_agency is not None:
            client_agency = Client.objects.get(pk=id_agency)
            if self.validate_type_client(client_agency, type_agency):
                client_detail = ProjectClientDetail(
                    project=project,
                    client=client_agency,
                    type=type_agency
                )
                client_detail.save()
            else:
                return False

        if id_productor is not None:
            client_productor = Client.objects.get(pk=id_productor)
            if self.validate_type_client(client_productor, type_productor):
                client_detail = ProjectClientDetail(
                    project=project,
                    client=client_productor,
                    type=type_productor
                )
                client_detail.save()
            else:
                return False
        return True

    def set_attributes(self, data):
        self.data_duty = data.get('duty')
        self.data_project = data.get('project')
        self.data_line = data.get('line')
        self.data_client = data.get('client')
        self.data_commercial = data.get('commercial')
        self.data_deliveries = data.get('deliveries')
        self.data_models = data.get('models')
        self.data_resources = data.get('resources')
        self.data_payment = data.get('payment')

        kwargs = {
            'project_id': data.get('project_id'),
            'line': self.data_project.get('line_productions')
        }
        self.project = self.get_project(**kwargs)
        self.casting = self.get_casting(**kwargs)
        self.extras= self.get_extras(**kwargs)
        self.photo_casting = self.get_photo_casting(**kwargs)
        self.representation = self.get_representation(**kwargs)

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
    MESSAGE_SUCCESS = 'Projecto actualizado correctamente'

    def get_representation(self, **kwargs):
        if kwargs.get('line') == Project.LINE_REPRESENTATION:
            representation = Representation.objects.get(project=self.project)
            return representation
        else:
            return Representation()

    def save_detail_model_representation(self, project_line):
        RepresentationDetailModel.objects.filter(representation=project_line).delete()
        return super(ProjectUpdateJsonView, self).save_detail_model_representation(project_line)

    def get_photo_casting(self, **kwargs):
        if kwargs.get('line') == Project.LINE_PHOTO:
            photo_casting = PhotoCasting.objects.get(project=self.project)
            return photo_casting
        else:
            return PhotoCasting()

    def save_detail_model_photo(self, project_line):
        PhotoCastingDetailModel.objects.filter(photo_casting=project_line).delete()
        return super(ProjectUpdateJsonView, self).save_detail_model_photo(project_line)

    def get_extras(self, **kwargs):
        if kwargs.get('line') == Project.LINE_EXTRA:
            extras = Extras.objects.get(project=self.project)
            return extras
        else:
            return Extras()

    def save_detail_model_extra(self, project_line):
        ExtrasDetailModel.objects.filter(extras=project_line).delete()
        return super(ProjectUpdateJsonView, self).save_detail_model_extra(project_line)

    def get_casting(self, **kwargs):
        if kwargs.get('line') == Project.LINE_CASTING:
            casting = Casting.objects.get(project=self.project)
            return casting
        else:
            return Casting()

    def save_detail_model_casting(self, project_line):
        CastingDetailModel.objects.filter(casting=project_line).delete()
        return super(ProjectUpdateJsonView, self).save_detail_model_casting(project_line)

    def get_project(self, **kwargs):
        project = Project.objects.get(pk=kwargs.get('project_id'))
        return project

    def save_clients(self, project):
        ProjectClientDetail.objects.filter(project=project).delete()
        return super(ProjectUpdateJsonView, self).save_clients(project)

    def save_delivery_dates(self, project):
        ProjectDetailDeliveries.objects.filter(project=project).delete()
        return super(ProjectUpdateJsonView, self).save_delivery_dates(project)

    def save_duty(self, project):
        DutyDetail.objects.filter(project=project).delete()
        return super(ProjectUpdateJsonView, self).save_duty(project)

    def save_resources(self, project):
        ProjectDetailStaff.objects.filter(project=project).delete()
        return super(ProjectUpdateJsonView, self).save_resources(project)

    def get_payment(self, **kwargs):
        try:
            return Payment.objects.get(project=self.project)
        except:
            return Payment()

    def process_validate(self):
        commercial = Commercial.objects.get(pk=self.data_project.get('commercial'))
        if Project.objects.filter(
                commercial=commercial,
                line_productions=self.data_project.get('line_productions')
        ).exclude(id__in=[self.project.id]).exists():
            return False, self.MESSAGE_ERROR_COMMERCIAL
        return True, None

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        context = {}
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
                    'budget_cost': float(detail.budget_cost),
                    'budget': float(detail.budget),
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
                    'budget': float(detail.budget) if detail.budget is not None else None
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
                    'budget_cost': float(detail.budget_cost) if detail.budget_cost is not None else None,
                    'observations': detail.observations
                })

        if self.line.get('id') == Project.LINE_REPRESENTATION:
            details = self.line_project.representation_detail_model_set.all()
            for detail in details:
                data.append({
                    'profile': detail.profile,
                    'model_name': detail.model.name_complete,
                    'model': {
                        'document': detail.model.get_type_doc_display() + ' | ' + detail.model.number_doc,
                        'id': detail.model.id,
                        'name': detail.model.name_complete,
                    },
                    'character': {
                        'id': detail.character,
                        'name': detail.get_character_display()
                    },
                    'currency': {
                        'id': detail.currency.id,
                        'symbol': detail.currency.symbol
                    },
                    'budget_cost': float(detail.budget_cost) if detail.budget_cost is not None else None,
                    'budget': float(detail.budget) if detail.budget is not None else None
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
                        'id_emp': staff.employee,
                    },
                    'percentage': int(staff.percentage),
                    'budget': float(staff.budget) if staff.budget is not None else None,
                    'total': float((staff.budget * staff.percentage)/100)
                })
        except:
            return data
        return data

    def get_payment(self):
        try:
            payment = Payment.objects.get(project=self.project)
            data = {
                'client': {
                    'type': self.get_types(payment.client.type_client.all()),
                    'id': payment.client.id,
                    'name': payment.client.name
                }
            }
            if self.project.currency is not None:
                data.update({
                    'currency': {
                    'symbol': self.project.currency.symbol,
                    'id': self.project.currency.id
                    }
                })
            return data
        except Exception,e :
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

    def get_duty(self):
        duty_detail = DutyDetail.objects.get(project=self.project)
        return {
            'duration_month': duty_detail.duration_month,
            'broadcasts': self.get_types(duty_detail.broadcast.all()),
            'type_contract': {
                'id': duty_detail.type_contract.id,
                'name': duty_detail.type_contract.name
            },
            'countries': self.get_types(duty_detail.country.all())

        }

    def get_data_project(self):
        project = {
            'id': self.project.id,
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
            "observation": self.project.observations,
            "duty":  self.get_duty()
        }

        if self.line.get('id') == Project.LINE_CASTING:
            project.update({
                "typeCasting": self.get_types(self.line_project.type_casting.all()),
                "ppi": self.line_project.ppi.strftime("%d/%m/%Y") if self.line_project.ppi is not None else None,
                "ppg": self.line_project.ppg.strftime("%d/%m/%Y") if self.line_project.ppg is not None else None,
                "internalBudget": float(self.project.budget_cost),
                "budget": float(self.project.budget)
            })
        if self.line.get('id') == Project.LINE_PHOTO:
            project.update({
                "type": {
                    'id': self.line_project.type_casting.id,
                    'name': self.line_project.type_casting.name
                },
                "use": self.get_types(self.line_project.use_photo.all()),
                "budget": float(self.project.budget)
            })
        if self.line.get('id') == Project.LINE_REPRESENTATION:
            event = {}
            if self.line_project.type_event is not None:
                event.update({
                    'id': self.line_project.type_event.id,
                    'name': self.line_project.type_event.name
                })
            project.update({
                "event": event,
                "ppi": self.line_project.ppi.strftime("%d/%m/%Y") if self.line_project.ppg is not None else None,
                "ppg": self.line_project.ppg.strftime("%d/%m/%Y") if self.line_project.ppg is not None else None,
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