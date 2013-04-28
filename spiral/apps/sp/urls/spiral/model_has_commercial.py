# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from django.views.generic import TemplateView

urlpatterns = patterns('',


    #Model has commercial
    url(r'model-commercial/$',
        TemplateView.as_view(template_name='base.html'),
        name='model_commercial_list'),
    url(r'model-commercial/create/$',
        TemplateView.as_view(template_name='base.html'),
        name='model_commercial_create'),
    url(r'model-commercial/delete/$',
        TemplateView.as_view(template_name='base.html'),
        name='model__commercial_delete'),

)