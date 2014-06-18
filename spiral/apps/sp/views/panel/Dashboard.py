# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import TemplateView

from apps.common.view import LoginRequiredMixin, PermissionRequiredMixin


class DashboardTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'panel/dashboard.html'


class SettingsTemplateView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    model = User
    template_name = 'panel/admin/settings.html'