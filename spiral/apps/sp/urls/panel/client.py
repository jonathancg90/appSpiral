# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from apps.sp.views.panel.Client import ClientListView, ClientCreateView, \
    ClientUpdateView, ClientDeleteView


urlpatterns = patterns('',

                       #Client
                       url(r'^list/$',
                           ClientListView.as_view(),
                           name='client_list'),
                       url(r'^create/$',
                           ClientCreateView.as_view(),
                           name='client_create'),
                       url(r'^edit/(?P<pk>\d+)/$',
                           ClientUpdateView.as_view(),
                           name='client_edit'),
                       url(r'^delete/(?P<pk>\d+)/$',
                           ClientDeleteView.as_view(),
                           name='client_delete')

                       )