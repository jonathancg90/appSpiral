# -*- coding: utf-8 -*-

from apps.common.view import  SearchFormMixin
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, UpdateView,\
    DeleteView, ListView
from django.conf import settings
from apps.sp.forms.Entry import EntryForm
from apps.sp.models.Entry import Entry
from apps.sp.forms.Entry import EntryFiltersForm
from apps.common.view import LoginRequiredMixin


class EntryCreateView(LoginRequiredMixin, CreateView):
    form_class = EntryForm
    template_name = 'panel/entry/create.html'
    success_url = "entry_list"

    def get_context_data(self, **kwargs):
        context = super(EntryCreateView,self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('entry_list')


class EntryUpdateView(LoginRequiredMixin, UpdateView):
    model = Entry
    form_class = EntryForm
    template_name = 'panel/entry/update.html'
    success_url = "entry_list"

    def get_context_data(self, **kwargs):
        context = super(EntryUpdateView,self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('entry_list')


class EntryDeleteView(LoginRequiredMixin, DeleteView):
    model = Entry
    template_name = 'panel/entry/delete.html'
    success_url = "entry_list"

    def get_context_data(self, **kwargs):
        context = super(EntryDeleteView,self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('entry_list')


class EntryListView(LoginRequiredMixin, SearchFormMixin, ListView):
    model = Entry
    template_name = 'panel/entry/entry_list.html'
    search_form_class = EntryFiltersForm
    context_object_name = 'entry_list'
    paginate_by = settings.PANEL_PAGE_SIZE
    filtering = {
        'name': SearchFormMixin.ALL,
    }