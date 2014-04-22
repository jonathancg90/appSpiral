# -*- coding: utf-8 -*-
import xlwt

from django.conf import settings
from django.http import HttpResponse, Http404
from django.views.generic import ListView, View, TemplateView

from apps.common.view import SearchFormMixin
from apps.common.view import LoginRequiredMixin
from apps.common.view import JSONResponseMixin
from apps.sp.models.Commercial import Commercial
from apps.sp.models.Project import Project
from apps.sp.models.ModelHasCommercial import ModelHasCommercial
from apps.sp.forms.ModelHasCommercial import ModelHasCommercialFilterForm
from apps.sp.forms.ModelHasCommercial import ProjectCodeFilterForm


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
    paginate_by = 100

    def get_data_project(self, project_code):
        data_project = {}
        try:
            commercial = Commercial.objects.get(project__project_code=project_code)
            data_project = commercial.get_data_api_json()
            data_project.update({'realized': commercial.realized})
            data_project.update({'code': project_code})
            data_project.update({'response': True})
        except:
            data_project.update({'response': False})
        return data_project

    def get_queryset(self):
        project_code = self.request.GET.get('code', None)
        data = []
        self.data_project = {'response':False}
        if project_code is not None and len(project_code) == 9:
            self.data_project = self.get_data_project(project_code)
            try:
                qs = super(ModelsPerCommercial, self).get_queryset()
                qs = qs.filter(commercial__project__project_code=project_code)
                for model in qs:
                    api_data = model.model.get_data_api_json()
                    api_data.update({
                        'code':model.model.model_code
                    })
                    data.append(api_data)
            except:
                raise Http404
        return data

    def get_project_id(self, project_code):
        try:
            return Project.objects.get(project_code=project_code).id
        except:
            return 0

    def get_context_data(self, **kwargs):
        context = super(ModelsPerCommercial, self).get_context_data(**kwargs)
        project_id = self.get_project_id(self.request.GET.get('code', None))

        if self.data_project.get('response') is True:
            context['project_data'] = self.data_project
            context['project_id'] = project_id
        else:
            context['project_data'] = {}
            context['project_id'] = project_id
        return context


class ExportCommercialRealizedView(LoginRequiredMixin, View):

    def export_excel(self, project_code):
        if project_code is not None and len(project_code) == 9:
            response = HttpResponse(mimetype="application/ms-excel")
            response['Content-Disposition'] = 'attachment; filename=participantes.xls'

            wb = xlwt.Workbook()
            ws = wb.add_sheet('Sheetname')
            column = 8

            commercial = Commercial.objects.get(project__project_code=project_code)

            data_project = commercial.get_data_api_json()
            ws.write(1, 1, 'Nombre')
            ws.write(1, 2, data_project.get('nombre', None))
            ws.write(2, 1, 'Fecha de realizacion')
            ws.write(2, 2, commercial.realized.strftime('%d/%m/%Y'))
            ws.write(3, 1, 'Productora')
            ws.write(3, 2, data_project.get('productora', None))
            ws.write(4, 1, 'Realizadora')
            ws.write(4, 2, data_project.get('realizadora',None))
            ws.write(5, 1, 'Agencia')
            ws.write(5, 2, data_project.get('agencia',None))
            model_has_commercial = ModelHasCommercial.objects.filter(
                commercial__project__project_code=project_code
            )
            ws.write(7, 1, 'Codigo')
            ws.write(7, 2, 'Nombres y apellidos')
            ws.write(7, 3, 'Edad')
            ws.write(7, 4, 'DNI')
            ws.write(7, 5, 'Telefonos')

            for model in model_has_commercial:
                api_data = model.model.get_data_api_json()
                if api_data.get('response', False) is True:
                    ws.write(column, 1, model.model.model_code)
                    ws.write(column, 2, api_data.get('modelo', None))
                    ws.write(column, 3, api_data.get('edad', None))
                    ws.write(column, 4, api_data.get('dni', None))
                    ws.write(column, 5, api_data.get('telefonos', None))
                    column += 1

            wb.save(response)
        return response

    def dispatch(self, request, *args, **kwargs):
        project_code = Project.objects.get(pk=self.kwargs.get('pk')).project_code
        response = self.export_excel(project_code)
        return response


class ModelSearchView(LoginRequiredMixin, TemplateView):
    template_name = 'panel/search/model/search.html'


class ModelBasicSearchView(LoginRequiredMixin, JSONResponseMixin, View):

    def post(self ,request, *args, **kwargs):
        data = []
        data = self.searchModel()
        return self.render_to_response(data)


class ModelAdvanceSearchView(LoginRequiredMixin, TemplateView):
    template_name = 'panel/search/model/advance_search.html'
