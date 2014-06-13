# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, FormView, View
from django.contrib.auth.models import User, Group

from apps.common.view import LoginRequiredMixin
from apps.sp.forms.User import UserGroupForm


class AdminUserListView(LoginRequiredMixin, ListView):
    template_name = 'panel/admin/user_list.html'
    model = User
    paginate_by = settings.PANEL_PAGE_SIZE


class AdminUserDetailView(LoginRequiredMixin, FormView):
    template_name = 'panel/admin/user_detail_group.html'
    form_class = UserGroupForm

    def get_form(self, form_class):
        form = super(AdminUserDetailView, self).get_form(form_class)
        form.set_groups()
        return form

    def form_valid(self, form):
        group = form.cleaned_data.get('group')
        user = User.objects.get(pk=self.kwargs.get('pk'))
        group.user_set.add(user)
        permissions = group.permissions.all()
        for permission in permissions:
            user.user_permissions.add(permission)

        return super(AdminUserDetailView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AdminUserDetailView, self).get_context_data(**kwargs)
        user = User.objects.get(pk=self.kwargs.get('pk'))
        context['user_detail'] = user
        context['groups'] = Group.objects.filter(user=user)
        return context

    def get_success_url(self):
        return reverse('admin_user_group_detail', kwargs={'pk': self.kwargs.get('pk')})


class AdminUserGroupDeleteView(LoginRequiredMixin, View):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(AdminUserGroupDeleteView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = request.POST
        group = Group.objects.get(pk=data.get('deleteGroup'))
        user = User.objects.get(pk=kwargs.get('pk'))
        group.user_set.remove(user)
        permissions = group.permissions.all()
        for permission in permissions:
            user.user_permissions.remove(permission)
        return redirect(reverse('admin_user_group_detail', kwargs={'pk': kwargs.get('pk')}))