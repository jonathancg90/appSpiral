# -*- coding: utf-8 -*-

from django.conf import settings
from django.views.generic import ListView, RedirectView, View
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from apps.common.view import  SearchFormMixin
from apps.common.view import LoginRequiredMixin
from apps.sp.models.ModelHasCommercial import ModelHasCommercial
from apps.sp.models.Model import Model
from apps.sp.forms.ModelHasCommercial import ModelHasCommercialFilterForm
from apps.sp.forms.Commercial import CommercialFiltersForm
from apps.sp.models.Commercial import Commercial
import datetime
import xlwt


class ModelHasCommercialListView(LoginRequiredMixin, SearchFormMixin, ListView):
    template_name = 'panel/model_has_commercial/list.html'
    model = ModelHasCommercial
    context_object_name = 'model_has_commercial_list'
    search_form_class = ModelHasCommercialFilterForm
    paginate_by = settings.PANEL_PAGE_SIZE
    filtering = {
        'commercial_id': SearchFormMixin.ALL,
        'commercial__brand': SearchFormMixin.ALL,
        'commercial__brand__entry': SearchFormMixin.ALL,
        'commercial_realized__icontains': SearchFormMixin.ALL,
    }

    def get(self, request, *args, **kwargs):
        model_code = self.kwargs.get('key')
        if len(model_code) == 6:
            try:
                self.model = Model.objects.get(model_code=model_code)
            except:
                self.model = Model()
                self.model.model_code = model_code
                self.model.name = ''
                self.model.last_name = ''
                self.model.birth = datetime.datetime.now()
                self.model.last_visit = datetime.datetime.now()
                self.model.save()
        else:
            raise Http404

        return super(ModelHasCommercialListView, self).get(request, *args, **kwargs)

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

    def get_queryset(self):
        qs = ModelHasCommercial.objects.filter(model=self.model)
        qs = self._set_filter_brand(qs)
        qs = self._set_filter_entry(qs)
        qs = qs.order_by('-commercial__realized')
        return qs

    def get_search_form(self, form_class):
        brand_id = self.request.GET.get('commercial__brand', None)
        entry_id = self.request.GET.get('commercial__brand__entry', None)
        form = super(ModelHasCommercialListView, self).get_search_form(form_class)
        if brand_id:
            form.set_commercial(brand_id)
        if entry_id:
            form.set_brand(entry_id)
        return form

    def get_context_data(self, **kwargs):
        self.request.session['model_has_commercial'] = self.model
        context = super(ModelHasCommercialListView, self).get_context_data(**kwargs)
        context['model'] = self.model
        context['model_name'] = self.model.get_data_api_json()
        return context


class ModelHasCommercialListModelView(LoginRequiredMixin, SearchFormMixin, ListView):
    template_name = 'panel/model_has_commercial/list.html'
    model = ModelHasCommercial
    context_object_name = 'model_has_commercial_list'
    search_form_class = ModelHasCommercialFilterForm
    paginate_by = settings.PANEL_PAGE_SIZE
    filtering = {
        'commercial_id': SearchFormMixin.ALL,
        'commercial__brand': SearchFormMixin.ALL,
        'commercial__brand__entry': SearchFormMixin.ALL,
    }

    def _set_filter_entry(self, qs):
        entry_id = str(self.request.GET.get('commercial__brand__entry', ''))
        if entry_id.isdigit():
            qs = qs.filter(commercial__brand__entry=entry_id)
        return qs

    def _set_filter_brand(self, qs):
        brand_id = str(self.request.GET.get('commercial__brand', ''))
        if brand_id.isdigit():
            qs = qs.filter(commercial__brand=brand_id)
        return qs

    def get_queryset(self):
        self.model = get_object_or_404(Model, id=self.kwargs.get('pk'))
        qs = ModelHasCommercial.objects.filter(model=self.model)
        qs = self._set_filter_brand(qs)
        qs = self._set_filter_entry(qs)
        return qs

    def get_search_form(self, form_class):
        brand_id = self.request.GET.get('commercial__brand', None)
        entry_id = self.request.GET.get('commercial__brand__entry', None)
        form = super(ModelHasCommercialListModelView, self).get_search_form(form_class)
        if brand_id:
            form.set_commercial(brand_id)
        if entry_id:
            form.set_brand(entry_id)
        return form

    def get_context_data(self, **kwargs):
        context = super(ModelHasCommercialListModelView, self).get_context_data(**kwargs)
        context['model'] = self.model
        return context


class ModelHasCommercialAddListView(LoginRequiredMixin, SearchFormMixin, ListView):
    model = Commercial
    template_name = 'panel/model_has_commercial/add_commercial.html'
    search_form_class = CommercialFiltersForm
    paginate_by = settings.PANEL_PAGE_SIZE
    context_object_name = 'model_has_commercial_add'
    filtering = {
        'name': SearchFormMixin.ALL,
        'brand__entry': SearchFormMixin.ALL,
        'brand_id': SearchFormMixin.ALL,
    }

    def _set_filter_entry(self, qs):
        entry_id = str(self.request.GET.get('brand__entry', ''))
        if entry_id.isdigit():
            qs = qs.filter(brand__entry=entry_id)
        return qs

    def get_queryset(self):
        qs = super(ModelHasCommercialAddListView, self).get_queryset()
        model_id = self.kwargs.get('pk')
        model = get_object_or_404(Model, id=model_id)
        model_commercial = ModelHasCommercial.objects.filter(model=model).values('commercial')
        qs = qs.exclude(pk__in=model_commercial)
        qs = self._set_filter_entry(qs)
        return qs

    def get_search_form(self, form_class):
        entry_id = self.request.GET.get('brand__entry', None)
        form = super(ModelHasCommercialAddListView, self).get_search_form(form_class)
        if entry_id:
            form.set_brand(entry_id)
        return form

    def get_context_data(self, **kwargs):
        context = super(ModelHasCommercialAddListView, self).get_context_data(**kwargs)
        context['model'] = get_object_or_404(Model, id=self.kwargs.get('pk'))
        return context


class ModelHasCommercialRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get(self, request, *args, **kwargs):
        self.model = self.request.session['model_has_commercial']
        return super(ModelHasCommercialRedirectView, self).get(request, *args, **kwargs)

    def get_redirect_url(self):
        return reverse('model_commercial_list', kwargs={
            'key':self.model.model_code
        })


class ModelHasCommercialAddRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get(self, request, *args, **kwargs):
        model_id = kwargs.get('model_id')
        commercial_id = kwargs.get('commercial_id')
        self.save_model_has_commercial(model_id, commercial_id)
        return super(ModelHasCommercialAddRedirectView, self).get(request, *args, **kwargs)

    def save_model_has_commercial(self, model_id, commercial_id):
        model_has_commercial = ModelHasCommercial()
        model_has_commercial.model = get_object_or_404(Model, id=model_id)
        model_has_commercial.commercial = get_object_or_404(Commercial, id=commercial_id)
        model_has_commercial.save()

    def get_redirect_url(self, model_id, commercial_id):
        return reverse('model_commercial_create', kwargs={
            'pk':self.kwargs["model_id"]
        })


class ModelHasCommercialDelRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False
    model_id = None

    def delete_model_has_commercial(self):
        model_has_commercial = get_object_or_404(ModelHasCommercial, id=self.kwargs.get('pk'))
        self.model_id = model_has_commercial.model.id
        model_has_commercial.delete()

    def get_redirect_url(self, pk):
        self.delete_model_has_commercial()
        return reverse('model_has_commercial_model_list', kwargs={
            'pk':self.model_id
        })


class ExportModelHasCommercialRedirectView(LoginRequiredMixin, View):

    def get_model(self):
        pk = self.kwargs.get('pk')
        model = Model.objects.get(pk=pk)
        return model

    def export_excel(self, model):
        commercial = ''
        column = 4
        response = HttpResponse(mimetype="application/ms-excel")
        response['Content-Disposition'] = 'attachment; filename=comercial.xls'

        wb = xlwt.Workbook()
        ws = wb.add_sheet('Sheetname')

        personal_data = model.get_data_api_json()
        try:
            ws.write(0, 0, personal_data.get('name'))
            ws.write(0, 1, personal_data.get('edad'))
            ws.write(0, 2, personal_data.get('estatura'))
        except:
            pass

        ws.write(0, 3, '')
        commercial_realized = ModelHasCommercial.objects.filter(model=model)
        commercial_realized = commercial_realized.order_by('-commercial__realized')

        all = ''
        for commercial in commercial_realized:
            name_commercial = commercial.commercial.name
            date_commercial = commercial.commercial.realized
            date_commercial = date_commercial.strftime('%m/%Y')
            commercial = name_commercial + ' ' +date_commercial
            # ws.write(0, column, commercial)
            all = all + ' ' + commercial + ' - '
            column +=1

        ws.write(2, 0, 'Todo: ')
        ws.write(2, 1, all)

        wb.save(response)
        return response

    def dispatch(self, request, *args, **kwargs):
        model = self.get_model()
        response = self.export_excel(model)
        return response
