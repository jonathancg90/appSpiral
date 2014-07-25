# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import ListView

from apps.sp.forms.Studio import StudioForm
from apps.sp.models.Studio import Studio
from apps.common.view import LoginRequiredMixin, PermissionRequiredMixin


class StudioListView(LoginRequiredMixin, PermissionRequiredMixin,
                    ListView):
    model = Studio
    template_name = 'panel/studio/studio_list.html'
    paginate_by = settings.PANEL_PAGE_SIZE


class StudioCreateView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    model = Studio
    form_class = StudioForm
    template_name = 'panel/studio/create.html'
    success_url = 'brand_list'
    permissions = {
        "permission": ('sp.add_studio', ),
    }

    def get_context_data(self, **kwargs):
        context = super(StudioCreateView,self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('studio_list')


class StudioUpdateView(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    model = Studio
    form_class = StudioForm
    template_name = 'panel/studio/update.html'
    success_url = 'brand_list'
    permissions = {
        "permission": ('sp.change_studio', ),
        }

    def get_context_data(self, **kwargs):
        context = super(StudioUpdateView, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('studio_list')


class StudioDeleteView(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    model = Studio
    template_name = 'panel/studio/delete.html'
    success_url = 'brand_list'
    permissions = {
        "permission": ('sp.delete_studio', ),
    }

    def get_context_data(self, **kwargs):
        context = super(StudioDeleteView,self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('studio_list')


