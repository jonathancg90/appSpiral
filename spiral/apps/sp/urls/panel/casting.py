# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from apps.sp.views.panel.Casting import CastingCharacterDataList


urlpatterns = patterns('',

                       #Character
                       url(r'^data-character/$',
                           CastingCharacterDataList.as_view(),
                           name='casting_data_character'),

                       )