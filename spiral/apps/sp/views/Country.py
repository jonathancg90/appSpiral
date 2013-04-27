from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from apps.sp.forms.Country import CountryForm
from apps.sp.models.Country import Country


class CountryCreateView(CreateView):
    form_class = CountryForm
    template = 'templates/CRUD.html'
    success_url = ''

    def get_context_data(self, **kwargs):
        context = super(CountryCreateView,self).get_context_data(**kwargs)
        context['action'] = 'create'
        return context


class CountryUpdateView(UpdateView):
    form_class = CountryForm
    template = 'templates/CRUD.html'
    success_url = ''

    def get_context_data(self, **kwargs):
        context = super(CountryUpdateView,self).get_context_data(**kwargs)
        context['action'] = 'update'
        return context

class CountryDeleteView(DeleteView):
    model = Country
    template = 'templates/CRUD.html'
    success_url = ''

    def get_context_data(self, **kwargs):
        context = super(CountryDeleteView,self).get_context_data(**kwargs)
        context['action'] = 'delete'
        return context

class CountryListView(ListView):
    model = Country
    template = ''

