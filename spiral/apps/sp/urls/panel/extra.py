# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from apps.sp.views.panel.Extra import ExtraCharacterDataList


urlpatterns = patterns('',

                       #Character
                       url(r'^data-character/$',
                           ExtraCharacterDataList.as_view(),
                           name='extra_data_character'),

                       )