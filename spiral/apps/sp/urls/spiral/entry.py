# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from django.views.generic import TemplateView
from apps.sp.views.Entry import EntryListView, EntryCreateView, EntryUpdateView, EntryDeleteView

urlpatterns = patterns('',

     #Retry
    url(r'retry/$',
        EntryListView.as_view(),
        name='retry_list'),
    url(r'retry/create$',
        TemplateView.as_view(template_name='panel_base.html'),
        name='retry_create'),
    url(r'retry/edit/$',
        TemplateView.as_view(template_name='panel_base.html'),
        name='retry_edit'),
    url(r'retry/delete/$',
        TemplateView.as_view(template_name='panel_base.html'),
        name='retry_delete'),
)