# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from apps.sp.views.panel.TypeCasting import TypeCastingDataList


urlpatterns = patterns('',

                       #Type Casting
                       url(r'^data-types/$',
                           TypeCastingDataList.as_view(),
                           name='type_casting_data'),

                       )