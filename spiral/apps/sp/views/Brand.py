# -*- coding: utf-8 -*-

from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from apps.common.view import SearchFormMixin
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
    template_name = 'panel/brand/crud.html'
    success_url = 'brand_list'

    def get_context_data(self, **kwargs):
        context = super(BrandCreateView,self).get_context_data(**kwargs)
        context['action'] = 'create'
        return context


class BrandUpdateView(UpdateView):
    model = Brand
    form_class = BrandForm
    template_name = 'panel/brand/crud.html'
    success_url = 'brand_list'

    def get_context_data(self, **kwargs):
        context = super(BrandUpdateView,self).get_context_data(**kwargs)
        context['action'] = 'update'
        return context


class BrandDeleteView(DeleteView):
    model = Brand
    template_name = 'panel/brand/crud.html'
    success_url = 'brand_list'

    def get_context_data(self, **kwargs):
        context = super(BrandDeleteView,self).get_context_data(**kwargs)
        context['action'] = 'delete'
        return context


