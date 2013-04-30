# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from django.views.generic import TemplateView

urlpatterns = patterns('',

    #Contract
    url(r'contract/$',
        TemplateView.as_view(template_name='panel_base.html'),
        name='contract_list'),
    url(r'contract/create/$',
        TemplateView.as_view(template_name='panel_base.html'),
        name='contract_create'),
    url(r'contract/edit/$',
        TemplateView.as_view(template_name='panel_base.html'),
        name='contract_edit'),
    url(r'contract/delete/$',
        TemplateView.as_view(template_name='panel_base.html'),
        name='contract_delete'),
    )