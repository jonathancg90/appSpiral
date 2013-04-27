# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'hello/$',
        TemplateView.as_view(template_name='base.html'),
        name='main'),
)