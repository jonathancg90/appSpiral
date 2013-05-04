# -*- coding: utf-8 -*-

from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from apps.sp.forms.Commercial import CommercialForm
from django.core.urlresolvers import reverse
from apps.sp.models.Commercial import Commercial


class CommercialCreateView(CreateView):
    model = Commercial
    form_class = CommercialForm
    template = 'templates/CRUD.html'
    success_url = ''

    def get_context_data(self, **kwargs):
        context = super(CommercialCreateView,self).get_context_data(**kwargs)
        context['action'] = 'create'
        return context


class CommercialUpdateView(UpdateView):
    model = Commercial
    form_class = CommercialForm
    template = 'templates/CRUD.html'
    success_url = ''

    def get_context_data(self, **kwargs):
        context = super(CommercialUpdateView,self).get_context_data(**kwargs)
        context['action'] = 'update'
        return context

class CommercialDeleteView(DeleteView):
    model = Commercial
    model = Commercial
    template = 'templates/CRUD.html'
    success_url = ''

    def get_context_data(self, **kwargs):
        context = super(CommercialDeleteView,self).get_context_data(**kwargs)
        context['action'] = 'delete'
        return context

class CommercialListView(ListView):
    model = Commercial
    template = ''

