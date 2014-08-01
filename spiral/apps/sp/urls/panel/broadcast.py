# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from apps.sp.views.panel.Broadcast import BroadcastJsonView


urlpatterns = patterns('',
                       url(r'^data-json/$',
                           BroadcastJsonView.as_view(),
                           name='broadcast_json')
                       )