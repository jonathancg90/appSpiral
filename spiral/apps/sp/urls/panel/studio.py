# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from apps.sp.views.panel.Studio import StudioListView, StudioCreateView, \
    StudioUpdateView, StudioDeleteView


urlpatterns = patterns('',
                       #Studio
                       url(r'^list/$',
                           StudioListView.as_view(),
                           name='studio_list'),
                       url(r'^create/$',
                           StudioCreateView.as_view(),
                           name='studio_create'),
                       url(r'^edit/(?P<pk>\d+)/$',
                           StudioUpdateView.as_view(),
                           name='studio_edit'),
                       url(r'^delete/(?P<pk>\d+)/$',
                           StudioDeleteView.as_view(),
                           name='studio_delete')
                       )