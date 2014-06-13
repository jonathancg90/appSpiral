# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, View
from django.contrib.auth.models import Group
from django.shortcuts import redirect

from apps.common.view import LoginRequiredMixin
from apps.sp.forms.Group import GroupForm


class AdminGroupListView(LoginRequiredMixin, ListView):
    template_name = 'panel/admin/group_list.html'
    model = Group
    paginate_by = settings.PANEL_PAGE_SIZE


class AdminGroupCreateView(LoginRequiredMixin, CreateView):
    template_name = 'panel/admin/group_create.html'
    model = Group
    form_class = GroupForm

    def get_success_url(self):
        return reverse('admin_group_list')


class AdminGroupEditView(LoginRequiredMixin, UpdateView):
    template_name = 'panel/admin/group_edit.html'
    model = Group
    form_class = GroupForm

    def get_success_url(self):
        return reverse('admin_group_list')


class AdminGroupDeleteView(LoginRequiredMixin, View):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(AdminGroupDeleteView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = request.POST
        group = Group.objects.get(pk=data.get('deleteGroup'))
        group.delete()
        return redirect(reverse('admin_group_list'))
