# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from apps.common.view import SearchFormMixin
from apps.common.view import JSONResponseMixin
from apps.sp.forms.Client import ClientFiltersForm, ClientForm
from apps.sp.models.Client import Client, TypeClient
from apps.common.view import LoginRequiredMixin, PermissionRequiredMixin


class ClientListView(LoginRequiredMixin, PermissionRequiredMixin,
                    SearchFormMixin, ListView):
    model = Client
    template_name = 'panel/client/client_list.html'
    search_form_class = ClientFiltersForm
    paginate_by = settings.PANEL_PAGE_SIZE
    filtering = {
        'name': SearchFormMixin.ALL,
        }


class ClientCreateView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'panel/client/create.html'
    success_url = 'brand_list'
    permissions = {
        "permission": ('sp.add_client', ),
        }

    def get_context_data(self, **kwargs):
        context = super(ClientCreateView,self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('client_list')


class ClientUpdateView(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'panel/client/update.html'
    success_url = 'brand_list'
    permissions = {
        "permission": ('sp.change_client', ),
        }

    def get_context_data(self, **kwargs):
        context = super(ClientUpdateView, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('client_list')


class ClientDeleteView(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    model = Client
    template_name = 'panel/client/delete.html'
    success_url = 'brand_list'
    permissions = {
        "permission": ('sp.delete_client', ),
        }

    def get_context_data(self, **kwargs):
        context = super(ClientDeleteView,self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('client_list')


class ClientDataListView(LoginRequiredMixin, PermissionRequiredMixin,
                             JSONResponseMixin, ListView):
    model = Client

    def get_queryset(self):
        qs = Client.objects.filter(status=Client.STATUS_ACTIVE)
        return qs

    def get_context_data(self, **kwargs):
        data = {}
        brand = self.get_queryset().values('id', 'name')
        data['client'] = [item for item in brand]
        return data


class TypeClientDataListView(LoginRequiredMixin, PermissionRequiredMixin,
                             JSONResponseMixin, ListView):
    model = TypeClient

    def get_context_data(self, **kwargs):
        data = {}
        type = self.get_queryset().values('id', 'name')
        data['types'] = [item for item in type]
        return data

