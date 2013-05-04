# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from django.views.generic import TemplateView
from apps.sp.views.Entry import EntryListView, EntryCreateView, EntryUpdateView, EntryDeleteView

urlpatterns = patterns('',

     #Retry
    url(r'list/$',
        EntryListView.as_view(),
        name='entry_list'),
    url(r'create/$',
        EntryCreateView.as_view(),
        name='entry_create'),
    url(r'edit/(?P<pk>\d+)/$',
        EntryUpdateView.as_view(),
        name='entry_edit'),
    url(r'delete/(?P<pk>\d+)/$',
        EntryDeleteView.as_view(),
        name='entry_delete'),
)