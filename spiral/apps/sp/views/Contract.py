from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from apps.sp.forms.Contract import ContractForm
from apps.sp.models.Contract import Contract


class ContractCreateView(CreateView):
    form_class = ContractForm
    template = 'templates/CRUD.html'
    success_url = ''

    def get_context_data(self, **kwargs):
        context = super(ContractCreateView,self).get_context_data(**kwargs)
        context['action'] = 'create'
        return context


class ContractlUpdateView(UpdateView):
    form_class = ContractForm
    template = 'templates/CRUD.html'
    success_url = ''

    def get_context_data(self, **kwargs):
        context = super(ContractlUpdateView,self).get_context_data(**kwargs)
        context['action'] = 'update'
        return context

class ContractDeleteView(DeleteView):
    model = Contract
    template = 'templates/CRUD.html'
    success_url = ''

    def get_context_data(self, **kwargs):
        context = super(ContractDeleteView,self).get_context_data(**kwargs)
        context['action'] = 'delete'
        return context

class ContractListView(ListView):
    model = Contract
    template = ''

