from apps.common.view import  SearchMixin
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from apps.sp.forms.Entry import EntryForm
from apps.sp.models.Entry import Entry
from apps.sp.forms.Entry import EntryFiltersForm


class EntryCreateView(CreateView):
    form_class = EntryForm
    template_name = 'panel/entry/crud.html'
    success_url = 'entry_list'

    def get_context_data(self, **kwargs):
        context = super(EntryCreateView,self).get_context_data(**kwargs)
        context['action'] = 'create'
        return context


class EntryUpdateView(UpdateView):
    form_class = EntryForm
    template_name = 'panel/entry/crud.html'
    success_url = 'entry_list'

    def get_context_data(self, **kwargs):
        context = super(EntryUpdateView,self).get_context_data(**kwargs)
        context['action'] = 'update'
        return context


class EntryDeleteView(DeleteView):
    model = Entry
    template_name = 'panel/entry/crud.html'
    success_url = 'entry_list'

    def get_context_data(self, **kwargs):
        context = super(EntryUpdateView,self).get_context_data(**kwargs)
        context['action'] = 'delete'
        return context


class EntryListView(SearchMixin, ListView):
    model = Entry
    template_name = 'panel/entry/entry_list.html'
    search_form_class = EntryFiltersForm

    def get_context_data(self, **kwargs):
        return super(EntryListView, self).get_context_data(**kwargs)
