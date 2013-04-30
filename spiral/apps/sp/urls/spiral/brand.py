# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from django.views.generic import TemplateView

urlpatterns = patterns('',

     #Brand
    url(r'brand/$',
        TemplateView.as_view(template_name='panel_base.html'),
        name='brand_list'),
    url(r'brand/create$',
        TemplateView.as_view(template_name='panel_base.html'),
        name='brand_create'),
    url(r'brand/edit/$',
        TemplateView.as_view(template_name='panel_base.html'),
        name='brand_edit'),
    url(r'brand/delete/$',
        TemplateView.as_view(template_name='panel_base.html'),
        name='brand_delete'),
)