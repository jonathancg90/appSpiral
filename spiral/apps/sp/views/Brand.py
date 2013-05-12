# -*- coding: utf-8 -*-

from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from apps.common.view import SearchFormMixin
from apps.common.view import JSONResponseMixin
from apps.sp.forms.Brand import BrandForm, BrandFiltersForm
from apps.sp.models.Brand import Brand


class BrandListView(SearchFormMixin, ListView):
    model = Brand
    template_name = 'panel/brand/brand_list.html'
    search_form_class = BrandFiltersForm
    filtering = {
        'entry_id': SearchFormMixin.ALL,
        'name': SearchFormMixin.ALL,

    }

    def get_context_data(self, **kwargs):
        return super(BrandListView, self).get_context_data(**kwargs)


class BrandCreateView(CreateView):
    model = Brand
    form_class = BrandForm
    template_name = 'panel/brand/create.html'
    success_url = 'brand_list'

    def get_context_data(self, **kwargs):
        context = super(BrandCreateView,self).get_context_data(**kwargs)
        return context


class BrandUpdateView(UpdateView):
    model = Brand
    form_class = BrandForm
    template_name = 'panel/brand/update.html'
    success_url = 'brand_list'

    def get_context_data(self, **kwargs):
        context = super(BrandUpdateView,self).get_context_data(**kwargs)
        return context


class BrandDeleteView(DeleteView):
    model = Brand
    template_name = 'panel/brand/delete.html'
    success_url = 'brand_list'

    def get_context_data(self, **kwargs):
        context = super(BrandDeleteView,self).get_context_data(**kwargs)
        return context


class BrandByEntryIdJson(JSONResponseMixin, ListView):
    model = Brand

    def get_queryset(self):
        entry_id = self.kwargs.get('entry', 0)
        qs = Brand.objects.filter(entry_id=entry_id)
        return qs

    def get_context_data(self, **kwargs):
        data = {}
        brand = self.get_queryset().values('id', 'name')
        data['brand'] = [item for item in brand]
        return data