# -*- coding: utf-8 -*-

from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from apps.sp.forms.Brand import BrandForm
from apps.sp.models.Brand import Brand


class BrandCreateView(CreateView):
    model = Brand
    form_class = BrandForm
    template = 'templates/CRUD.html'
    success_url = ''

    def get_context_data(self, **kwargs):
        context = super(BrandCreateView,self).get_context_data(**kwargs)
        context['action'] = 'create'
        return context


class BrandUpdateView(UpdateView):
    model = Brand
    form_class = BrandForm
    template = 'templates/CRUD.html'
    success_url = ''

    def get_context_data(self, **kwargs):
        context = super(BrandUpdateView,self).get_context_data(**kwargs)
        context['action'] = 'update'
        return context

class BrandDeleteView(DeleteView):
    model = Brand
    template = 'templates/CRUD.html'
    success_url = ''

    def get_context_data(self, **kwargs):
        context = super(BrandDeleteView,self).get_context_data(**kwargs)
        context['action'] = 'delete'
        return context


class BrandListView(ListView):
    model = Brand
    template = ''
