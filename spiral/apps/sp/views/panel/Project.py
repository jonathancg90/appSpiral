# -*- coding: utf-8 -*-

from django.views.generic import TemplateView

from apps.common.view import LoginRequiredMixin, PermissionRequiredMixin
from apps.sp.models.Project import Project


class ProjectView(LoginRequiredMixin, PermissionRequiredMixin,
                  TemplateView):
    model = Project
    template_name = 'panel/project/crud.html'

