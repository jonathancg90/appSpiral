# -*- coding: utf-8 -*-

from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from apps.common.view import SearchFormMixin
from apps.sp.forms.Commercial import CommercialForm, CommercialFiltersForm
from django.core.urlresolvers import reverse
from apps.sp.models.Commercial import Commercial


class CommercialCreateView(CreateView):
    model = Commercial
    form_class = CommercialForm
    template_name = 'panel/commercial/crud.html'
    success_url = 'commercial_list'

    def get_context_data(self, **kwargs):
        context = super(CommercialCreateView,self).get_context_data(**kwargs)
        context['action'] = 'create'
        return context


class CommercialUpdateView(UpdateView):
    model = Commercial
    form_class = CommercialForm
    template_name = 'panel/commercial/crud.html'
    success_url = 'commercial_list'

    def get_context_data(self, **kwargs):
        context = super(CommercialUpdateView,self).get_context_data(**kwargs)
        context['action'] = 'update'
        return context

class CommercialDeleteView(DeleteView):
    model = Commercial
    template_name = 'panel/commercial/crud.html'
    success_url = 'commercial_list'

    def get_context_data(self, **kwargs):
        context = super(CommercialDeleteView,self).get_context_data(**kwargs)
        context['action'] = 'delete'
        return context

class CommercialListView(SearchFormMixin, ListView):
    model = Commercial
    template_name = 'panel/commercial/commercial_list.html'
    search_form_class = CommercialFiltersForm
    filtering = {
        'name': SearchFormMixin.ALL,
        'entry_id': SearchFormMixin.ALL,
        'brand_id': SearchFormMixin.ALL,
    }

    def get_context_data(self, **kwargs):
        return super(CommercialListView, self).get_context_data(**kwargs)

