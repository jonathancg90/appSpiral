# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from apps.sp.views.panel.PhotoCasting import TypePhotoCastingDataList


urlpatterns = patterns('',

                       #Character
                       url(r'^data-types/$',
                           TypePhotoCastingDataList.as_view(),
                           name='photo_casting_data_types'),

                       )