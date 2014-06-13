# -*- coding: utf-8 -*-
from django.contrib import messages
from django.views.generic import TemplateView

from apps.common.view import LoginRequiredMixin


class DashboardTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'panel/dashboard.html'


class SettingsTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'panel/settings.html'