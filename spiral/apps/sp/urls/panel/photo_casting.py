# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from apps.sp.views.panel.PhotoCasting import TypePhotoCastingDataList, \
    UsePhotoDataList


urlpatterns = patterns('',
                       url(r'^data-types/$',
                           TypePhotoCastingDataList.as_view(),
                           name='photo_casting_data_types'),
                       url(r'^use-photo/$',
                           UsePhotoDataList.as_view(),
                           name='photo_casting_use_photos'),
                       )