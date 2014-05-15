# -*- coding: utf-8 -*-
import json

from django.views.generic import View, TemplateView

from apps.common.view import LoginRequiredMixin
from apps.common.view import NewJSONResponseMixin
from apps.sp.logic.search import Search


class ModelSearchTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'panel/search/model/search.html'


class ModelSearchView(LoginRequiredMixin, NewJSONResponseMixin, View):

    def set_attributes(self):
        self._type = self.request.POST.get('type')
        self._text = self.request.POST.get('text')
        self._mode = self.request.POST.get('mode')

    def post(self ,request, *args, **kwargs):
        self.set_attributes()

        search = Search()

        #Default: Insensitive
        if self._mode in 'true':
            search.set_mode(Search.MODE_SENSITIVE)

        #Default Simple
        if self._type == Search.TYPE_ADVANCE:
            search.set_type(Search.TYPE_ADVANCE)

        data = {'text': self._text}
        search.set_params(data)
        result = search.run()
        result = list(result)
        return self.render_json_response(result)
