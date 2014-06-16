# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, View
from django.contrib.auth.models import Group, User
from django.contrib.auth.models import Permission
from django.contrib.admin.models import ContentType
from django.shortcuts import redirect
from django.db.models import Q

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

    def get_entity_permissions(self):
        data = []
        content_types = ContentType.objects.filter(Q(app_label='sp') | Q(app_label='auth'))
        for content_type in content_types:
            data.append({
                'content_type_id': content_type.id,
                'content_type_name': content_type.name,
                'content_type_permissions': self.get_permission(content_type)
            })
        return data

    def form_valid(self, form):
        self.object = form.save()
        for post in self.request.POST:
            if 'permission' in post:
                permission = Permission.objects.get(pk=self.request.POST[post])
                self.object.permissions.add(permission)
        return super(AdminGroupCreateView, self).form_valid(form)

    def get_permission(self, entity):
        result = []
        permissions = Permission.objects.filter(content_type=entity)
        for permission in permissions:
            result.append({
                'permission_id': permission.id,
                'permission_name': permission.name
            })
        return result

    def get_context_data(self, **kwargs):
        content = super(AdminGroupCreateView, self).get_context_data(**kwargs)
        content_types = self.get_entity_permissions()
        content['content_types'] = content_types
        return content

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
        users = User.objects.filter(groups=group)
        group_permissions = group.permissions.all()
        for user in users:
            # user_permissions = user.get_all_permissions()
            # for permission in user_permissions:
            for group_permission in group_permissions:
                user.user_permissions.remove(group_permission)
                # if permission == group_permission.content_type.app_label + '.' + group_permission.codename:
        group.delete()

        return redirect(reverse('admin_group_list'))
