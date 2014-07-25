# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from apps.sp.views.panel.Entry import EntryListView, \
    EntryCreateView, EntryUpdateView, EntryDeleteView, \
    EntryDataListView

urlpatterns = patterns('',

     #Entry
    url(r'^list/$',
        EntryListView.as_view(),
        name='entry_list'),
    url(r'^create/$',
        EntryCreateView.as_view(),
        name='entry_create'),
    url(r'^edit/(?P<pk>\d+)/$',
        EntryUpdateView.as_view(),
        name='entry_edit'),
    url(r'^delete/(?P<pk>\d+)/$',
        EntryDeleteView.as_view(),
        name='entry_delete'),
    url(r'^data-list/$',
        EntryDataListView.as_view(),
        name='entry_data_list'),
)