# -*- coding: utf-8 -*-
import json
from django.db.models import Q

from django.views.generic import View, TemplateView

from apps.common.view import LoginRequiredMixin
from apps.common.view import NewJSONResponseMixin
from apps.sp.models.Model import ModelFeatureDetail, Model
from apps.sp.models.Feature import Feature
from apps.sp.logic.search import Search


class ModelSearchTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'panel/search/model/search.html'


class ModelSearchView(LoginRequiredMixin, NewJSONResponseMixin, View):

    def set_attributes(self):
        self._type = self.request.POST.get('type')
        self._text = self.request.POST.get('text', None)
        self._mode = self.request.POST.get('mode')
        self._features = self.request.POST.get('features', None)

    def post(self ,request, *args, **kwargs):
        data = {}
        self.set_attributes()

        search = Search()

        #Default: Insensitive
        if self._mode in 'true':
            search.set_mode(Search.MODE_SENSITIVE)

        #Default Simple
        if self._type == Search.TYPE_ADVANCE:
            search.set_type(Search.TYPE_ADVANCE)
            data.update({'features': self._features})
        else:
            data.update({'text': self._text})
        search.set_params(data)
        result = search.run()
        result = list(result)
        return self.render_json_response(result)


class ModelFeatureDataJsonView(LoginRequiredMixin, NewJSONResponseMixin, View):

    def get(self ,request, *args, **kwargs):
        data = []
        # details = ModelFeatureDetail.objects.filter(feature_value_id__in = [7,38])
        model = Model.objects.all().prefetch_related('feature_detail')
        Model.objects.all().prefetch_related()
        details = model.fe
        # details = ModelFeatureDetail.objects.filter(Q(feature_value_id=7) & Q(feature_value_id=38))
        for detail in details:
            data.append({
                'model': detail.model.name_complete,
            })
        return self.render_json_response(data)

        result = Feature.get_data_features()
        return self.render_json_response(result)