# -*- coding: utf-8 -*-

from django.conf import settings
from django.views.generic import ListView
from apps.common.view import  SearchFormMixin
from apps.common.view import LoginRequiredMixin
from apps.sp.models.Commercial import Commercial
from apps.sp.models.ModelHasCommercial import ModelHasCommercial
from apps.sp.forms.ModelHasCommercial import ModelHasCommercialFilterForm, \
    ProjectCodeFilterForm
from django.http import HttpResponseRedirect, Http404


class CommercialRealizedListView(LoginRequiredMixin, SearchFormMixin, ListView):
    template_name = 'panel/search/commercial_realized.html'
    model = ModelHasCommercial
    context_object_name = 'search_commercial_realized'
    search_form_class = ModelHasCommercialFilterForm
    paginate_by = settings.PANEL_PAGE_SIZE
    filtering = {
        'commercial_id': SearchFormMixin.ALL,
        'commercial__brand': SearchFormMixin.ALL,
        'commercial__brand__entry': SearchFormMixin.ALL,
        'commercial_realized__iexact': SearchFormMixin.ALL,
    }

    def get_queryset(self):
        qs = super(CommercialRealizedListView, self).get_queryset()
        qs = self._set_filter_brand(qs)
        qs = self._set_filter_entry(qs)
        qs = qs.order_by('-commercial__realized')
        return qs

    def _set_filter_entry(self, qs):
        entry_id = str(self.request.GET.get('commercial__brand__entry', None))
        if entry_id.isdigit():
            qs = qs.filter(commercial__brand__entry=entry_id)
        return qs

    def _set_filter_brand(self, qs):
        brand_id = str(self.request.GET.get('commercial__brand', ))
        if brand_id.isdigit():
            qs = qs.filter(commercial__brand=brand_id)
        return qs

    def get_search_form(self, form_class):
        brand_id = self.request.GET.get('commercial__brand', None)
        entry_id = self.request.GET.get('commercial__brand__entry', None)
        form = super(CommercialRealizedListView, self).get_search_form(form_class)
        if brand_id:
            form.set_commercial(brand_id)
        if entry_id:
            form.set_brand(entry_id)
        return form


class ModelsPerCommercial(LoginRequiredMixin, SearchFormMixin, ListView):
    template_name = 'panel/search/models_per_commercial.html'
    model = ModelHasCommercial
    context_object_name = 'search_model_per_commercial'
    search_form_class = ProjectCodeFilterForm
    paginate_by = settings.PANEL_PAGE_SIZE

    def get_data_project(self, project_code):
        data_project = {}
        commercial = Commercial.objects.get(project__project_code=project_code)
        data_project = commercial.get_data_api_json()
        data_project.update({'realized': commercial.realized})
        return data_project

    def get_queryset(self):
        project_code = self.request.GET.get('code', None)
        data = []
        self.data_project = None
        if project_code is not None and len(project_code) == 9:
            self.data_project = self.get_data_project(project_code)
            try:
                qs = super(ModelsPerCommercial, self).get_queryset()
                qs = qs.filter(commercial__project__project_code=project_code)
                for model in qs:
                    appi_data = model.model.get_data_api_json()
                    tmp = {}
                    tmp['code'] = model.model.model_code
                    if appi_data.get('response') is True:
                        tmp['name'] = appi_data.modelo
                        tmp['edad'] = appi_data.edad
                        tmp['dni'] = None
                        tmp['telefonos'] = None

                    data.append(tmp)
            except:
                raise Http404
        return data

    def get_context_data(self, **kwargs):
        context = super(ModelsPerCommercial, self).get_context_data(**kwargs)
        if self.data_project is not None:
            if self.data_project.get('response')==True:
                context['project_data'] = {
                    'name': self.date_project.realized,
                    'date': self.date_project,
                    'productora': self.date_project,
                    'realizadora': self.date_project,
                    'agencia': self.date_project
                }
            else:
                context['project_data'] = {}
        return context
