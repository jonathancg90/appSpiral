# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from apps.sp.views.panel.Model import ModelControlListView

urlpatterns = patterns('',

     #Retry
    url(r'^model-control/list/$',
        ModelControlListView.as_view(),
        name='panel_model_control_list'),
)