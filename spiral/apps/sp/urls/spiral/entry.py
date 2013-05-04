# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from django.views.generic import TemplateView
from apps.sp.views.Entry import EntryListView, EntryCreateView, EntryUpdateView, EntryDeleteView

urlpatterns = patterns('',

     #Retry
    url(r'entry/$',
        EntryListView.as_view(),
        name='entry_list'),
    url(r'ertry/create$',
        TemplateView.as_view(template_name='panel_base.html'),
        name='entry_create'),
    url(r'entry/edit/$',
        TemplateView.as_view(template_name='panel_base.html'),
        name='entry_edit'),
    url(r'entry/delete/$',
        TemplateView.as_view(template_name='panel_base.html'),
        name='entry_delete'),
)