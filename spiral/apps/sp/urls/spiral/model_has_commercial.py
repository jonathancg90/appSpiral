# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from django.views.generic import TemplateView
from apps.sp.views.ModelHasCommercial import ModelHasCommercialListView, \
    ModelHasCommercialAddListView



urlpatterns = patterns('',

    #Model has commercial
    url(r'list/(?P<key>\w+)/$',
        ModelHasCommercialListView.as_view(),
        name='model_commercial_list'),

    url(r'create/$',
        ModelHasCommercialAddListView.as_view(),
        name='model_commercial_create'),

    url(r'delete/$',
        TemplateView.as_view(template_name='panel/base.html'),
        name='model__commercial_delete'),

)