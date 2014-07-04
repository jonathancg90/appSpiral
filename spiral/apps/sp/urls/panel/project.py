# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from apps.sp.views.panel.Project import ProjectView

urlpatterns = patterns('',
                       url(r'^$',
                           ProjectView.as_view(),
                           name='project_crud'),
                       )
