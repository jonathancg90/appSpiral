# -*- coding: utf-8 -*-

from apps.common.view import  SearchFormMixin
from django.views.generic import CreateView, UpdateView,\
    DeleteView, ListView
from django.conf import settings
from apps.sp.forms.Entry import EntryForm
from apps.sp.models.Entry import Entry
from apps.sp.forms.Entry import EntryFiltersForm


class EntryCreateView(CreateView):
    form_class = EntryForm
    template_name = 'panel/entry/crud.html'
    success_url = "entry_list"

    def get_context_data(self, **kwargs):
        context = super(EntryCreateView,self).get_context_data(**kwargs)
        context['action'] = 'create'
        return context



class EntryUpdateView(UpdateView):
    model = Entry
    form_class = EntryForm
    template_name = 'panel/entry/crud.html'
    success_url = "entry_list"

    def get_context_data(self, **kwargs):
        context = super(EntryUpdateView,self).get_context_data(**kwargs)
        context['action'] = 'update'
        return context


class EntryDeleteView(DeleteView):
    model = Entry
    template_name = 'panel/entry/crud.html'
    success_url = "entry_list"

    def get_context_data(self, **kwargs):
        context = super(EntryDeleteView,self).get_context_data(**kwargs)
        context['action'] = 'delete'
        return context


class EntryListView(SearchFormMixin, ListView):
    model = Entry
    template_name = 'panel/entry/entry_list.html'
    search_form_class = EntryFiltersForm
    context_object_name = 'entry_list'
    paginate_by = settings.PANEL_PAGE_SIZE
    filtering = {
        'name': SearchFormMixin.ALL,
    }

    def get_context_data(self, **kwargs):
        return super(EntryListView, self).get_context_data(**kwargs)
