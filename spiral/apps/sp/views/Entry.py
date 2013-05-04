from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from apps.sp.forms.Entry import EntryForm
from apps.sp.models.Entry import Entry


class EntryCreateView(CreateView):
    form_class = EntryForm
    template = 'templates/CRUD.html'
    success_url = ''

    def get_context_data(self, **kwargs):
        context = super(EntryCreateView,self).get_context_data(**kwargs)
        context['action'] = 'create'
        return context


class EntryUpdateView(UpdateView):
    form_class = EntryForm
    template = 'templates/CRUD.html'
    success_url = ''

    def get_context_data(self, **kwargs):
        context = super(EntryUpdateView,self).get_context_data(**kwargs)
        context['action'] = 'update'
        return context

class EntryDeleteView(DeleteView):
    model = Entry
    template = 'templates/CRUD.html'
    success_url = ''

    def get_context_data(self, **kwargs):
        context = super(EntryUpdateView,self).get_context_data(**kwargs)
        context['action'] = 'delete'
        return context

class EntryListView(ListView):
    model = Entry
    template_name = 'panel/entry/entry_list.html'

    def get_context_data(self, **kwargs):
        return super(EntryListView, self).get_context_data(**kwargs)


