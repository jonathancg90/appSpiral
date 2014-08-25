# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from apps.sp.views.panel.Representation import RepresentationEventsDataList, \
    RepresentationCharacterDataList


urlpatterns = patterns('',

                       #events
                       url(r'^data-events/$',
                           RepresentationEventsDataList.as_view(),
                           name='representation_data_event'),
                       url(r'^data-character/$',
                           RepresentationCharacterDataList.as_view(),
                           name='representation_data_character'),
                       )