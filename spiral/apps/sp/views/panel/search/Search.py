# -*- coding: utf-8 -*-
import json

from django.views.generic import View, TemplateView

from apps.common.view import LoginRequiredMixin, PermissionRequiredMixin
from apps.common.view import NewJSONResponseMixin
from apps.sp.models.Country import Country
from apps.sp.models.Model import Model
from apps.sp.models.Project import Project
from django.contrib.auth.models import Permission
from apps.sp.models.List import DetailList, UserCollaborationDetail, List
from apps.sp.models.Feature import Feature, FeatureValue
from apps.sp.logic.search import Search


class ModelSearchTemplateView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'panel/search/model/search.html'
    model = Model

    def verify_permissions(self):
        permission = Permission.objects.filter(codename='add_model')
        has_permission = self.request.user.has_perm(permission)
        return has_permission

    def get_context_data(self, **kwargs):
        context = super(ModelSearchTemplateView, self).get_context_data(**kwargs)
        context['menu'] = 'search'
        context['update_model'] = self.verify_permissions()
        return context


class ModelSearchView(LoginRequiredMixin, NewJSONResponseMixin, View):

    def set_attributes(self):
        self._type = self.request.POST.get('type')
        self._paginate = self.request.POST.get('paginate')
        self._text = self.request.POST.get('text', None)
        self._mode = self.request.POST.get('mode')
        self._features = self.request.POST.get('features', None)
        self._advance = self.request.POST.get('advance', None)
        if self._advance is not None:
            self._advance = json.loads(self._advance)
            self._order = self.get_order()
        if self._features is not None:
            self._features = json.loads(self._features)

    def get_order(self):
        for item in self._advance:
            if item.get('camp') == 'orden':
                data = {'as': 'desc'}

                if item.get('id') == 'casting':
                    data.update({'camp': 'cant_casting'})
                    self._advance.remove(item)
                    return data
                elif item.get('id') == 'extra':
                    data.update({'camp': 'cant_extra'})
                    self._advance.remove(item)
                    return data
                elif item.get('id') == 'visita':
                    data.update({'camp': 'last_visit'})
                    self._advance.remove(item)
                    return data
                else:
                    return None
        return None

    def post(self ,request, *args, **kwargs):
        data = {}
        self.set_attributes()

        search = Search()

        #Default: Insensitive
        if self._mode in 'true':
            search.set_mode(Search.MODE_SENSITIVE)

        #Default Simple
        if self._type == str(Search.TYPE_ADVANCE):
            # if self._order is not None:
            search.set_order_by(self._order)
            search.set_type(Search.TYPE_ADVANCE)
            data.update({'features': self._features})
            data.update({'advance': self._advance})
        else:
            search.set_paginate(self._paginate)
            data.update({'text': self._text})
        search.set_params(data)
        result = search.run()
        result = list(result)
        return self.render_json_response(result)


class ModelFeatureDataJsonView(LoginRequiredMixin, NewJSONResponseMixin, View):

    def get_nationalities(self):
        data = []
        countries = Country.objects.filter(status=Country.STATUS_ACTIVE)
        for country in countries:
            data.append({
                'id': country.id,
                'nationality':  country.nationality
            })
        return data

    def get_occupations(self):
        data = []
        feature=Feature.objects.get(name='Ocupacion')
        feature_values = FeatureValue.objects.filter(feature=feature)
        for value in feature_values:
            data.append({
                'id': value.id,
                'name': value.name
            })
        return data

    def get_genders(self):
        data = []
        data.append({
            'id': Model.GENDER_FEM,
            'text': 'Femenino'
        })
        data.append({
            'id': Model.GENDER_MASC,
            'text': 'Masculino'
        })
        return data

    def get(self, request, *args, **kwargs):
        data = {}
        features = Feature.get_data_features()
        data.update({"features": features})
        data.update({"occupations": self.get_occupations()})
        data.update({"nationalities": self.get_nationalities()})
        data.update({"genders": self.get_genders()})
        return self.render_json_response(data)


class ModelParticipateDataJsonView(LoginRequiredMixin, NewJSONResponseMixin, View):

    def get_list_participate(self):
        data = []
        detail_list = DetailList.objects.filter(model_id=self.kwargs.get('pk'))
        detail_list = detail_list.prefetch_related('list')
        detail_list = detail_list.prefetch_related('list__project')
        detail_list = detail_list.exclude(list__project=None)
        detail_list = detail_list.exclude(list__status= List.STATUS_ARCHIVE)
        detail_list = detail_list.filter(list__project__status=Project.STATUS_START)
        for detail in detail_list:
            user_collaboration = UserCollaborationDetail.objects.get(list=detail.list)
            data.append({
                'id': detail.id,
                'commercial': detail.list.project.commercial.name,
                'name': detail.list.title,
                'owner': user_collaboration.user_owner.username
            })
        return data

    def get(self, request, *args, **kwargs):
        data = {}
        list_participate = self.get_list_participate()
        data.update({"list": list_participate})
        return self.render_json_response(data)


