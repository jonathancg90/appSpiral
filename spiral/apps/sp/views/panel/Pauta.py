# -*- coding: utf-8 -*-
import json
from datetime import datetime

from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.views.generic import View

from apps.common.view import JSONResponseMixin
from apps.common.view import LoginRequiredMixin, PermissionRequiredMixin


from apps.sp.models.Model import Model
from apps.sp.models.Pauta import Pauta, DetailPauta
from apps.sp.models.UserProfile import UserProfile
from apps.sp.models.Project import Project, ProjectDetailStaff


class PautaTemplateView(LoginRequiredMixin, PermissionRequiredMixin,
                     TemplateView):
    template_name = 'panel/pauta/list.html'
    model = Pauta

    def get_context_data(self, **kwargs):
        context = super(PautaTemplateView, self).get_context_data(**kwargs)
        context['menu'] = 'pauta'
        return context


class PautaListJsonView(LoginRequiredMixin, PermissionRequiredMixin,
                       JSONResponseMixin, View):
    model = Pauta

    def get_queryset(self):
        data = []
        today = datetime.now()
        pautas = Pauta.objects.filter(date=today)
        pautas = pautas.prefetch_related('project')
        pautas = pautas.prefetch_related('project__commercial')
        for pauta in pautas:
            data.append({
                'id': pauta.id,
                'date': pauta.date.strftime('%Y-%m-%d'),
                'detail': self.get_pauta_detail(pauta)
            })
        return data

    def get_pauta_detail(self, pauta):
        data = []
        details = pauta.detail_pauta_set.all()
        project = '%s (%s)' %(pauta.project.commercial.name, pauta.project.get_code())
        for detail in details:
            data.append({
                'id_detail': detail.id,
                'id_model': detail.model.id,
                'photo': detail.model.main_image,
                'project': project,
                'time': detail.hour.strftime('%H:%M %p'),
                'character': detail.character,
                'observation': detail.observation,
                'model': detail.model.name_complete
            })
        return data

    def get(self, request, *args, **kwargs):
        data = {}
        data['pautas'] = self.get_queryset()
        return self.render_to_response(data)


class PautaProjectListJsonView(LoginRequiredMixin, PermissionRequiredMixin,
                               JSONResponseMixin, View):
    model = Pauta

    def get_queryset(self):
        data = []
        user_profile = UserProfile.objects.get(user=self.request.user)

        project_details = ProjectDetailStaff.objects.filter(employee=user_profile.cod_emp)
        project_details = project_details.prefetch_related('project')
        project_details = project_details.prefetch_related('project__commercial')
        for project_detail in project_details:
            data.append({
                'id': project_detail.project.id,
                'name': project_detail.project.commercial.name,
                'code': project_detail.project.get_code(),
                'commercial_id': project_detail.project.commercial.id
            })
        return data

    def get(self, request, *args, **kwargs):
        context = {}
        context['project'] = self.get_queryset()
        return self.render_to_response(context)


class PautaAddModelJsonView(LoginRequiredMixin, PermissionRequiredMixin,
                            JSONResponseMixin, View):
    model = Pauta
    MESSAGE_SUCCESS = 'Modelo agregado a pauta'
    MESSAGE_ERROR = 'No se pudo agregar el modelo a la pauta'
    MESSAGE_ERROR_DETAIL = 'El modelo ya se encuentra en pauta'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(PautaAddModelJsonView, self).dispatch(request, *args, **kwargs)

    def save_pauta(self, data):
        _date = data.get('date').split('/')
        _date = '%s-%s-%s'%(_date[2], _date[1], _date[0])
        model = Model.objects.get(model_code=data.get('model').get('model_code'))
        try:
            pauta = Pauta.objects.get(date=_date, project_id=data.get('project').get('id'))
            if DetailPauta.objects.filter(pauta=pauta, model=model).exists():
                return None, self.MESSAGE_ERROR_DETAIL
        except:
            pauta = Pauta()
            pauta.date = _date
            pauta.project_id = data.get('project').get('id')
            pauta.save()
        try:
            detail_pauta = DetailPauta()
            detail_pauta.hour = data.get('time')
            detail_pauta.pauta = pauta
            detail_pauta.model = model
            detail_pauta.character = data.get('character').get('id')
            detail_pauta.observation = data.get('observation')
            detail_pauta.save()
            return detail_pauta, self.MESSAGE_SUCCESS
        except Exception, e:
            return None, self.MESSAGE_ERROR

    def post(self, request, *args, **kwargs):
        context = {}
        data = json.loads(request.body)
        model, msg = self.save_pauta(data)
        context['status'] = 'success'
        context['message'] = msg
        if model is None:
            context['status'] = 'warning'
        return self.render_to_response(context)