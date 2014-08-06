# -*- coding: utf-8 -*-
import json

from django.views.generic import View, TemplateView

from apps.common.view import LoginRequiredMixin
from apps.common.view import NewJSONResponseMixin
from apps.sp.models.Country import Country
from apps.sp.models.Model import ModelFeatureDetail, Model
from apps.sp.models.Feature import Feature, FeatureValue
from apps.sp.logic.search import Search


class ModelSearchTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'panel/search/model/search.html'

    def get_context_data(self, **kwargs):
        context = super(ModelSearchTemplateView, self).get_context_data(**kwargs)
        context['menu'] = 'search'
        return context


class ModelSearchView(LoginRequiredMixin, NewJSONResponseMixin, View):

    def set_attributes(self):
        self._type = self.request.POST.get('type')
        self._text = self.request.POST.get('text', None)
        self._mode = self.request.POST.get('mode')
        self._features = self.request.POST.get('features', None)
        self._advance = self.request.POST.get('advance', None)
        if self._advance is not None:
            self._advance = json.loads(self._advance)
        if self._features is not None:
            self._features = json.loads(self._features)

    def post(self ,request, *args, **kwargs):
        data = {}
        self.set_attributes()

        search = Search()

        #Default: Insensitive
        if self._mode in 'true':
            search.set_mode(Search.MODE_SENSITIVE)

        #Default Simple
        if self._type == str(Search.TYPE_ADVANCE):
            search.set_type(Search.TYPE_ADVANCE)
            data.update({'features': self._features})
            data.update({'advance': self._advance})
        else:
            # if "DNI" in self._text:
            #     data.update({'dni': self._text})
            # else:
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