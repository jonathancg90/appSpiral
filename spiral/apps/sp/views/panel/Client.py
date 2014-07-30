# -*- coding: utf-8 -*-
import json

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError

from apps.common.view import SearchFormMixin
from apps.common.view import JSONResponseMixin
from apps.sp.forms.Client import ClientFiltersForm, ClientForm
from apps.sp.models.Client import Client, TypeClient
from apps.sp.models.Project import ProjectClientDetail
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

    def delete(self, request, *args, **kwargs):
        client_detail = ProjectClientDetail.objects.filter(client=self.get_object())
        if client_detail:
            self.get_object().status = Client.STATUS_INACTIVE
            self.get_object().save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(ClientDeleteView, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('client_list')


class ClientDataListView(LoginRequiredMixin, PermissionRequiredMixin,
                             JSONResponseMixin, ListView):
    model = Client

    def get_queryset(self):
        qs = Client.objects.filter(status=Client.STATUS_ACTIVE)
        return qs

    def get_client_detail(self, clients):
        data = []
        for client in clients:
            data.append({
                'id': client.id,
                'name': client.name,
                'type': self.get_types(client)
            })
        return data

    def get_types(self, client):
        data = []
        types = client.type_client.all()
        for type in types:
            data.append({
                'id': type.id,
                'name': type.name
            })
        return data


    def get_context_data(self, **kwargs):
        data = {}
        clients = self.get_queryset()
        data['client'] = self.get_client_detail(clients)
        return data


class TypeClientDataListView(LoginRequiredMixin, PermissionRequiredMixin,
                             JSONResponseMixin, ListView):
    model = TypeClient

    def get_context_data(self, **kwargs):
        data = {}
        type = self.get_queryset().values('id', 'name')
        data['types'] = [item for item in type]
        return data


class ClientCreateDataJson(LoginRequiredMixin, PermissionRequiredMixin,
                               JSONResponseMixin, View):
    permissions = {
        "permission": ('sp.add_client', ),
        }
    SAVE_SUCCESSFUL = 'Cliente registrado'
    SAVE_ERROR = 'Ocurrio un error al registrar el cliente'
    SAVE_RUC_ERROR = 'El RUC ingresado ya se encuentra regisrado'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(ClientCreateDataJson, self).dispatch(request, *args, **kwargs)

    def save_client(self, data):
        try:
            client = Client()
            client.name = data.get('name')
            client.address = data.get('address')
            client.ruc = data.get('ruc')
            client.save()
            self.save_type_detail(client, data.get('type'))
            return client, self.SAVE_SUCCESSFUL
        except IntegrityError, e:
            return None, self.SAVE_RUC_ERROR
        except Exception, e:
            return None, self.SAVE_ERROR

    def save_type_detail(self, client, types):
        for type in types:
            client.type_client.add(TypeClient.objects.get(pk=type.get('id')))

    def get_types(self, client):
        data = []
        types = client.type_client.all()
        for type in types:
            data.append({
                'id': type.id,
                'name': type.name
            })
        return data

    def post(self, request, *args, **kwargs):
        context = {}
        data = json.loads(request.body)
        client, msg = self.save_client(data)
        context['status'] = 'success'
        context['message'] = msg
        if client is None:
            context['status'] = 'warning'
        else:
            context['result'] = {
                'name': client.name,
                'id': client.id,
                'type':  self.get_types(client)
            }
        return self.render_to_response(context)
